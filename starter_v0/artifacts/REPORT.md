# Day 04 Lab v2 Report — Research Agent

<<<<<<< HEAD
=======
> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377
## Team

- Team:
- Members:
- Provider/model:

<<<<<<< HEAD
## Final Metrics

- Final version:
- Final artifact_version:
- Best base run file:
- Base case accuracy:
- Base tool routing accuracy:
- Base argument accuracy:
- Group eval run file:
- Group eval accuracy:
- Chat transcript file:

## Version Evidence
=======
---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: 

## A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

<<<<<<< HEAD
## Failure Analysis
=======
## B2. Failure Analysis
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

<<<<<<< HEAD
## Team Eval Cases

List at least 5 cases added to `data/eval_group.json`.
=======
## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

<<<<<<< HEAD
## Live Chat Evidence
=======
## B4. Live Chat Evidence
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

<<<<<<< HEAD
## Bonus Evidence
=======
## B5. Bonus Evidence
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |

<<<<<<< HEAD
## Reflection
=======
## B6. Reflection
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?
<<<<<<< HEAD

=======
>>>>>>> 23e0c297f4fd4018bbf8cbedf96fad3f8c831377
