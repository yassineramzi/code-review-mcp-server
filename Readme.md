# MCP Code Review Server (MVP)

## Overview
This is a minimal Model Context Protocol (MCP) server MVP that:
- Validates and sanitizes incoming code fragments.
- Runs simple "typed tools" to produce review comments.
- Returns structured JSON responses.

## Run locally (venv)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.server:app --reload --host 0.0.0.0 --port 8000
