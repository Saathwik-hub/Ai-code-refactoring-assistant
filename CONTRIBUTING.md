# Contributing to AI Code Refactoring Assistant

Thank you for your interest in contributing to the **AI Code Refactoring Assistant**! We welcome bug reports, feature suggestions, test coverage additions, and pull requests.

---

## 1. Code of Conduct

Please be respectful, constructive, and collaborative in all discussions and pull requests.

---

## 2. Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Ai-code-refactoring-assistant.git
   cd Ai-code-refactoring-assistant
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the local development server:
   ```bash
   python -m backend.app
   ```
   Open `http://127.0.0.1:8000` in your web browser.

---

## 3. Running Automated Tests

Always run tests before opening a pull request:
```bash
python -m unittest discover tests
```
Ensure all 21+ unit and integration tests pass cleanly with zero errors.

---

## 4. Coding Standards

- **Python**: Follow PEP 8 guidelines. Use type annotations (`typing`) where appropriate.
- **FastAPI**: Keep route handlers lightweight; encapsulate business logic in `controllers/` and `services/`.
- **Frontend**: Maintain vanilla JavaScript (ES6+) and custom CSS tokens without introducing heavy frontend framework dependencies.

---

## 5. Pull Request Guidelines

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit changes with clear, descriptive commit messages:
   ```bash
   git commit -m "feat(analyzer): add cyclomatic threshold alerts"
   ```
3. Push to your fork and submit a Pull Request against `main`.
