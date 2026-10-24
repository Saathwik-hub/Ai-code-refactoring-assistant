# AI Code Refactoring Assistant - Phase 1 (MVP)

A web-based developer tool designed to assist programmers in managing, validating, editing, and preparing source code for AI-powered refactoring.

Phase 1 delivers a developer-centric user interface inspired by Visual Studio Code, GitHub, and JetBrains IDEs, built on a modular FastAPI backend architecture.

---

## 🚀 Features Implemented (Phase 1 MVP)

1. **Landing Page**:
   - Modern hero section with call-to-action buttons.
   - Core features grid, benefits comparison, technology stack badges.
   - Responsive navigation bar with theme toggle.

2. **Simple Authentication System**:
   - Register and Login forms with validation.
   - Password visibility toggle (show/hide password).
   - Session storage handling with redirection to Dashboard.

3. **Developer Dashboard**:
   - Welcome banner with user profile integration.
   - Repository & code metrics grid (Total Files, Total Lines of Code, Validated Snippets, Primary Language).
   - Drag-and-drop file upload zone.
   - Recent files table with language badges, size, date, open in editor, and delete options.
   - System activity timeline.

4. **Monaco Code Editor Workspace**:
   - Integrated Visual Studio Code Monaco Editor via AMD loader.
   - Syntax highlighting, auto-indentation, line numbers, code folding, theme switching (`vs-dark` and `vs-light`), and Monaco built-in autocomplete.
   - Language selector dropdown for manual language override.

5. **Drag & Drop File Upload**:
   - Drag-and-drop zone and file browser file picker.
   - Supported extensions: `.py`, `.java`, `.js`, `.ts`, `.cpp`, `.c`, `.html`, `.css`, `.json`.
   - File size validation (5 MB limit) and unsupported file format detection alerts.

6. **Automated Language Detection**:
   - Heuristics engine detecting languages automatically based on file extensions or code keyword patterns (`def`, `function`, `public class`, `#include`, `<!DOCTYPE html>`, etc.).

7. **Multi-Language Syntax Validation Engine**:
   - Python AST syntax validator (`ast.parse`).
   - JSON parsing validator (`json.loads`).
   - JS, TS, C, C++, Java, HTML, CSS bracket and delimiter balance checkers.
   - Bottom diagnostics panel rendering error counts, warning counts, line/column numbers, diagnostic messages, and statusbar indicators.

8. **Sidebar File Explorer**:
   - Tree view of uploaded files.
   - Open file in Monaco editor, create new file, rename file, delete file, download code snippet.

9. **Theme Support**:
   - Dark theme default with curated HSL developer tokens (`#0d1117`, `#161b22`, primary blue `#3b82f6`, accent purple `#8b5cf6`).
   - Light theme with persistence in `localStorage`.

10. **Modular FastAPI Backend Architecture**:
    - Clean separation into `routes/`, `controllers/`, `models/`, `utils/`, and `uploads/`.
    - Ready for Phase 2 AI LLM/Ollama integrations.

---

## 📁 Project Structure

```
AI-Code-Refactoring-Assistant/
├── frontend/
│   ├── index.html         # Landing Page
│   ├── login.html         # Login Page
│   ├── register.html      # Register Page
│   ├── dashboard.html     # Developer Dashboard
│   ├── editor.html        # Monaco Code Editor & File Explorer Workspace
│   ├── profile.html       # User Profile Page
│   ├── settings.html      # Settings & Preferences Page
│   ├── about.html         # About & Phase 2 AI Roadmap
│   ├── css/
│   │   ├── main.css       # Global design system & theme tokens
│   │   ├── editor.css     # Monaco & diagnostics panel layout
│   │   └── dashboard.css  # Stats grid, file tables, drag-drop styling
│   ├── js/
│   │   ├── api.js         # FastAPI backend HTTP client wrapper
│   │   ├── auth.js        # Auth logic, form validation, password toggle
│   │   ├── app.js         # Theme switching, notifications, mobile menu
│   │   ├── editor.js      # Monaco Editor setup, syntax diagnostics
│   │   └── fileManager.js # Drag-and-drop upload, file explorer tree
│   ├── images/
│   └── assets/
├── backend/
│   ├── app.py             # FastAPI entrypoint & static mounting
│   ├── routes/
│   │   ├── auth.py        # Authentication API endpoints
│   │   ├── files.py       # Upload, create, list, rename, delete API endpoints
│   │   └── syntax.py      # Language detection & syntax validation endpoints
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── file_controller.py
│   │   └── syntax_controller.py
│   ├── models/
│   │   ├── user.py        # Auth Pydantic schemas
│   │   └── file_model.py  # File metadata & syntax diagnostic schemas
│   ├── utils/
│   │   ├── file_utils.py  # Extension mapper & size validator
│   │   └── syntax_checker.py # Python AST & multi-language syntax checker
│   └── uploads/           # Local file storage
├── README.md              # Documentation
└── requirements.txt       # Dependencies
```

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3 (Vanilla CSS Design System), JavaScript (ES6+), Monaco Editor (VS Code Engine CDN).
- **Backend**: Python 3.11, FastAPI, Uvicorn, Python-Multipart, Pydantic.
- **Storage**: Local File Storage in `backend/uploads/`.

---

## ⚡ How to Run the Application

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Launch the FastAPI Server
Start the backend server using Uvicorn:
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Open in Browser
Open your browser and navigate to:
```
http://127.0.0.1:8000
```
- Landing Page: `http://127.0.0.1:8000`
- Dashboard: `http://127.0.0.1:8000/static/dashboard.html`
- Code Editor: `http://127.0.0.1:8000/static/editor.html`

Alternatively, the frontend can also be opened directly via file browser or any static HTTP server!

---

## 🔮 Phase 2 AI Integration Roadmap

The application architecture is modularized so future phases can seamlessly integrate:
- **Ollama / LLM Refactoring Engine** (Local Llama 3, DeepSeek-Coder, CodeLlama).
- **Static Code Analysis & Linting**.
- **Cyclomatic Complexity & Maintainability Index Metrics**.
- **Side-by-Side Visual Code Diff Viewer**.
- **In-Editor AI Chat Assistant**.
