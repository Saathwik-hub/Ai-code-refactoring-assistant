# REST API Reference Manual

The **AI Code Refactoring Assistant** provides a comprehensive RESTful API built on FastAPI.

**Base URL**: `http://127.0.0.1:8000`  
**Interactive Swagger UI**: `http://127.0.0.1:8000/docs`  
**ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## 1. System & Health

### `GET /health`
Verifies backend service operational readiness.
- **Response**: `200 OK`
```json
{
  "status": "healthy",
  "phase": "3-AI-Refactoring"
}
```

---

## 2. Syntax & Language Detection

### `POST /api/syntax/validate`
Validates code syntax using AST parsing (Python/JSON) or delimiter balancing (JS, Java, C++, HTML, CSS).
- **Request Body**:
```json
{
  "code": "def add(x, y):\n    return x + y",
  "language": "python"
}
```
- **Response**: `200 OK`
```json
{
  "is_valid": true,
  "language": "python",
  "diagnostics": [],
  "error_count": 0,
  "warning_count": 0,
  "summary": "Python syntax validation passed successfully."
}
```

### `POST /api/syntax/detect`
Automatically detects programming language via file extension or content heuristic analysis.
- **Request Body**:
```json
{
  "filename": "app.js",
  "code": "function calculate() { return 42; }"
}
```
- **Response**: `200 OK`
```json
{
  "detected_language": "javascript",
  "confidence": 0.95
}
```

---

## 3. Static Code Analysis

### `POST /api/analysis/run`
Executes multi-rule static code analysis, cyclomatic complexity measurement, and maintainability grading.
- **Request Body**:
```json
{
  "code": "import os\npassword = '123'\ndef run():\n    eval('2+2')",
  "filename": "security_check.py",
  "language": "python"
}
```
- **Response**: `200 OK`
```json
{
  "id": "report_a1b2c3d4",
  "filename": "security_check.py",
  "language": "python",
  "health_score": 52,
  "grade": "D",
  "total_issues": 2,
  "critical_count": 1,
  "high_count": 1,
  "medium_count": 0,
  "scores": {
    "overall_health": 52.0,
    "grade": "D",
    "maintainability": 50.0,
    "readability": 60.0,
    "security": 45.0,
    "complexity_score": 85.0
  },
  "complexity": {
    "cyclomatic_complexity": 2,
    "nesting_depth": 1,
    "function_count": 1
  },
  "issues": [
    {
      "id": "sec_01",
      "rule_id": "SEC-001",
      "category": "security",
      "severity": "Critical",
      "message": "Hardcoded sensitive credentials/secret detected.",
      "line": 2,
      "column": 1,
      "recommendation": "Store API keys and passwords in environment variables."
    }
  ]
}
```

### `GET /api/analysis/report/{report_id}`
Retrieves a previously computed analysis report by ID.

### `GET /api/analysis/download/{report_id}?format=json|txt`
Downloads the analysis report as formatted JSON or a structured plaintext report.

---

## 4. AI Refactoring & Optimizer

### `POST /api/refactor`
Refactors source code using Ollama (if available) or the local rule-based AST engine with before/after metrics.
- **Request Body**:
```json
{
  "code": "import os\ndef compute():\n    return 42",
  "filename": "main.py",
  "language": "python",
  "mode": "Clean Code",
  "analysis_report_id": null
}
```
- **Response**: `200 OK`
```json
{
  "id": "refactor_e9f8g7h6",
  "filename": "main.py",
  "language": "python",
  "mode": "Clean Code",
  "model_used": "Local AI Engine (Rules & Complexity Optimizer)",
  "original_code": "import os\ndef compute():\n    return 42",
  "refactored_code": "import os\n\ndef compute() -> int:\n    \"\"\"Compute sample result.\"\"\"\n    return 42",
  "explanations": [
    {
      "title": "Clean Code Enhancements",
      "original_snippet": "def compute():",
      "refactored_snippet": "def compute() -> int:",
      "rationale": "Added explicit return type annotations.",
      "principle_used": "PEP 484 Type Hints",
      "trade_off": "None"
    }
  ],
  "metrics_before": { "health_score": 85, "complexity": 1 },
  "metrics_after": { "health_score": 98, "complexity": 1 }
}
```

### `POST /api/optimizer/run`
Analyzes algorithmic time complexity bottlenecks and returns optimized code with estimated speedups.
- **Request Body**:
```json
{
  "code": "def find_common(a, b):\n    return [x for x in a if x in b]",
  "language": "python"
}
```

### `GET /api/optimizer/ollama-status`
Returns Ollama daemon reachability, detected models, and recommended coder models.

### `POST /api/chat`
In-editor AI coding assistant conversation endpoint.
- **Request Body**:
```json
{
  "messages": [{ "role": "user", "content": "How do I optimize this loop?" }],
  "current_code": "for i in range(len(arr)): print(arr[i])",
  "language": "python"
}
```

### `GET /api/ai/history`
Returns a list of all historical refactoring sessions.

---

## 5. File Management

- `GET /api/files`: Returns list of uploaded files.
- `GET /api/files/{id}`: Returns file content and metadata.
- `POST /api/files/upload`: Multipart file upload (5 MB limit).
- `POST /api/files/create`: Create a new file snippet.
- `PUT /api/files/{id}/rename`: Rename a file.
- `DELETE /api/files/{id}`: Delete a file.

---

## 6. Authentication

- `POST /api/auth/register`: Create user account (`username`, `email`, `password`).
- `POST /api/auth/login`: Authenticate and receive session access token.
