# app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class CodeReviewRequest(BaseModel):
    repo: str = Field(..., description="Repository identifier, e.g., org/name")
    pr_id: Optional[int] = Field(None, description="Pull request id (optional)")
    author: Optional[str] = Field(None, description="Author username/email")
    file_path: str = Field(..., description="Path of the file being reviewed")
    code: str = Field(..., description="File contents or diff fragment")
    metadata: Optional[dict] = Field(default_factory=dict, description="Optional metadata")

class ReviewComment(BaseModel):
    line: int
    comment: str
    severity: str  # INFO, WARNING, ERROR

class CodeReviewResponse(BaseModel):
    repo: str
    pr_id: Optional[int]
    file_path: str
    comments: List[ReviewComment]
    sanitized: bool = False
    original_length: int = 0
