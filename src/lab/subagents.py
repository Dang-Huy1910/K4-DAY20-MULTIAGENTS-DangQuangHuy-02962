"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Delegate when you first need to survey a workspace: read README, instruction, "
                "docstrings, sample rows, and log fragments, then report facts. Use this before "
                "changing files whenever the layout or data quirks are unclear."
            ),
            "system_prompt": (
                "You are an explorer. Read files and run read-only commands only. "
                "Report the directory layout, relevant conventions, data quirks (duplicates, "
                "missing values, date formats, timezones, log levels), and the exact rules "
                "from README/docstrings. Do not create, edit, or delete files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Delegate when the next step is to change code or write output files "
                "(answer.json, clean.csv, errors.json) and then run tests or a verification "
                "script. Put every task rule, file path, and expected output format in the "
                "delegation message."
            ),
            "system_prompt": (
                "You are an implementer. Apply the requested changes, then verify them "
                "(run tests, re-read outputs, or compute checksums). Report which files you "
                "changed, which commands you ran, and the results. Do not claim a file exists "
                "unless you created or edited it in this session."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Delegate after an implementation pass to independently check the workspace "
                "against the task rules, edge cases, and house conventions. Use this before "
                "the final answer. Do not ask the reviewer to make the edits."
            ),
            "system_prompt": (
                "You are an independent reviewer. Re-read the task rules and the current "
                "workspace. Check edge cases (dirty data, timezones, multiline stack traces, "
                "docstring contracts). Report each issue with a file path and a concrete "
                "mismatch. Do not modify files."
            ),
        },
    ]
