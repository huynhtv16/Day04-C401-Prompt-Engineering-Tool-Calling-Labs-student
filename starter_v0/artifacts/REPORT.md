# Day 04 Lab v2 Report — Research Agent

---

## Team

- Team: [Your Team Name]
- Members: [Member 1, Member 2, ...]
- Provider/model: OpenRouter / openai/gpt-4o-mini

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent giúp tìm thông tin nghiên cứu và tin tức và job từ đa nền tảng, đọc nội dung web, tổng hợp lại thành văn bản, và gửi kết quả lên Telegram. Agent dùng tool để trả lời các yêu cầu: tìm tweet/trending, tìm tin tức, tra cứu URL, định dạng nội dung, và gửi tin nhắn Telegram ngay lập tức.

**Link dùng thử (deploy):**

URL: chạy public trên cloudflare https://endorsed-advertiser-interpreted-reseller.trycloudflare.com/

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại khi thông tin thiếu | không |
| job search | Tìm các job trên mọi web đa nền tảng như linkedIn, ..| Có |
| timeline | Lấy tweet mới nhất từ một tài khoản | không |
| social_search | Tìm tin/trending trên mạng xã hội | không |
| lookup | Tìm nội dung web/news theo truy vấn | không |
| fetch | Lấy nội dung từ một URL | không |
| format | Trình bày và định dạng nội dung đã thu thập | không |
| send | Gửi tin nhắn Telegram ngay lập tức | Có gửi tele khi được yêu cầu |
| policy | Tra cứu chính sách nội bộ | không |
| papers | Tìm bài báo khoa học | không |
| paper_text | Lấy nội dung text từ bài báo | không |

## A3. Câu hỏi mẫu để thử

1. "Tóm tắt 3 tweet mới nhất của Andrej Karpathy." 
2. "Tìm các job trên mạng liên quan đến AI với mức lương from - to sau đó tổng hợp và gửi cho tôi qua telegram"
3. "Tìm tin AI tuần này và gửi bản tin ngắn lên Telegram." 
4. "Đọc bài viết này và tóm tắt 3 ý chính: https://..." 
5. "Tra cứu policy nội bộ về xuất bản bên ngoài và báo lại ngắn gọn." 
6. "Tìm các bài báo AI về reinforcement learning."

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Thiết lập cơ sở và kiểm tra tool routing | 0.70 | 0.70 | runs/v0_B_base_openrouter_20260602T142838455852.json |
| v1 | prompt | Cải thiện routing và clarify để giảm missing_info | 0.70 | 0.75 | runs/v1_B_base_openrouter_20260602T145432624445.json |
| v2 | prompt + send | Cập nhật Telegram send không cần confirm và hoàn thiện boundary | 0.75 | 0.80 | runs/v2_B_base_openrouter_20260602T161750471280.json |

## B2. Failure Analysis

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| G01_direct_timeline_musk | wrong_arg_value | timeline | Agent cần gọi đúng timeline với handle Elon Musk và limit 3 | Cập nhật case để ghi rõ handle và prompt để agent dùng timeline chính xác |
| G09_multiturn_confirm_then_send | wrong_boundary | send | Agent cần gọi send với confirmed=true sau khi người dùng xác nhận gửi | Cập nhật `send` tool và prompt để xử lý trường hợp xác nhận gửi rõ ràng |

## B3. Team Eval Cases

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_direct_timeline_musk | Tóm tắt tweet mới nhất của Elon Musk | timeline screenname=elonmusk limit=3 | success |
| G02_social_search_trending_ai | Tìm nội dung trending AI trên mạng xã hội | social_search query=AI search_type=Top limit=5 | success |
| G03_lookup_news_climate | Tìm tin news về climate change | lookup query=climate change topic=news timeframe=week | success |
| G04_fetch_article_summary | Tóm tắt nội dung từ URL bài viết | fetch url=https://example.com/article | success |
| G05_send_telegram_text | Gửi tin nhắn Telegram với nội dung cụ thể | send text=Thông báo cập nhật AI mới nhất. confirmed=true | success |
| G06_multiturn_fill_handle_then_limit | Multiturn bổ sung handle và giới hạn | timeline screenname=openai limit=3 | success |
| G07_multiturn_carry_topic_and_timeframe | Multiturn chuyển sang semiconductor nhưng vẫn giữ news/week | lookup query=semiconductor topic=news timeframe=week | success |
| G08_multiturn_fill_url_then_fetch | Multiturn cung cấp URL và yêu cầu fetch | fetch url=https://openai.com/index/introducing-gpt-4-1/ | success |
| G09_multiturn_confirm_then_send | Multiturn xác nhận gửi Telegram | send text=Ban lãnh đạo cần theo dõi sát xu hướng AI agent trong tuần này. confirmed=true | success |
| G10_multiturn_out_of_scope_excel | Multiturn yêu cầu công thức Excel ngoài phạm vi research | no_tool refuse | success |
| G011_direct_timeline_musk | Tìm cho tôi các job trên các nền tảng sau đó tổng hợp cho tôi | timeline screenname=job_search limit=3 | success |

## B4. Live Chat Evidence

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "trên twitter đang có trend gì hot" | social_search | transcripts/v2_openrouter_20260602T152120.transcript.json | Agent gọi `social_search` và trả lời danh sách trend |
| 2 | "Tìm các job liên quan đến AI và gửi cho tô qua telegram" | job_search | transcripts/v2_openrouter_20260602T152120.transcript.json | Agent gọi `job_search` và trả lời danh sách trend |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | `tools/send/tool.py` | Gửi Telegram  | Cần kiểm tra tránh gửi nhầm nội dung |
| Job Search  | `tools/job_search/tool.py` | Thêm tool tìm job trên mạng, sau đó tổng hợp gửi qua telegram, có thể tìm các job mình chỉ định |
| UI | `starter_v0/streamlit_app.py` | Chat UI lưu transcript và chạy trực tiếp | Cần đảm bảo config env và dữ liệu an toàn |

## B6. Reflection

- Fixes thuộc `system_prompt.md`: định nghĩa rõ ràng ranh giới tool, ưu tiên `clarify` khi thiếu thông tin, tránh gọi tool khi ngoài phạm vi.
- Fixes thuộc `tools.yaml`: mô tả tool và parameters, đặc biệt `send` giữ tham số `confirmed` nhưng không còn bắt buộc.
- Manual review cần cho: boundary gửi Telegram và nội dung thực tế trước khi gửi đi.
- Cải thiện tiếp theo: chạy thêm phiên bản v3, bổ sung transcript đa lượt hơn, và làm poster / demo nhanh cho phần A.

