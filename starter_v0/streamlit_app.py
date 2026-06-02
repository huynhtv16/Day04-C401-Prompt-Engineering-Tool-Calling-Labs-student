import streamlit as st
import subprocess
import sys
import json
from pathlib import Path
import glob

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version
from chat import run_model_tool_loop, trim_history, write_transcript, now_iso, safe_slug

ROOT = Path(__file__).parent
load_lab_env(ROOT)


def run_cmd(cmd):
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return 1, "", str(e)


def render_tool_rounds(rounds):
    for round_record in rounds:
        st.markdown(f"**Tool round {round_record.get('round')}**")
        tool_calls = round_record.get("tool_calls") or []
        if tool_calls:
            st.write("Tool calls:")
            for call in tool_calls:
                st.write(f"- {call.get('name')}")
            with st.expander("Show tool details"):
                st.write("Tool call args:")
                st.json(tool_calls)
                tool_results = round_record.get("tool_results")
                if tool_results:
                    st.write("Tool results:")
                    st.json(tool_results)
        if round_record.get("assistant_text"):
            st.write("Assistant text:")
            st.write(round_record["assistant_text"])


st.title("Research Agent Chat")
st.write("Use the sidebar to configure provider, model, and chat settings.")

with st.sidebar:
    st.title("Settings")
    provider = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
    model = st.text_input("Model (optional)", value="")
    version = st.text_input("Version label", value="v0")
    suite = st.selectbox("Suite", ["base", "group", "extension"], index=0)
    eval_cases = st.text_input("Eval cases file", value="data/eval_base.json")
    st.markdown("---")
    st.subheader("Chat settings")
    system_prompt_path = st.text_input("System prompt path", value=str(ROOT / "artifacts" / "system_prompt.md"))
    tools_path = st.text_input("Tools YAML path", value=str(ROOT / "artifacts" / "tools.yaml"))
    transcripts_dir = st.text_input("Transcripts dir", value=str(ROOT / "transcripts"))
    history_window = st.number_input("History window", value=5, min_value=0)
    max_tool_rounds = st.number_input("Max tool rounds", value=4, min_value=1)
    st.markdown("---")
    if st.button("Run preflight"):
        cmd = [sys.executable, "scripts/preflight_provider.py", "--provider", provider]
        code, out, err = run_cmd(cmd)
        st.subheader("Preflight output")
        st.text(out or err)
    if st.button("Run baseline eval"):
        cmd = [sys.executable, "run_eval.py", "--provider", provider, "--version", version, "--suite", suite, "--eval-cases", eval_cases]
        code, out, err = run_cmd(cmd)
        st.subheader("Run output")
        st.text(out)
        if err:
            st.subheader("Run errors")
            st.text(err)
        run_files = sorted(glob.glob(str(ROOT / "runs" / "*.json")), key=lambda p: Path(p).stat().st_mtime)
        if run_files:
            latest = run_files[-1]
            st.write("Latest run file:")
            st.write(latest)

st.markdown("---")

# ------------------ Chat UI ------------------
st.header("Live Chat")

if "chat_initialized" not in st.session_state:
    st.session_state.chat_initialized = False

if st.button("Start chat session"):
    tool_declarations = load_tool_declarations(Path(tools_path))
    openai_tools = to_openai_tools(tool_declarations)
    provider_obj = make_provider(provider)
    artifact_version = build_artifact_version(version, Path(system_prompt_path), Path(tools_path))
    timestamp = now_iso().replace(":", "").replace("-", "").replace(".", "")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider), timestamp])
    transcript_path = Path(transcripts_dir) / f"{transcript_id}.transcript.json"
    transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider,
        "model": model or getattr(provider_obj, "default_model", None),
        "system_prompt": str(system_prompt_path),
        "tools": str(tools_path),
        "history_window": history_window,
        "max_tool_rounds": max_tool_rounds,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

    st.session_state.provider_obj = provider_obj
    st.session_state.openai_tools = openai_tools
    st.session_state.transcript = transcript
    st.session_state.transcript_path = transcript_path
    st.session_state.history = []
    st.session_state.turn_index = 0
    st.session_state.chat_initialized = True
    st.success(f"Chat session started — transcript: {transcript_path}")

if st.session_state.chat_initialized:
    st.subheader("Conversation")
    for turn_record in st.session_state.transcript["turns"]:
        with st.chat_message("user"):
            st.markdown(turn_record["user"])
        with st.chat_message("assistant"):
            st.markdown(turn_record.get("assistant_text", ""))
            if turn_record.get("rounds"):
                render_tool_rounds(turn_record["rounds"])

    user_input = st.chat_input("Send a message")
    if user_input:
        st.session_state.turn_index += 1
        system_prompt = Path(system_prompt_path).read_text(encoding="utf-8")
        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(st.session_state.history, history_window),
            {"role": "user", "content": user_input},
        ]

        result = run_model_tool_loop(
            provider=st.session_state.provider_obj,
            messages=messages,
            tools=st.session_state.openai_tools,
            model=model or None,
            max_tool_rounds=max_tool_rounds,
        )

        assistant_text = result.get("assistant_text", "")
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": assistant_text})

        turn_record = {
            "turn_index": st.session_state.turn_index,
            "started_at": now_iso(),
            "user": user_input,
            **result,
            "ended_at": now_iso(),
        }
        st.session_state.transcript["turns"].append(turn_record)
        write_transcript(Path(st.session_state.transcript_path), st.session_state.transcript)

        with st.chat_message("assistant"):
            st.markdown(assistant_text)
            if result.get("rounds"):
                render_tool_rounds(result["rounds"])
        st.write(f"Transcript saved: {st.session_state.transcript_path}")

st.markdown("---")

st.subheader("Transcripts")
if st.button("List transcripts"):
    t_files = sorted(glob.glob(str(ROOT / "transcripts" / "*.transcript.json")), key=lambda p: Path(p).stat().st_mtime)
    if not t_files:
        st.write("No transcripts found")
    else:
        for t in t_files[-10:][::-1]:
            st.write(t)
            if st.button(f"Open {Path(t).name}"):
                try:
                    with open(t, "r", encoding="utf-8") as f:
                        st.json(json.load(f))
                except Exception as e:
                    st.text(f"Could not open: {e}")
