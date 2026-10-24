/* Monaco Editor Workspace Controller */

class EditorManager {
  constructor() {
    this.editor = null;
    this.currentLanguage = 'python';
    this.currentFile = null;
    this.monacoLoaded = false;
  }

  init() {
    const editorContainer = document.getElementById('monaco-editor-target');
    if (!editorContainer) return;

    // Load Monaco via AMD loader from CDN
    if (typeof require !== 'undefined' && require.config) {
      require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });
      require(['vs/editor/editor.main'], () => {
        this.createEditor(editorContainer);
      });
    } else {
      console.warn("Monaco loader not found, loading script fallback...");
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js';
      script.onload = () => {
        require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });
        require(['vs/editor/editor.main'], () => {
          this.createEditor(editorContainer);
        });
      };
      document.head.appendChild(script);
    }

    this.bindControls();
  }

  createEditor(container) {
    const theme = App.theme === 'dark' ? 'vs-dark' : 'vs-light';
    
    this.editor = monaco.editor.create(container, {
      value: `# AI Code Refactoring Assistant - Python Workspace
def analyze_code(source_code):
    \"\"\"Analyze code structure and return metrics\"\"\"
    lines = source_code.split('\\n')
    non_empty = [l for l in lines if l.strip()]
    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty)
    }

if __name__ == "__main__":
    result = analyze_code("print('Hello Refactor AI')")
    print("Analysis Result:", result)
`,
      language: 'python',
      theme: theme,
      automaticLayout: true,
      fontSize: 14,
      fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
      minimap: { enabled: true },
      lineNumbers: 'on',
      folding: true,
      autoIndent: 'full',
      formatOnPaste: true,
      formatOnType: true,
      tabSize: 4,
      scrollBeyondLastLine: false,
    });

    this.monacoLoaded = true;

    // Track Cursor Position
    this.editor.onDidChangeCursorPosition((e) => {
      const pos = e.position;
      const lineColElem = document.getElementById('status-cursor-pos');
      if (lineColElem) {
        lineColElem.innerText = `Ln ${pos.lineNumber}, Col ${pos.column}`;
      }
    });

    // Code change listener for auto syntax checking (throttled)
    let timer = null;
    this.editor.onDidChangeModelContent(() => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        this.runSyntaxValidation(false);
      }, 1000);
    });

    // Initial syntax check
    this.runSyntaxValidation(false);
  }

  setTheme(themeName) {
    if (this.editor && this.monacoLoaded) {
      monaco.editor.setTheme(themeName);
    }
  }

  setLanguage(lang) {
    this.currentLanguage = lang;
    if (this.editor && this.monacoLoaded) {
      const model = this.editor.getModel();
      monaco.editor.setModelLanguage(model, lang);
    }
    const statusLang = document.getElementById('status-language');
    if (statusLang) {
      statusLang.innerText = lang.toUpperCase();
    }
    const selectElem = document.getElementById('editor-lang-select');
    if (selectElem) {
      selectElem.value = lang;
    }
  }

  setCode(code, filename = null, language = null) {
    if (this.editor && this.monacoLoaded) {
      this.editor.setValue(code);
    }
    if (filename) {
      const titleElem = document.getElementById('active-file-name');
      if (titleElem) titleElem.innerText = filename;
    }
    if (language) {
      this.setLanguage(language);
    } else if (filename) {
      this.autoDetectLanguage(code, filename);
    }
  }

  getCode() {
    return this.editor ? this.editor.getValue() : '';
  }

  async autoDetectLanguage(code, filename = null) {
    try {
      const res = await API.detectLanguage(code, filename);
      if (res && res.detected_language) {
        this.setLanguage(res.detected_language);
        App.showToast(`Auto-detected language: ${res.detected_language.toUpperCase()}`, 'info');
      }
    } catch (e) {
      // Local regex fallback
      const ext = filename ? filename.split('.').pop().toLowerCase() : '';
      const extMap = { py: 'python', js: 'javascript', ts: 'typescript', java: 'java', cpp: 'cpp', c: 'c', html: 'html', css: 'css', json: 'json' };
      if (extMap[ext]) {
        this.setLanguage(extMap[ext]);
      }
    }
  }

  async runSyntaxValidation(showToast = true) {
    const code = this.getCode();
    const lang = this.currentLanguage;
    if (!code.strip && code.trim() === '') return;

    try {
      const result = await API.validateSyntax(code, lang);
      this.renderDiagnostics(result);
      if (showToast) {
        if (result.is_valid) {
          App.showToast(`Syntax Validation Passed (${lang.toUpperCase()})`, 'success');
        } else {
          App.showToast(`Syntax Validation Found ${result.error_count} Error(s)`, 'danger');
        }
      }
    } catch (err) {
      // Local fallback syntax validator
      this.renderLocalDiagnostics(code, lang);
    }
  }

  renderDiagnostics(result) {
    const container = document.getElementById('diagnostics-output-list');
    const badgeErr = document.getElementById('diag-error-count');
    const badgeWarn = document.getElementById('diag-warn-count');
    const statusDiag = document.getElementById('status-diagnostics');

    if (badgeErr) badgeErr.innerText = result.error_count;
    if (badgeWarn) badgeWarn.innerText = result.warning_count;

    if (statusDiag) {
      statusDiag.innerText = result.is_valid ? '✓ Syntax OK' : `❌ ${result.error_count} Error(s)`;
      statusDiag.style.color = result.is_valid ? '#10b981' : '#ef4444';
    }

    if (!container) return;

    if (result.diagnostics.length === 0) {
      container.innerHTML = `
        <div class="diag-item diag-success">
          <span>✅</span> <span>${result.summary} No syntax errors detected.</span>
        </div>
      `;
      return;
    }

    container.innerHTML = result.diagnostics.map(d => `
      <div class="diag-item diag-${d.severity}">
        <span>${d.severity === 'error' ? '❌' : '⚠️'}</span>
        <span>Line ${d.line || 1}${d.column ? `, Col ${d.column}` : ''}: ${d.message}</span>
      </div>
    `).join('');
  }

  renderLocalDiagnostics(code, lang) {
    let errors = [];
    if (lang === 'json') {
      try { JSON.parse(code); }
      catch (e) { errors.push({ line: 1, message: e.message, severity: 'error' }); }
    }
    this.renderDiagnostics({
      is_valid: errors.length === 0,
      language: lang,
      diagnostics: errors,
      error_count: errors.length,
      warning_count: 0,
      summary: errors.length === 0 ? "Syntax OK" : "Syntax error detected"
    });
  }

  bindControls() {
    const langSelect = document.getElementById('editor-lang-select');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        this.setLanguage(e.target.value);
        this.runSyntaxValidation(true);
      });
    }

    const checkSyntaxBtn = document.getElementById('btn-validate-syntax');
    if (checkSyntaxBtn) {
      checkSyntaxBtn.addEventListener('click', () => this.runSyntaxValidation(true));
    }

    const downloadBtn = document.getElementById('btn-download-code');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        const titleElem = document.getElementById('active-file-name');
        const filename = titleElem ? titleElem.innerText : 'snippet.txt';
        const blob = new Blob([this.getCode()], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
        App.showToast(`Downloaded '${filename}'`, 'success');
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('monaco-editor-target')) {
    window.editorManager = new EditorManager();
    window.editorManager.init();
  }
});
