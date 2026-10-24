/* ==========================================================================
   AI Code Refactoring Assistant - Backend API Client Wrapper
   ========================================================================== */

const API_BASE_URL = window.location.origin.includes('8000') 
  ? window.location.origin 
  : 'http://127.0.0.1:8000';

class ApiClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = options.headers || {};

    if (!headers['Content-Type'] && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Server returned status ${response.status}`);
      }

      return data;
    } catch (err) {
      console.warn(`[API] Call to ${endpoint} failed, falling back to local client processing where possible.`, err);
      throw err;
    }
  }

  // Auth Endpoints
  async register(username, email, password) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
  }

  async login(username_or_email, password) {
    return this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username_or_email, password })
    });
  }

  // File Endpoints
  async listFiles() {
    return this.request('/api/files', { method: 'GET' });
  }

  async getFile(fileId) {
    return this.request(`/api/files/${fileId}`, { method: 'GET' });
  }

  async uploadFile(fileObj) {
    const formData = new FormData();
    formData.append('file', fileObj);
    return this.request('/api/files/upload', {
      method: 'POST',
      body: formData
    });
  }

  async createFile(filename, language, content) {
    return this.request('/api/files/create', {
      method: 'POST',
      body: JSON.stringify({ filename, language, content })
    });
  }

  async renameFile(fileId, newFilename) {
    return this.request(`/api/files/${fileId}/rename`, {
      method: 'PUT',
      body: JSON.stringify({ new_filename: newFilename })
    });
  }

  async deleteFile(fileId) {
    return this.request(`/api/files/${fileId}`, { method: 'DELETE' });
  }

  // Syntax & Language Endpoints
  async validateSyntax(code, language) {
    return this.request('/api/syntax/validate', {
      method: 'POST',
      body: JSON.stringify({ code, language })
    });
  }

  async detectLanguage(code, filename = null) {
    return this.request('/api/syntax/detect', {
      method: 'POST',
      body: JSON.stringify({ code, filename })
    });
  }

  // ── Phase 2: Static Analysis Endpoints ──
  async runAnalysis(code, filename, language) {
    return this.request('/api/analysis/run', {
      method: 'POST',
      body: JSON.stringify({ code, filename, language })
    });
  }

  async getAnalysisReport(reportId) {
    return this.request(`/api/analysis/report/${reportId}`, { method: 'GET' });
  }

  async downloadAnalysisReport(reportId, format = 'json') {
    const url = `${API_BASE_URL}/api/analysis/download/${reportId}?format=${format}`;
    window.open(url, '_blank');
  }

  // ── Phase 3: AI Refactoring Endpoints ──
  async refactorCode(code, filename, language, mode = 'Clean Code', analysisReportId = null) {
    return this.request('/api/refactor', {
      method: 'POST',
      body: JSON.stringify({ code, filename, language, mode, analysis_report_id: analysisReportId })
    });
  }

  async explainCode(code, language) {
    return this.request('/api/explain', {
      method: 'POST',
      body: JSON.stringify({ code, language })
    });
  }

  async optimizeCode(code, language) {
    return this.request('/api/optimize', {
      method: 'POST',
      body: JSON.stringify({ code, language })
    });
  }

  async chatWithAI(messages, currentCode = '', language = 'python') {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ messages, current_code: currentCode, language })
    });
  }

  async getRefactoringHistory() {
    return this.request('/api/ai/history', { method: 'GET' });
  }

  async getRefactoringSession(sessionId) {
    return this.request(`/api/ai/history/${sessionId}`, { method: 'GET' });
  }
}

const API = new ApiClient();
