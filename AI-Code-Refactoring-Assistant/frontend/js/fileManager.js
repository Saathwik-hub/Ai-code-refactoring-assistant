/* File Upload & Explorer Manager for AI Code Refactoring Assistant */

const ALLOWED_EXTENSIONS = ['.py', '.java', '.js', '.ts', '.cpp', '.c', '.html', '.css', '.json'];
const MAX_FILE_SIZE_MB = 5;

class FileManager {
  constructor() {
    this.files = [];
    this.activeFileId = null;
  }

  init() {
    this.initDragAndDrop();
    this.initFileInput();
    this.initCreateFileBtn();
    this.loadFileList();
  }

  async loadFileList() {
    try {
      const fileList = await API.listFiles();
      this.files = fileList;
    } catch (err) {
      // Local demo storage fallback
      const cached = localStorage.getItem('demo_files');
      if (cached) {
        this.files = JSON.parse(cached);
      } else {
        this.files = [
          {
            id: 'file_demo_py',
            filename: 'demo_algorithm.py',
            original_name: 'demo_algorithm.py',
            extension: '.py',
            language: 'python',
            size_bytes: 482,
            uploaded_at: new Date().toISOString(),
            content: `# AI Code Refactoring Assistant - Python Workspace
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

if __name__ == "__main__":
    sample_data = [3, 6, 8, 10, 1, 2, 1]
    sorted_data = quick_sort(sample_data)
    print("Sorted Output:", sorted_data)
`
          },
          {
            id: 'file_demo_js',
            filename: 'app_logic.js',
            original_name: 'app_logic.js',
            extension: '.js',
            language: 'javascript',
            size_bytes: 360,
            uploaded_at: new Date().toISOString(),
            content: `// Developer Assistant JS Demo
function calculateStats(items) {
    if (!Array.isArray(items)) {
        throw new Error("Invalid input: expected array");
    }
    const total = items.reduce((acc, curr) => acc + curr, 0);
    const average = total / items.length;
    return { total, average, count: items.length };
}

console.log(calculateStats([10, 20, 30, 40, 50]));
`
          },
          {
            id: 'file_demo_json',
            filename: 'config.json',
            original_name: 'config.json',
            extension: '.json',
            language: 'json',
            size_bytes: 220,
            uploaded_at: new Date().toISOString(),
            content: `{
  "appName": "AI Code Refactoring Assistant",
  "version": "1.0.0-MVP",
  "theme": "dark",
  "autoSave": true,
  "maxUploadSizeMB": 5
}`
          }
        ];
        localStorage.setItem('demo_files', JSON.stringify(this.files));
      }
    }

    this.renderExplorerSidebar();
    this.renderDashboardTable();
    this.renderDashboardStats();
  }

