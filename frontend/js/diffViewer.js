/* Side-by-Side Diff Viewer Generator */

class DiffViewer {
  static render(originalCode, refactoredCode, containerId = 'diff-viewer-container') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const origLines = originalCode.split('\n');
    const refLines = refactoredCode.split('\n');
    const maxLen = Math.max(origLines.length, refLines.length);

    let origHTML = '';
    let refHTML = '';
    let additions = 0;
    let deletions = 0;
    let modifications = 0;

    for (let i = 0; i < maxLen; i++) {
      const origLine = origLines[i] !== undefined ? origLines[i] : '';
      const refLine = refLines[i] !== undefined ? refLines[i] : '';
      const lineNum = i + 1;

      if (origLine === refLine) {
        origHTML += DiffViewer._renderLine(lineNum, origLine, 'unchanged');
        refHTML += DiffViewer._renderLine(lineNum, refLine, 'unchanged');
      } else if (origLine && !refLine && i >= refLines.length) {
        origHTML += DiffViewer._renderLine(lineNum, origLine, 'removed');
        refHTML += DiffViewer._renderLine('', '', 'unchanged');
        deletions++;
      } else if (!origLine && refLine && i >= origLines.length) {
        origHTML += DiffViewer._renderLine('', '', 'unchanged');
        refHTML += DiffViewer._renderLine(lineNum, refLine, 'added');
        additions++;
      } else {
        origHTML += DiffViewer._renderLine(lineNum, origLine, 'removed');
        refHTML += DiffViewer._renderLine(lineNum, refLine, 'added');
        modifications++;
      }
    }

    container.innerHTML = `
      <div class="diff-container">
        <div class="diff-pane">
          <div class="diff-pane-header original">📄 Original Code</div>
          ${origHTML}
        </div>
        <div class="diff-pane">
          <div class="diff-pane-header">✨ Refactored Code</div>
          ${refHTML}
        </div>
      </div>
    `;

    // Update summary bar
    const summaryBar = document.getElementById('diff-summary-stats');
    if (summaryBar) {
      summaryBar.innerHTML = `
        <div class="diff-stat additions">+ ${additions + modifications} additions</div>
        <div class="diff-stat deletions">- ${deletions + modifications} deletions</div>
        <div class="diff-stat" style="color: var(--text-muted);">Total Lines Changed: ${additions + deletions + modifications}</div>
      `;
    }
  }

  static _renderLine(num, content, type) {
    const escaped = DiffViewer._escapeHTML(content);
    return `<div class="diff-line diff-line-${type}">
      <span class="diff-line-num">${num}</span>
      <span class="diff-line-content">${escaped}</span>
    </div>`;
  }

  static _escapeHTML(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
}
