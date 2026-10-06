# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Đặng Quang Huy | 02962 | Toàn bộ harness (`agent.py`, `subagents.py`, `runner.py`, `curator.py`), báo cáo |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: chưa cấu hình khóa API trên máy này. Harness dùng `make_model()` khi chạy thật; `recursion_limit` mặc định 60; `LAB_TEMPERATURE` mặc định 0 theo `.env.example`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Python 3.12.3, Ubuntu (kernel 7.0.0-34-generic), chạy trực tiếp (không Docker).
- Số lần chạy tác vụ đã dùng / ngân sách: 0 lần chạy LLM (bộ test ngoại tuyến 32 passed, không tốn token).
- Commit của tag `freeze`: chưa gắn (chưa có lần chạy `skills-auto` trên mô hình thật).

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

Dự đoán trên **tác vụ đánh giá**, trước khi nhìn điểm eval. Căn cứ: phân loại lỗi kỳ vọng (nhóm E chiếm đa số với mô hình có tool calling) và tài liệu lab (SkillsBench, SkillEvolBench, Anthropic multi-agent).

- H1 (subagents so với baseline): Điểm trung bình eval của `subagents` không cao hơn `baseline`, trong khi token trung bình cao hơn, vì subagent bị cô lập ngữ cảnh và dễ thiếu quy tắc trong lời giao việc; Anthropic ghi nhận hệ đa tác tử tốn khoảng 15 lần token so với hội thoại thường.
- H2 (skills-auto so với baseline): `skills-auto` có thể tăng tỉ lệ đạt check quy ước (`rule_`) trên tác vụ học, nhưng trên eval lợi ích trung bình gần 0, vì SkillsBench ghi nhận skill do mô hình tự sinh trung bình không có lợi, khác với skill do người viết.
- H3 (tác vụ học so với tác vụ đánh giá): Mọi chênh lệch dương của `skills-auto` trên tác vụ học sẽ nhỏ hơn (hoặc mất) trên tác vụ đánh giá — dấu hiệu quá khớp theo SkillEvolBench; skill sinh từ `detail` của học không chứa quy ước mới chỉ có trên eval.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có các công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep` (tệp), `execute` (shell), `task` (subagent). Công cụ chạy lệnh là `execute`.
2. Mô tả `task` nói `general-purpose` là agent đa năng để nghiên cứu câu hỏi phức tạp, tìm tệp/nội dung và làm tác vụ nhiều bước; nó có cùng bộ công cụ với tác tử chính. Mỗi lần gọi mặc định không trạng thái: subagent chỉ thấy prompt được gửi và trả về một báo cáo cuối.
3. System prompt mặc định rỗng. Trích từ `task`: "Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report." Trích từ `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search."

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| | | | |

Nhận xét: chưa có `results/baseline/` từ mô hình thật. Sẽ điền sau khi chạy `python -m lab.runner --condition baseline --tasks learn` với mô hình hỗ trợ tool calling.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế): `explorer` (đọc README/docstring/mẫu, không sửa), `implementer` (sửa tệp và chạy test), `reviewer` (đối chiếu kết quả độc lập, không sửa). Tách khảo sát / thực hiện / kiểm chứng để giảm vá triệu chứng (nhóm C) và bỏ qua đặc tả (nhóm A).
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0): chưa có lần chạy thật.
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc): chưa có vết.
- Ảnh hưởng đến token và thời gian: chưa đo.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: 0. `curate_skills` đã cài và `tests/test_04_curator.py` đạt; chưa gọi LLM vì chưa có check thất bại từ baseline thật.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| | | | |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Chưa có `report/table.md` từ `python -m lab.compare` vì chưa đủ `run.json`.

```text
(chưa có bảng — chạy đủ 3 điều kiện × 6 tác vụ rồi `python -m lab.compare > report/table.md`)
```

## 8. Phân tích

1. Chưa có số liệu điểm học/eval theo điều kiện.
2. Chưa tách được check kỹ thuật và check quy ước trên kết quả thật; `scripts/check_breakdown.py` sẵn sàng sau khi có `results/`.
3. Chưa có `skills_read` / `trace.md` từ `skills-auto`.
4. Chi phí token chưa đo trên mô hình thật. Test ngoại tuyến xác nhận `UsageMetadataCallbackHandler` cộng token kể cả subagent.
5. Curator không đưa `role == "eval"` vào prompt; `validate_skill` chặn `eval_markers()` và tên đường dẫn không an toàn (`../evil`). Đây là biện pháp chống rò rỉ, chưa kiểm chứng trên skill do LLM sinh.
6. Nhiễu: chưa có cặp điểm Phần 3.4 và sau đóng băng.

## 9. Hạn chế và tính hợp lệ

1. Số tác vụ nhỏ (3 họ × 1 học + 1 đánh giá): một check quy ước mới trên eval có thể đảo thứ hạng điều kiện.
2. Mỗi cấu hình dự kiến chạy một lần: nhiễu mô hình (cùng skill, khác điểm) không tách được khỏi hiệu quả điều kiện; GUIDE yêu cầu so sánh Phần 3.4 với lần chạy sau freeze đúng vì lý do này.
3. Chưa chạy mô hình thật trên máy nộp harness: mọi kết luận về điểm, token, overfitting phải chờ `LAB_MODEL` hỗ trợ tool calling.
4. Tác vụ do giảng viên thiết kế sẵn quy ước ẩn (`rule_`): điều kiện `skills-auto` được tối ưu đúng loại tín hiệu đó qua `detail` của học, nên lợi ích trên eval có thể không tổng quát ngoài lab.

## 10. Kết luận

Harness Deep Agents đã cài đủ `make_backend`, `build_agent`, `get_subagents`, `run_task` và `curate_skills`. `pytest` đạt 32/32 (offline, không tốn token). Backend không kế thừa biến môi trường (không lộ khóa API) và file tools/shell dùng chung đường dẫn tương đối `workspace/...`. Bước tiếp theo là điền `.env` với mô hình hỗ trợ tool calling, chạy baseline/subagents trên tác vụ học, curator, commit giả thuyết, tag `freeze`, rồi đo eval.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
  - `python3 -m venv .venv && pip install -e .`
  - `pytest` → 32 passed
  - `python scripts/tour.py`
- Thử thách mở rộng (nếu có): chưa làm.
- Ghi chú khác: không commit `.env`. Lần chạy LLM chính thức chưa thực hiện vì chưa có `LAB_MODEL` / khóa API trên môi trường này.
