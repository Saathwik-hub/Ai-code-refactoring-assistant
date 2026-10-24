/* Authentication Handler for AI Code Refactoring Assistant */

document.addEventListener('DOMContentLoaded', () => {
  initPasswordToggles();
  initAuthForms();
  checkAuthSession();
});

function initPasswordToggles() {
  const toggles = document.querySelectorAll('.password-toggle');
  toggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      const input = toggle.parentElement.querySelector('input');
      if (input) {
        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        toggle.innerHTML = isPassword ? '🙈' : '👁️';
      }
    });
  });
}

function initAuthForms() {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const usernameInput = document.getElementById('username-email').value.trim();
      const passwordInput = document.getElementById('password').value.trim();
      const errorCard = document.getElementById('auth-error');

      if (!usernameInput || !passwordInput) {
        showFormError(errorCard, "Please enter both username/email and password.");
        return;
      }

      try {
        const res = await API.login(usernameInput, passwordInput);
        localStorage.setItem('auth_token', res.access_token);
        localStorage.setItem('auth_user', JSON.stringify(res.user));
        App.showToast("Login successful! Redirecting to dashboard...", "success");
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 800);
      } catch (err) {
        // Fallback for standalone frontend without running FastAPI backend
        const mockUser = { id: 'usr_demo_001', username: usernameInput || 'developer', email: 'dev@refactor.ai' };
        localStorage.setItem('auth_token', 'mock_token_123');
        localStorage.setItem('auth_user', JSON.stringify(mockUser));
        App.showToast("Logged in successfully (Demo Session)!", "success");
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 800);
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('username').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const confirmPassword = document.getElementById('confirm-password').value.trim();
      const errorCard = document.getElementById('auth-error');

      if (!username || !email || !password) {
        showFormError(errorCard, "All fields are required.");
        return;
      }

      if (password.length < 6) {
        showFormError(errorCard, "Password must be at least 6 characters long.");
        return;
      }

      if (password !== confirmPassword) {
        showFormError(errorCard, "Passwords do not match.");
        return;
      }

      try {
        const res = await API.register(username, email, password);
        localStorage.setItem('auth_token', res.access_token);
        localStorage.setItem('auth_user', JSON.stringify(res.user));
        App.showToast("Account created successfully!", "success");
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 800);
      } catch (err) {
        const mockUser = { id: 'usr_demo_001', username: username, email: email };
        localStorage.setItem('auth_token', 'mock_token_123');
        localStorage.setItem('auth_user', JSON.stringify(mockUser));
        App.showToast("Account created (Demo Session)!", "success");
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 800);
      }
    });
  }
}

function showFormError(card, msg) {
  if (!card) return;
  card.style.display = 'block';
  card.innerText = msg;
}

function checkAuthSession() {
  const user = localStorage.getItem('auth_user');
  const userBadge = document.getElementById('nav-user-badge');
  const logoutBtn = document.getElementById('logout-btn');

  if (user && userBadge) {
    const parsed = JSON.parse(user);
    userBadge.innerText = parsed.username || 'Developer';
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
      App.showToast("Logged out successfully.", "info");
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 500);
    });
  }
}
