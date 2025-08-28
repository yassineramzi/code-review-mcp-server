# Dockerfile - multi-stage, secure, non-root
# ---------- Build stage ----------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # install build deps (if any)
    COPY requirements.txt /app/requirements.txt
    RUN pip --disable-pip-version-check install --no-cache-dir -r requirements.txt
    
    # ---------- Final runtime stage ----------
    FROM python:3.11-slim
    
    # create non-root user/group
    RUN groupadd -r mcp && useradd -r -g mcp mcpuser
    
    WORKDIR /app
    
    # copy minimal runtime artifacts from builder
    COPY --from=builder /usr/local /usr/local
    COPY app ./app
    
    # switch to non-root user
    USER mcpuser
    
    EXPOSE 8000
    
    CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
    