/* Global Application Controller for AI Code Refactoring Assistant */

const App = {
  theme: localStorage.getItem('app_theme') || 'dark',

  init() {
    this.applyTheme(this.theme);
    this.initThemeToggle();
    this.initMobileNav();
    this.createToastContainer();
  },

  applyTheme(newTheme) {
    this.theme = newTheme;
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('app_theme', newTheme);

    const toggleBtn = document.querySelectorAll('.theme-toggle-btn');
    toggleBtn.forEach(btn => {
      btn.innerHTML = newTheme === 'dark' ? '☀️' : '🌙';
      btn.title = newTheme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme';
    });

    // Notify Monaco editor if active
    if (window.editorManager && typeof window.editorManager.setTheme === 'function') {
      window.editorManager.setTheme(newTheme === 'dark' ? 'vs-dark' : 'vs-light');
    }
  },

  toggleTheme() {
    const nextTheme = this.theme === 'dark' ? 'light' : 'dark';
    this.applyTheme(nextTheme);
  },

  initThemeToggle() {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => this.toggleTheme());
    });
  },

  initMobileNav() {
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileBtn && navLinks) {
      mobileBtn.addEventListener('click', () => {
        navLinks.classList.toggle('mobile-open');
      });
    }
  },

  createToastContainer() {
    if (!document.querySelector('.toast-container')) {
      const container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
  },

  showToast(message, type = 'info') {
    this.createToastContainer();
    const container = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'warning') icon = '⚠️';
    if (type === 'danger') icon = '❌';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
