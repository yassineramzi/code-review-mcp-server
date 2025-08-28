# app/handlers.py
from .models import CodeReviewRequest, CodeReviewResponse, ReviewComment
from .compliance import sanitize_code
from typing import List


class MCPTools:
    """
    A small collection of typed tools the LLM/agent could call.
    In the real system these would be callable RPCs or structured tool calls.
    """

    @staticmethod
    def analyze_diff_for_prints(code: str) -> List[ReviewComment]:
        comments = []
        # naive: for each line that contains 'print(' return a warning
        for idx, line in enumerate(code.splitlines(), start=1):
            if "print(" in line:
                comments.append(
                    ReviewComment(line=idx, comment="Avoid using 'print' in production code.", severity="WARNING")
                )
        return comments

    @staticmethod
    def find_todos(code: str) -> List[ReviewComment]:
        comments = []
        for idx, line in enumerate(code.splitlines(), start=1):
            if "TODO" in line or "FIXME" in line:
                comments.append(
                    ReviewComment(line=idx, comment="Resolve TODO/FIXME before merging.", severity="INFO")
                )
        return comments


def analyze_code(request: CodeReviewRequest) -> CodeReviewResponse:
    """
    Orchestrates available tools and returns an aggregated response.
    This function is intentionally simple to stay as an MVP. Replace
    or extend by calling an LLM agent that can call MCPTools methods.
    """
    # sanitize code and remember if sanitized
    sanitized_code, sanitized_flag = sanitize_code(request.code)

    comments = []
    # call typed tools
    comments.extend(MCPTools.analyze_diff_for_prints(sanitized_code))
    comments.extend(MCPTools.find_todos(sanitized_code))

    # deduplicate comments on the same line with same message
    unique = {}
    for c in comments:
        key = (c.line, c.comment)
        if key not in unique:
            unique[key] = c
    deduped_comments = list(unique.values())

    response = CodeReviewResponse(
        repo=request.repo,
        pr_id=request.pr_id,
        file_path=request.file_path,
        comments=deduped_comments,
        sanitized=sanitized_flag,
        original_length=len(request.code)
    )
    return response