  renderExplorerSidebar() {
    const listElem = document.getElementById('explorer-file-list');
    if (!listElem) return;

    if (this.files.length === 0) {
      listElem.innerHTML = `<li style="padding: 1rem; color: var(--text-muted); font-size: 0.85rem; text-align: center;">No files uploaded yet</li>`;
      return;
    }

    listElem.innerHTML = this.files.map(f => `
      <li class="file-item ${f.id === this.activeFileId ? 'active' : ''}" data-id="${f.id}">
        <span class="file-item-name">
          <span>${getFileIcon(f.extension)}</span>
          <span>${f.filename}</span>
        </span>
        <span class="file-actions-hover">
          <button title="Rename File" onclick="fileManager.renameFilePrompt('${f.id}')" class="explorer-btn">✏️</button>
          <button title="Delete File" onclick="fileManager.deleteFilePrompt('${f.id}')" class="explorer-btn">🗑️</button>
        </span>
      </li>
    `).join('');

    // Add click event to open file in editor
    listElem.querySelectorAll('.file-item').forEach(item => {
      item.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON') return;
        const id = item.getAttribute('data-id');
        this.openFileInEditor(id);
      });
    });
  }

  renderDashboardTable() {
    const tableBody = document.getElementById('dashboard-recent-files');
    if (!tableBody) return;

    if (this.files.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">No files found. Click "Upload File" or "New Project" to start.</td></tr>`;
      return;
    }

    tableBody.innerHTML = this.files.map(f => {
      const dateStr = new Date(f.uploaded_at).toLocaleDateString();
      const kbStr = (f.size_bytes / 1024).toFixed(1) + ' KB';
      return `
        <tr>
          <td>
            <div style="display: flex; align-items: center; gap: 0.6rem; font-weight: 600;">
              <span>${getFileIcon(f.extension)}</span>
              <span>${f.filename}</span>
            </div>
          </td>
          <td><span class="lang-badge ${f.language}">${f.language}</span></td>
          <td>${kbStr}</td>
          <td>${dateStr}</td>
          <td>
            <button onclick="fileManager.openFileInEditorRedirect('${f.id}')" class="btn btn-secondary" style="padding: 0.25rem 0.6rem; font-size: 0.8rem;">Open in Editor</button>
            <button onclick="fileManager.deleteFilePrompt('${f.id}')" class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.8rem; color: var(--danger-red);">Delete</button>
          </td>
        </tr>
      `;
    }).join('');
  }

  renderDashboardStats() {
    const totalFilesElem = document.getElementById('stat-total-files');
    const totalLinesElem = document.getElementById('stat-total-lines');
    const validatedFilesElem = document.getElementById('stat-validated-files');
    const primaryLangElem = document.getElementById('stat-primary-lang');

    if (totalFilesElem) totalFilesElem.innerText = this.files.length;
    
    let totalLines = 0;
    const langCounts = {};

    this.files.forEach(f => {
      if (f.content) {
        totalLines += f.content.split('\n').length;
      }
      langCounts[f.language] = (langCounts[f.language] || 0) + 1;
    });

    if (totalLinesElem) totalLinesElem.innerText = totalLines;
    if (validatedFilesElem) validatedFilesElem.innerText = this.files.length;

    let primary = 'Python';
    let max = 0;
    for (const [lang, count] of Object.entries(langCounts)) {
      if (count > max) {
        max = count;
        primary = lang.toUpperCase();
      }
    }
    if (primaryLangElem) primaryLangElem.innerText = primary;
  }

  async openFileInEditor(fileId) {
    this.activeFileId = fileId;
    this.renderExplorerSidebar();

    const file = this.files.find(f => f.id === fileId);
    if (!file) return;

    if (window.editorManager) {
      window.editorManager.setCode(file.content || '', file.filename, file.language);
      App.showToast(`Opened '${file.filename}'`, 'info');
    }
  }

  openFileInEditorRedirect(fileId) {
    localStorage.setItem('open_file_id', fileId);
    window.location.href = 'editor.html';
  }

  validateFileObj(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      App.showToast(`Unsupported file extension '${ext}'. Supported: ${ALLOWED_EXTENSIONS.join(', ')}`, 'danger');
      return false;
    }
    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      App.showToast(`File size exceeds limit of ${MAX_FILE_SIZE_MB}MB`, 'danger');
      return false;
    }
    return true;
  }

  async processUploadFile(file) {
    if (!this.validateFileObj(file)) return;

    try {
      const uploadedMeta = await API.uploadFile(file);
      App.showToast(`Successfully uploaded '${file.name}'!`, 'success');
      await this.loadFileList();
      if (window.location.pathname.includes('editor.html')) {
        this.openFileInEditor(uploadedMeta.id);
      }
    } catch (err) {
      // Local fallback file reader
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        const extMap = { '.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.html': 'html', '.css': 'css', '.json': 'json' };
        
        const newFile = {
          id: 'file_' + Math.random().toString(36).substr(2, 8),
          filename: file.name,
          original_name: file.name,
          extension: ext,
          language: extMap[ext] || 'plaintext',
          size_bytes: file.size,
          uploaded_at: new Date().toISOString(),
          content: content
        };

        this.files.unshift(newFile);
        localStorage.setItem('demo_files', JSON.stringify(this.files));
        App.showToast(`Uploaded '${file.name}' (Local Session)`, 'success');
        this.renderExplorerSidebar();
        this.renderDashboardTable();
        this.renderDashboardStats();
        if (window.location.pathname.includes('editor.html')) {
          this.openFileInEditor(newFile.id);
        }
      };
      reader.readAsText(file);
    }
  }

  initDragAndDrop() {
    const dropzone = document.getElementById('upload-dropzone');
    if (!dropzone) return;

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
      }, false);
    });

    dropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        this.processUploadFile(files[0]);
      }
    });

    dropzone.addEventListener('click', () => {
      const input = document.getElementById('hidden-file-input');
      if (input) input.click();
    });
  }

  initFileInput() {
    const input = document.getElementById('hidden-file-input');
    if (input) {
      input.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
          this.processUploadFile(e.target.files[0]);
        }
      });
    }
  }

  initCreateFileBtn() {
    const createBtn = document.getElementById('btn-create-file');
    if (createBtn) {
      createBtn.addEventListener('click', () => {
        const name = prompt("Enter new filename (e.g. script.py, main.js, index.html):", "new_script.py");
        if (name && name.trim()) {
          this.createNewFile(name.trim());
        }
      });
    }
  }

  async createNewFile(filename) {
    const ext = '.' + filename.split('.').pop().toLowerCase();
    const extMap = { '.py': 'python', '.js': 'javascript', '.ts': 'typescript', '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.html': 'html', '.css': 'css', '.json': 'json' };
    const lang = extMap[ext] || 'python';

    const defaultContent = `# ${filename}\n# Created with AI Code Refactoring Assistant\n`;

    try {
      const res = await API.createFile(filename, lang, defaultContent);
      App.showToast(`Created file '${filename}'`, 'success');
      await this.loadFileList();
      this.openFileInEditor(res.id);
    } catch (e) {
      const newFile = {
        id: 'file_' + Math.random().toString(36).substr(2, 8),
        filename: filename,
        original_name: filename,
        extension: ext,
        language: lang,
        size_bytes: defaultContent.length,
        uploaded_at: new Date().toISOString(),
        content: defaultContent
      };
      this.files.unshift(newFile);
      localStorage.setItem('demo_files', JSON.stringify(this.files));
      App.showToast(`Created file '${filename}'`, 'success');
      this.renderExplorerSidebar();
      this.renderDashboardTable();
      this.renderDashboardStats();
      this.openFileInEditor(newFile.id);
    }
  }

  async renameFilePrompt(fileId) {
    const target = this.files.find(f => f.id === fileId);
    if (!target) return;
    const newName = prompt(`Rename '${target.filename}' to:`, target.filename);
    if (newName && newName.trim() && newName !== target.filename) {
      try {
        await API.renameFile(fileId, newName.trim());
        App.showToast(`Renamed to '${newName}'`, 'success');
        await this.loadFileList();
      } catch (e) {
        target.filename = newName.trim();
        target.extension = '.' + newName.split('.').pop().toLowerCase();
        localStorage.setItem('demo_files', JSON.stringify(this.files));
        App.showToast(`Renamed file to '${newName}'`, 'success');
        this.renderExplorerSidebar();
        this.renderDashboardTable();
      }
    }
  }

  async deleteFilePrompt(fileId) {
    const target = this.files.find(f => f.id === fileId);
    if (!target) return;
    if (confirm(`Are you sure you want to delete '${target.filename}'?`)) {
      try {
        await API.deleteFile(fileId);
        App.showToast(`Deleted '${target.filename}'`, 'info');
        await this.loadFileList();
      } catch (e) {
        this.files = this.files.filter(f => f.id !== fileId);
        localStorage.setItem('demo_files', JSON.stringify(this.files));
        App.showToast(`Deleted '${target.filename}'`, 'info');
        this.renderExplorerSidebar();
        this.renderDashboardTable();
        this.renderDashboardStats();
      }
    }
  }
}

function getFileIcon(ext) {
  switch (ext ? ext.toLowerCase() : '') {
    case '.py': return '🐍';
    case '.js': return '🟨';
    case '.ts': return '🟦';
    case '.java': return '☕';
    case '.cpp': case '.c': return '⚙️';
    case '.html': return '🌐';
    case '.css': return '🎨';
    case '.json': return '📋';
    default: return '📄';
  }
}

const fileManager = new FileManager();
document.addEventListener('DOMContentLoaded', () => fileManager.init());
