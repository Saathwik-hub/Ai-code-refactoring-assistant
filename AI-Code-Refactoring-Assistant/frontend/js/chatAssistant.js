/* Floating AI Chat Drawer Widget */

(function () {
  const CHAT_HTML = `
  <div class="chat-drawer" id="chatDrawer">
    <div class="chat-drawer-header" id="chatToggle">
      <span>💬 AI Chat Assistant</span>
      <span id="chatToggleIcon">▲</span>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="chat-msg assistant">Hi! I can help with your code. Paste a snippet, ask questions, or request explanations.</div>
    </div>
    <div class="chat-input-row">
      <input type="text" class="chat-input" id="chatInput" placeholder="Ask about code..." />
      <button class="chat-send-btn" id="chatSend">➤</button>
    </div>
  </div>`;

  function init() {
    if (document.getElementById('chatDrawer')) return;
    document.body.insertAdjacentHTML('beforeend', CHAT_HTML);

    const drawer = document.getElementById('chatDrawer');
    const toggle = document.getElementById('chatToggle');
    const icon = document.getElementById('chatToggleIcon');
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSend');

    toggle.addEventListener('click', () => {
      drawer.classList.toggle('open');
      icon.textContent = drawer.classList.contains('open') ? '▼' : '▲';
    });

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') sendMessage();
    });
  }

  function addMessage(content, role) {
    const box = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.textContent = content;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    input.value = '';

    // Gather editor context if available
    let currentCode = '';
    let language = 'python';
    try {
      if (window.monacoEditor) {
        currentCode = window.monacoEditor.getValue();
        const model = window.monacoEditor.getModel();
        if (model) language = model.getLanguageId();
      }
    } catch (e) { /* ignore */ }

    try {
      const messages = [{ role: 'user', content: text }];
      const res = await API.chatWithAI(messages, currentCode, language);
      addMessage(res.reply || res.response || JSON.stringify(res), 'assistant');
    } catch (err) {
      addMessage('⚠️ Error: ' + err.message, 'assistant');
    }
  }

  // Load when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
