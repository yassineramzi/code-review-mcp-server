# Code Review MCP Server

An MCP-compliant server that performs static analysis on code snippets (e.g., Java, Python) to detect security flaws, bad practices, and optimization opportunities.

---

## 🚀 Quick Start

```bash
git clone https://github.com/yassineramzi/code-review-mcp-server.git
cd code-review-mcp-server
docker build -t mcp-server:latest .
docker run -p 8000:8000 mcp-server:latest
```

The MCP server will be available on port **8000** by default.

---

## 📡 Example Requests
You can explore and test the API interactively using FastAPI Swagger UI:
http://localhost:8000/docs#/default/review_code_review_post

### 1. Health Check

```json
{
  "id": "1",
  "type": "health_check"
}
```

Response:

```json
{
  "id": "1",
  "type": "result",
  "success": true,
  "message": "MCP Server is running"
}
```

---

### 2. Code Review Request

```json
{
  "id": "2",
  "type": "analyze_code",
  "params": {
    "language": "java",
    "code": "import java.io.File; import com.amazonaws.services.s3.*; public class Example { public void upload(String bucket) { AmazonS3 s3 = AmazonS3ClientBuilder.defaultClient(); s3.createBucket(bucket); } }"
  }
}
```

Response:

```json
{
  "id": "2",
  "type": "result",
  "success": true,
  "findings": [
    {
      "severity": "HIGH",
      "issue": "Unvalidated bucket name passed to S3.createBucket()",
      "recommendation": "Validate and sanitize user input before bucket creation."
    },
    {
      "severity": "MEDIUM",
      "issue": "AWS client instantiation without custom configuration.",
      "recommendation": "Use least-privilege IAM roles and explicit configuration."
    }
  ]
}
```

👉 Full details and system design explanation: [Medium article](https://medium.com/@yassine.ramzi2010/building-an-ai-powered-code-reviewer-with-mcp-part-2-system-design-implementation-752a020689fe)
