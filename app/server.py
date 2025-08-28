# app/server.py
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .models import CodeReviewRequest
from .compliance import validate_request
from .handlers import analyze_code

app = FastAPI(title="MCP Code Review Server", version="0.1.0")

# configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp.server")


@app.on_event("startup")
async def startup_event():
    logger.info("MCP Code Review Server starting up.")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/review")
async def review_code(request: CodeReviewRequest):
    logger.info("Received review request: repo=%s file=%s pr=%s", request.repo, request.file_path, request.pr_id)
    is_valid, reason = validate_request(request.code)
    if not is_valid:
        logger.warning("Rejected request: %s", reason)
        raise HTTPException(status_code=400, detail=reason)

    # Process
    response = analyze_code(request)
    logger.info("Review completed: comments=%d sanitized=%s", len(response.comments), response.sanitized)
    return JSONResponse(status_code=200, content=response.dict())


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception while handling request: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
