/**
 * Code Optimizer & Complexity Reducer Frontend Controller
 */

// Preset code samples for 1-click testing
const PRESETS = {
  "pair-sum": {
    name: "⚡ O(N²) Pair Sum & Search",
    lang: "python",
    code: `def find_target_pairs(numbers, target_sum):
    """Finds all pairs of numbers in a list that add up to target_sum."""
    matching_pairs = []
    
    # Inefficient O(N²) quadratic nested loop
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] + numbers[j] == target_sum:
                matching_pairs.append((numbers[i], numbers[j]))
                
    # Dead code after logic
    return matching_pairs
    print("This line will never be reached")`
  },
  "bubble-sort": {
    name: "🚀 O(N²) Bubble Sort",
    lang: "python",
    code: `def bubble_sort_algorithm(data_list):
    """Sorts a list in ascending order using slow O(N²) bubble sort."""
    n = len(data_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data_list[j] > data_list[j + 1]:
                data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
    return data_list`
  },
  "recursion": {
    name: "🔄 O(2ⁿ) Exponential Fibonacci",
    lang: "python",
    code: `def fibonacci_recursive(n):
    """Calculates n-th Fibonacci number using naive O(2ⁿ) exponential recursion."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Exponential subproblem duplication without memoization
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)`
  },
  "fullstack": {
    name: "🧩 Fullstack Client + Server",
    lang: "javascript",
    code: `<!-- Client-side HTML UI -->
<div id="user-dashboard">
  <h2>User Search Panel</h2>
  <input type="text" id="user-query" placeholder="Search users...">
  <button id="search-btn">Run Search</button>
  <ul id="results-list"></ul>
</div>

<script>
  // Frontend client search handler
  document.getElementById('search-btn').addEventListener('click', async () => {
    const query = document.getElementById('user-query').value;
    const res = await fetch('/api/search?q=' + query);
    const data = await res.json();
    document.getElementById('results-list').innerHTML = data.items.map(i => '<li>' + i.name + '</li>').join('');
  });
</script>

// Backend Service API Router
const express = require('express');
const router = express.Router();

router.get('/api/search', (req, res) => {
  const q = req.query.q || '';
  const users = [{id: 1, name: 'Alice'}, {id: 2, name: 'Bob'}, {id: 3, name: 'Charlie'}];
  
  // Linear search inside endpoint
  const matches = [];
  for (let i = 0; i < users.length; i++) {
    if (users[i].name.toLowerCase().indexOf(q.toLowerCase()) !== -1) {
      matches.push(users[i]);
    }
  }
  res.json({ items: matches, count: matches.length });
});`
  },
  "list-comp": {
    name: "🧹 Verbose Loops & Booleans",
    lang: "python",
    code: `def process_user_records(records):
    # Verbose manual loop building a list
    active_users = []
    for user in records:
        if user.is_active == True:
            active_users.append(user.name)

    # Inefficient empty check and duplicate prints
    if len(active_users) == 0:
        print("No active users found.")
        print("Please check your database connection.")
        print("Operation cancelled.")
        return []

    return active_users`
  },
  "java-duplicates": {
    name: "☕ Java O(N²) Duplicate Finder",
    lang: "java",
    code: `import java.util.Scanner;

public class ComplexProgram {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter array size: ");
        int n = sc.nextInt();
        int[] arr = new int[n];

        System.out.println("Enter array elements:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        // Find duplicate elements - Inefficient quadratic O(n²) nested loop
        System.out.println("\\nDuplicate elements:");
        for (int i = 0; i < n; i++) {
            int count = 0;
            for (int j = 0; j < n; j++) {
                if (arr[i] == arr[j]) {
                    count++;
                }
            }
        }
    }
}`
  }
};

let currentOptimizationResult = null;

document.addEventListener("DOMContentLoaded", () => {
  initPresets();
  setupEventListeners();
  loadPreset("java-duplicates");
  checkOllamaConnection();
});

function initPresets() {
  const container = document.getElementById("presets-list");
  if (!container) return;

  container.innerHTML = "";
  Object.keys(PRESETS).forEach(key => {
    const p = PRESETS[key];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "preset-chip";
    btn.innerHTML = `<span>${p.name}</span>`;
    btn.onclick = () => loadPreset(key);
    container.appendChild(btn);
  });
}

function loadPreset(key) {
  const p = PRESETS[key];
  if (!p) return;

  const codeArea = document.getElementById("optimizer-input");
  const langSelect = document.getElementById("optimizer-lang");

  if (codeArea) codeArea.value = p.code;
  if (langSelect) langSelect.value = p.lang;
}

function setupEventListeners() {
  const runBtn = document.getElementById("btn-run-optimizer");
  if (runBtn) {
    runBtn.addEventListener("click", runCodeOptimizer);
  }

  const refreshOllamaBtn = document.getElementById("btn-refresh-ollama");
  if (refreshOllamaBtn) {
    refreshOllamaBtn.addEventListener("click", () => {
      checkOllamaConnection(true);
    });
  }

  const clearBtn = document.getElementById("btn-clear-optimizer");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      const codeArea = document.getElementById("optimizer-input");
      if (codeArea) codeArea.value = "";
      hideResults();
    });
  }

  // Tab switching
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const targetTab = btn.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });

  // Copy buttons
  setupCopyBtn("btn-copy-optimized", () => currentOptimizationResult ? currentOptimizationResult.optimized_code : "");
  setupCopyBtn("btn-copy-frontend", () => currentOptimizationResult ? currentOptimizationResult.frontend_code : "");
  setupCopyBtn("btn-copy-backend", () => currentOptimizationResult ? currentOptimizationResult.backend_code : "");

  // Download buttons
  setupDownloadBtn("btn-download-optimized", () => currentOptimizationResult ? currentOptimizationResult.optimized_code : "", () => getFilenameForLang("optimized"));
  setupDownloadBtn("btn-download-frontend", () => currentOptimizationResult ? currentOptimizationResult.frontend_code : "", () => "frontend_app.html");
  setupDownloadBtn("btn-download-backend", () => currentOptimizationResult ? currentOptimizationResult.backend_code : "", () => getFilenameForLang("backend_service"));

  // Send to Editor
  const sendEditorBtn = document.getElementById("btn-send-to-editor");
  if (sendEditorBtn) {
    sendEditorBtn.addEventListener("click", () => {
      if (!currentOptimizationResult) return;
      localStorage.setItem("editor_imported_code", currentOptimizationResult.optimized_code);
      localStorage.setItem("editor_imported_lang", currentOptimizationResult.language);
      window.location.href = "editor.html";
    });
  }
}

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(b => {
    b.classList.toggle("active", b.getAttribute("data-tab") === tabId);
  });
  document.querySelectorAll(".tab-content-pane").forEach(pane => {
    pane.classList.toggle("active", pane.id === `pane-${tabId}`);
  });
}

async function checkOllamaConnection(notify = false) {
  const dot = document.getElementById("ollama-status-dot");
  const label = document.getElementById("ollama-status-label");
  const sub = document.getElementById("ollama-status-sub");
  const modelSelect = document.getElementById("optimizer-model");
  if (!dot || !label) return;

  dot.style.background = "#eab308";
  label.textContent = "Ollama: Connecting...";
  if (sub) sub.textContent = "Querying local Ollama server...";

  try {
    const baseUrl = (typeof API_BASE_URL !== 'undefined')
      ? API_BASE_URL
      : (window.location.origin.includes('8000') ? window.location.origin : 'http://127.0.0.1:8000');

    const appSettings = JSON.parse(localStorage.getItem('app_settings') || '{}');
    const endpointParam = appSettings.ollamaUrl ? `?url=${encodeURIComponent(appSettings.ollamaUrl)}` : '';

    const res = await fetch(`${baseUrl}/api/optimizer/ollama-status${endpointParam}`);
    if (res.ok) {
      const data = await res.json();
      if (data.available) {
        dot.style.background = "#10b981";
        const best = data.best_model || "Connected";
        label.textContent = `Ollama: Online (${best})`;
        if (sub) sub.textContent = `${data.models.length} model(s) available at ${data.endpoint}`;

        if (modelSelect && data.models && data.models.length > 0) {
          modelSelect.innerHTML = "";
          const autoOpt = document.createElement("option");
          autoOpt.value = "auto";
          autoOpt.textContent = `Auto-Detect (${best})`;
          modelSelect.appendChild(autoOpt);

          data.models.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m;
            opt.textContent = m;
            if (m === data.best_model) opt.selected = true;
            modelSelect.appendChild(opt);
          });
        }
        if (notify && typeof App !== 'undefined') {
          App.showToast("Ollama connected successfully!", "success");
        }
        return;
      }
    }
  } catch (err) {
    console.debug("Ollama check err:", err);
  }

  dot.style.background = "#f59e0b";
  label.textContent = "Ollama: Offline (Smart Engine Active)";
  if (sub) sub.textContent = "Deterministic Algorithmic Engine will optimize your code";
  if (notify && typeof App !== 'undefined') {
    App.showToast("Ollama not responding. Using local Algorithmic Optimizer Engine.", "info");
  }
}

async function runCodeOptimizer() {
  const codeArea = document.getElementById("optimizer-input");
  const langSelect = document.getElementById("optimizer-lang");
  const modelSelect = document.getElementById("optimizer-model");
  const runBtn = document.getElementById("btn-run-optimizer");

  const code = codeArea ? codeArea.value.trim() : "";
  const language = langSelect ? langSelect.value : "python";
  const chosenModel = modelSelect ? modelSelect.value : "auto";

  if (!code) {
    alert("Please enter or paste code to optimize.");
    return;
  }

  const origBtnText = runBtn.innerHTML;
  runBtn.innerHTML = `<span>⏳ Optimizing & Reducing Complexity...</span>`;
  runBtn.disabled = true;

  try {
    const baseUrl = (typeof API_BASE_URL !== 'undefined')
      ? API_BASE_URL
      : (window.location.origin.includes('8000') ? window.location.origin : 'http://127.0.0.1:8000');

    const appSettings = JSON.parse(localStorage.getItem('app_settings') || '{}');
    const ollamaUrl = appSettings.ollamaUrl || null;

    const res = await fetch(`${baseUrl}/api/optimizer/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        language,
        model: chosenModel === "auto" ? null : chosenModel,
        ollama_url: ollamaUrl
      })
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw new Error(errBody.detail || "Optimization failed");
    }

    const data = await res.json();
    currentOptimizationResult = data;
    renderResults(data);
  } catch (err) {
    console.warn("Backend optimizer unavailable, using client-side engine:", err.message);
    try {
      const data = clientSideOptimize(code, language);
      currentOptimizationResult = data;
      renderResults(data);
    } catch (fallbackErr) {
      console.error("Client-side optimizer error:", fallbackErr);
      alert("Error optimizing code: " + fallbackErr.message);
    }
  } finally {
    runBtn.innerHTML = origBtnText;
    runBtn.disabled = false;
  }
}

// ══════════════════════════════════════════════════════════════════════
// CLIENT-SIDE OPTIMIZER ENGINE (works without backend)
// ══════════════════════════════════════════════════════════════════════

function clientSideOptimize(code, language) {
  const lang = language.toLowerCase();
  let optimized = code;
  let changes = [];

  if (lang === "python" || lang === "py") {
    ({ optimized, changes } = optimizePython(code));
  } else if (["javascript", "js", "typescript", "ts"].includes(lang)) {
    ({ optimized, changes } = optimizeJS(code));
  } else if (lang === "java") {
    ({ optimized, changes } = optimizeJava(code));
  } else if (["c", "cpp", "c++"].includes(lang)) {
    ({ optimized, changes } = optimizeCpp(code));
  } else {
    ({ optimized, changes } = optimizeGeneric(code));
  }

  const complexityBefore = estimateComplexity(code);
  const complexityAfter = estimateComplexity(optimized);

  const linesBefore = code.split("\n").filter(l => l.trim()).length;
  const linesAfter = optimized.split("\n").filter(l => l.trim()).length;
  const reduction = linesBefore - linesAfter;
  const pct = Math.round((reduction / Math.max(linesBefore, 1)) * 100);

  const summaryParts = [];
  if (complexityBefore !== complexityAfter) summaryParts.push(`Time complexity reduced from ${complexityBefore} to ${complexityAfter}`);
  if (reduction > 0) summaryParts.push(`Code reduced by ${reduction} lines (${pct}% smaller)`);
  if (changes.length > 0) summaryParts.push(`${changes.length} optimization(s) applied`);
  if (!summaryParts.length) summaryParts.push("Code is already clean and optimal");

  const speedup = calculateSpeedup(complexityBefore, complexityAfter);

  return {
    id: "opt_client_" + Date.now().toString(36),
    original_code: code,
    optimized_code: optimized,
    frontend_code: null,
    backend_code: null,
    speedup_estimate: speedup,
    separation_note: null,
    language: lang,
    changes,
    complexity_before: complexityBefore,
    complexity_after: complexityAfter,
    lines_before: linesBefore,
    lines_after: linesAfter,
    summary: summaryParts.join(". ") + ".",
    created_at: new Date().toISOString()
  };
}

// ── Python Optimizer ─────────────────────────────────────────────────

function optimizePython(code) {
  const lines = code.split("\n");
  const resultLines = [];
  const changes = [];
  let i = 0;
  let skipUntil = -1;

  while (i < lines.length) {
    if (i < skipUntil) { i++; continue; }
    const line = lines[i];
    const stripped = line.trim();
    const indent = line.substring(0, line.length - line.trimStart().length);

    // ── Pattern 1: Nested loop pair search → hash map ──────────────
    if (/^for\s+\w+\s+in\s+range\(/.test(stripped)) {
      const blockEnd = findBlockEnd(lines, i);
      const block = lines.slice(i, blockEnd).join("\n");

      // Detect pair-sum pattern: for i ... for j ... if arr[i] + arr[j] == target
      const pairMatch = block.match(
        /for\s+(\w+)\s+in\s+range\(\s*len\((\w+)\).*?\):\s*\n\s+for\s+(\w+)\s+in\s+range\(.*?\):\s*\n\s+if\s+\1\s*!=\s*\3\s+and\s+\2\[\1\]\s*\+\s*\2\[\3\]\s*==\s*(\w+):\s*\n\s+(\w+)\.append\((.*?)\)/s
      );
      if (pairMatch) {
        const [, , arr, , target, resList] = pairMatch;
        resultLines.push(`${indent}# Optimized to O(n) using Hash Map complement lookup`);
        resultLines.push(`${indent}seen = {}`);
        resultLines.push(`${indent}for num in ${arr}:`);
        resultLines.push(`${indent}    diff = ${target} - num`);
        resultLines.push(`${indent}    if diff in seen:`);
        resultLines.push(`${indent}        ${resList}.append((diff, num))`);
        resultLines.push(`${indent}    seen[num] = True`);
        changes.push({
          title: "Nested Loop → Hash Map Lookup",
          before: "O(n²) nested loop pair-sum search",
          after: "O(n) hash map complement lookup",
          description: `Replaced O(n²) double loop searching ${arr} with O(n) single-pass hash map lookup.`
        });
        i = blockEnd;
        continue;
      }

      // Detect duplicate finder: for i... for j... if arr[i] == arr[j]
      const dupMatch = block.match(
        /for\s+(\w+)\s+in\s+range\(\s*len\((\w+)\).*?\):\s*\n\s+for\s+(\w+)\s+in\s+range\(.*?\):\s*\n\s+if\s+.*?\2\[\1\]\s*==\s*\2\[\3\]/s
      );
      if (dupMatch) {
        const arr = dupMatch[2];
        resultLines.push(`${indent}# O(n) duplicate detection via Set`);
        resultLines.push(`${indent}seen = set()`);
        resultLines.push(`${indent}duplicates = set()`);
        resultLines.push(`${indent}for x in ${arr}:`);
        resultLines.push(`${indent}    if x in seen:`);
        resultLines.push(`${indent}        duplicates.add(x)`);
        resultLines.push(`${indent}    seen.add(x)`);
        changes.push({
          title: "Nested Loop → Set Lookup",
          before: "O(n²) nested loop duplicate finder",
          after: "O(n) set-based duplicate detection",
          description: "Replaced O(n²) nested loop duplicate search with O(n) Set tracking."
        });
        i = blockEnd;
        continue;
      }
    }

    // ── Pattern 1b: Bubble sort → sorted() ──────────────────────────
    if (stripped.startsWith("def ") && (/bubble/i.test(stripped) || isBubbleSortBlock(lines, i))) {
      const blockEnd = findBlockEnd(lines, i);
      const block = lines.slice(i, blockEnd).join("\n");
      if (looksLikeBubbleSort(block)) {
        const fnMatch = stripped.match(/def\s+(\w+)\s*\((\w+)\)/);
        if (fnMatch) {
          resultLines.push(`${indent}def ${fnMatch[1]}(${fnMatch[2]}):`);
          resultLines.push(`${indent}    return sorted(${fnMatch[2]})`);
          changes.push({
            title: "Bubble Sort → Built-in sorted()",
            before: "O(n²) bubble sort implementation",
            after: "O(n log n) Timsort via sorted()",
            description: "Replaced manual bubble sort with Python's optimized built-in sorted() using Timsort."
          });
          i = blockEnd;
          continue;
        }
      }
    }

    // ── Pattern 2: Exponential recursion → memoization ──────────────
    if (stripped.startsWith("def ") && (/fib|recur|calc/i.test(stripped))) {
      const blockEnd = findBlockEnd(lines, i);
      const block = lines.slice(i, blockEnd).join("\n");
      const fnNameMatch = stripped.match(/def\s+(\w+)/);
      if (fnNameMatch) {
        const fnName = fnNameMatch[1];
        const callCount = (block.match(new RegExp(`${fnName}\\(`, 'g')) || []).length;
        if (callCount >= 2) {
          // Check if lru_cache already exists
          if (!resultLines.some(l => l.trim() === "from functools import lru_cache")) {
            resultLines.push(`${indent}from functools import lru_cache`);
            resultLines.push("");
          }
          resultLines.push(`${indent}@lru_cache(maxsize=None)`);
          // Push the function as-is
          for (let k = i; k < blockEnd; k++) {
            resultLines.push(lines[k]);
          }
          changes.push({
            title: "Exponential Recursion → Memoized O(n)",
            before: "O(2ⁿ) naive exponential recursion",
            after: "O(n) memoized recursion via @lru_cache",
            description: `Added @lru_cache memoization to '${fnName}', converting exponential time to linear O(n).`
          });
          i = blockEnd;
          continue;
        }
      }
    }

    // ── Pattern 3: Manual list build → list comprehension ───────────
    if (/^\w+\s*=\s*\[\]$/.test(stripped) && i + 2 < lines.length) {
      const varName = stripped.split("=")[0].trim();
      const nextLine = lines[i + 1] ? lines[i + 1].trim() : "";
      const forMatch = nextLine.match(/^for\s+(\w+)\s+in\s+(.+)\s*:$/);
      if (forMatch) {
        const loopVar = forMatch[1];
        const iterable = forMatch[2];
        const bodyLine = lines[i + 2] ? lines[i + 2].trim() : "";

        // Check for conditional: if cond: \n  var.append(expr)
        if (bodyLine.startsWith("if ") && i + 3 < lines.length) {
          const cond = bodyLine.replace(/^if\s+/, "").replace(/:$/, "").trim();
          const innerBody = lines[i + 3] ? lines[i + 3].trim() : "";
          const appendMatch = innerBody.match(new RegExp(`^${varName}\\.append\\((.+)\\)$`));
          if (appendMatch) {
            resultLines.push(`${indent}${varName} = [${appendMatch[1]} for ${loopVar} in ${iterable} if ${cond}]`);
            changes.push({
              title: "Manual Loop → List Comprehension",
              before: "4-line loop with conditional append",
              after: "1-line filtered list comprehension",
              description: "Converted verbose loop+if+append pattern into a clean filtered list comprehension."
            });
            i += 4;
            continue;
          }
        }

        // Simple append pattern
        const appendMatch = bodyLine.match(new RegExp(`^${varName}\\.append\\((.+)\\)$`));
        if (appendMatch) {
          resultLines.push(`${indent}${varName} = [${appendMatch[1]} for ${loopVar} in ${iterable}]`);
          changes.push({
            title: "Manual Loop → List Comprehension",
            before: "3-line loop with append",
            after: "1-line list comprehension",
            description: "Converted 3-line loop+append into a 1-line list comprehension."
          });
          i += 3;
          continue;
        }
      }
    }

    // ── Pattern 4: if-elif chain → dict dispatch ────────────────────
    if (stripped.startsWith("if ") && stripped.includes("==") && stripped.includes('"')) {
      const chain = detectIfChain(lines, i);
      if (chain && chain.branches.length >= 3) {
        const varName = chain.branches[0].var;
        const dictName = `${varName}_dispatch`;
        const items = chain.branches
          .filter(b => b.val !== "_else_")
          .map(b => `"${b.val}": lambda: ${b.body}`)
          .join(", ");
        const defaultBranch = chain.branches.find(b => b.val === "_else_");
        resultLines.push(`${indent}${dictName} = {${items}}`);
        if (defaultBranch) {
          resultLines.push(`${indent}action = ${dictName}.get(${varName}, lambda: ${defaultBranch.body})`);
        } else {
          resultLines.push(`${indent}action = ${dictName}.get(${varName}, lambda: None)`);
        }
        resultLines.push(`${indent}action()`);
        changes.push({
          title: "If-Elif Chain → Dictionary Dispatch",
          before: `${chain.branches.length}-branch if-elif chain O(n)`,
          after: "O(1) dictionary lookup",
          description: `Replaced ${chain.branches.length}-branch if-elif chain on '${varName}' with O(1) dictionary dispatch.`
        });
        i += chain.totalLines;
        continue;
      }
    }

    // ── Pattern 5: Dead code after return ───────────────────────────
    if (stripped.startsWith("return ")) {
      resultLines.push(line);
      let j = i + 1;
      let deadCount = 0;
      const baseIndent = indent.length;
      while (j < lines.length) {
        const nextLine = lines[j];
        const nextStripped = nextLine.trim();
        if (!nextStripped) { j++; continue; }
        const nextIndent = nextLine.length - nextLine.trimStart().length;
        if (nextIndent <= baseIndent) break;
        deadCount++;
        j++;
      }
      if (deadCount > 0) {
        changes.push({
          title: "Remove Dead Code",
          before: `${deadCount} unreachable line(s) after return`,
          after: "Removed",
          description: "Removed unreachable code after return statement."
        });
        skipUntil = j;
      }
      i++;
      continue;
    }

    // ── Pattern 6: Simplify verbose booleans ────────────────────────
    if (/if\s+.+\s*==\s*True/.test(stripped)) {
      const newLine = line.replace(/(\w+)\s*==\s*True/g, '$1');
      resultLines.push(newLine);
      changes.push({ title: "Simplify Boolean Check", before: "x == True", after: "x", description: "Removed redundant comparison with True." });
      i++; continue;
    }
    if (/if\s+.+\s*==\s*False/.test(stripped)) {
      const newLine = line.replace(/(\w+)\s*==\s*False/g, 'not $1');
      resultLines.push(newLine);
      changes.push({ title: "Simplify Boolean Check", before: "x == False", after: "not x", description: "Removed redundant comparison with False." });
      i++; continue;
    }

    // ── Pattern 7: len(x) == 0 → not x ─────────────────────────────
    if (/len\(\w+\)\s*==\s*0/.test(stripped)) {
      const newLine = line.replace(/len\((\w+)\)\s*==\s*0/g, 'not $1');
      resultLines.push(newLine);
      changes.push({ title: "Pythonic Empty Check", before: "len(x) == 0", after: "not x", description: "Replaced verbose length check with Pythonic truthiness test." });
      i++; continue;
    }

    // ── Pattern 8: Combine consecutive prints ───────────────────────
    if (stripped.startsWith("print(")) {
      const printBlock = [line];
      let j = i + 1;
      while (j < lines.length && lines[j].trim().startsWith("print(")) {
        printBlock.push(lines[j]);
        j++;
      }
      if (printBlock.length >= 3) {
        const args = printBlock.map(pl => {
          const m = pl.trim().match(/print\((.+)\)/);
          return m ? m[1] : '""';
        });
        resultLines.push(`${indent}print(${args.join(", ")})`);
        changes.push({
          title: "Combine Print Statements",
          before: `${printBlock.length} separate print() calls`,
          after: "1 combined print() call",
          description: "Combined multiple consecutive print statements into a single call."
        });
        i = j;
        continue;
      }
    }

    // ── Default: keep line ──────────────────────────────────────────
    resultLines.push(line);
    i++;
  }

  // Remove trailing blank lines
  while (resultLines.length && !resultLines[resultLines.length - 1].trim()) {
    resultLines.pop();
  }

  let optimized = resultLines.join("\n").replace(/\n{3,}/g, '\n\n');
  return { optimized, changes };
}

// ── JavaScript/TypeScript Optimizer ──────────────────────────────────

function optimizeJS(code) {
  const lines = code.split("\n");
  const resultLines = [];
  const changes = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const stripped = line.trim();
    const indent = line.substring(0, line.length - line.trimStart().length);

    // var → const
    if (/^var\s+\w+/.test(stripped)) {
      resultLines.push(line.replace("var ", "const "));
      changes.push({ title: "var → const", before: "var (function-scoped)", after: "const (block-scoped)", description: "Replaced var with const for block scoping and immutability." });
      continue;
    }

    // == → ===
    if (stripped.includes(" == ") && !stripped.includes(" === ") && !stripped.startsWith("//")) {
      resultLines.push(line.replace(/ == /g, " === "));
      changes.push({ title: "Strict Equality", before: "== (loose)", after: "=== (strict)", description: "Replaced loose equality with strict equality to prevent type coercion bugs." });
      continue;
    }

    // .indexOf() !== -1 → .includes()
    if (stripped.includes(".indexOf(") && stripped.includes("!== -1")) {
      const newLine = line.replace(/(\w+)\.indexOf\((.+?)\)\s*!==\s*-1/g, '$1.includes($2)');
      resultLines.push(newLine);
      changes.push({ title: "indexOf → includes", before: ".indexOf(x) !== -1", after: ".includes(x)", description: "Replaced verbose indexOf check with cleaner includes() method." });
      continue;
    }

    // Simple function → arrow function
    const fnMatch = line.match(/^(\s*)function\s+(\w+)\s*\(([^)]*)\)\s*\{/);
    if (fnMatch && i + 2 < lines.length) {
      const nextStripped = lines[i + 1].trim();
      const afterNext = lines[i + 2] ? lines[i + 2].trim() : "";
      if (nextStripped.startsWith("return ") && afterNext === "}") {
        const returnVal = nextStripped.replace("return ", "").replace(/;$/, "");
        resultLines.push(`${fnMatch[1]}const ${fnMatch[2]} = (${fnMatch[3]}) => ${returnVal};`);
        changes.push({ title: "Function → Arrow Function", before: "3-line function declaration", after: "1-line arrow function", description: `Simplified function '${fnMatch[2]}' to a concise arrow function.` });
        i += 2;
        continue;
      }
    }

    // Remove console.log
    if (stripped.startsWith("console.log(")) {
      changes.push({ title: "Remove console.log", before: "console.log() debug statement", after: "Removed", description: "Removed debug logging statement for production readiness." });
      continue;
    }

    // innerHTML → textContent (XSS)
    if (stripped.includes(".innerHTML =") && !stripped.split("=").slice(1).join("=").includes("<")) {
      resultLines.push(line.replace(".innerHTML =", ".textContent ="));
      changes.push({ title: "Fix XSS: innerHTML → textContent", before: "innerHTML (XSS risk)", after: "textContent (safe)", description: "Replaced innerHTML with textContent to prevent XSS vulnerabilities." });
      continue;
    }

    resultLines.push(line);
  }

  let optimized = resultLines.join("\n").replace(/\n{3,}/g, '\n\n');
  return { optimized, changes };
}

// ── Java Optimizer ──────────────────────────────────────────────────

function optimizeJava(code) {
  let optimized = code;
  const changes = [];

  // Pattern 1: Nested loop duplicate search O(n²) → HashSet O(n)
  const dupRegex = /for\s*\(\s*int\s+(\w+)\s*=[^;]+;\s*\1\s*<[^;]+;\s*\1\+\+\s*\)\s*\{[\s\S]*?for\s*\(\s*int\s+(\w+)\s*=[^;]+;\s*\2\s*<[^;]+;\s*\2\+\+\s*\)\s*\{[\s\S]*?(\w+)\[\1\]\s*==\s*\3\[\2\][\s\S]*?\}[\s\S]*?\}/;
  const match = optimized.match(dupRegex);
  if (match) {
    const arr = match[3] || "arr";
    const replacement = `// O(n) duplicate search via HashSet\n        Set<Integer> seen = new HashSet<>();\n        Set<Integer> duplicates = new LinkedHashSet<>();\n        for (int x : ${arr}) {\n            if (!seen.add(x)) duplicates.add(x);\n        }\n        for (int dup : duplicates) {\n            System.out.println(dup);\n        }`;
    optimized = optimized.replace(match[0], replacement);
    if (!optimized.includes("import java.util.Set;") && !optimized.includes("import java.util.*;")) {
      const importStmt = "import java.util.Set;\nimport java.util.HashSet;\nimport java.util.LinkedHashSet;\n";
      optimized = optimized.includes("import ") ? optimized.replace(/import [^\n]+;\n/, m => m + importStmt) : importStmt + optimized;
    }
    changes.push({
      title: "Nested Loop Duplicate Search → HashSet O(n)",
      before: "O(n²) nested loop comparing arr[i] == arr[j]",
      after: "O(n) linear pass with HashSet",
      description: "Replaced quadratic O(n²) nested loop comparisons with an O(n) HashSet lookup."
    });
  }

  // Pattern 2: Bubble sort in Java
  const bubbleRegex = /for\s*\([^)]+\)\s*\{[\s\n]*for\s*\([^)]+\)\s*\{[\s\n]*if\s*\(\s*(\w+)\[\w+\]\s*>\s*\1\[\w+\s*\+\s*1\]\s*\)[\s\S]*?\}[\s\n]*\}/;
  const bMatch = optimized.match(bubbleRegex);
  if (bMatch) {
    optimized = optimized.replace(bMatch[0], `Arrays.sort(${bMatch[1]}); // O(n log n)`);
    if (!optimized.includes("import java.util.Arrays;") && !optimized.includes("import java.util.*;")) {
      optimized = "import java.util.Arrays;\n" + optimized;
    }
    changes.push({
      title: "Bubble Sort → Arrays.sort()",
      before: "O(n²) manual bubble sort",
      after: "O(n log n) Arrays.sort()",
      description: "Replaced manual quadratic bubble sort with Java's optimized Dual-Pivot Quicksort."
    });
  }

  return { optimized, changes };
}

// ── C/C++ Optimizer ─────────────────────────────────────────────────

function optimizeCpp(code) {
  const lines = code.split("\n");
  const resultLines = [];
  const changes = [];

  for (const line of lines) {
    const stripped = line.trim();

    if (stripped.includes("using namespace std;")) {
      changes.push({ title: "Remove using namespace std", before: "using namespace std; (global pollution)", after: "Use explicit std:: prefix", description: "Global namespace pollution. Use std:: prefix for clarity." });
      continue;
    }

    resultLines.push(line);
  }

  return { optimized: resultLines.join("\n"), changes };
}

// ── Generic Optimizer ───────────────────────────────────────────────

function optimizeGeneric(code) {
  const changes = [];
  let optimized = code;

  const beforeCount = code.split("\n").length;
  optimized = optimized.replace(/\n{3,}/g, '\n\n');
  const afterCount = optimized.split("\n").length;
  if (afterCount < beforeCount) {
    changes.push({ title: "Remove Excess Blank Lines", before: `${beforeCount - afterCount} extra blank lines`, after: "Cleaned up", description: "Removed excessive blank lines for cleaner code." });
  }

  const cleaned = optimized.split("\n").map(l => l.trimEnd()).join("\n");
  if (cleaned !== optimized) {
    changes.push({ title: "Remove Trailing Whitespace", before: "Trailing spaces on lines", after: "Trimmed", description: "Removed trailing whitespace from all lines." });
    optimized = cleaned;
  }

  return { optimized, changes };
}

// ── Complexity Estimator ────────────────────────────────────────────

function estimateComplexity(code) {
  const lines = code.split("\n");
  let hasTripleNest = false;
  let hasDoubleNest = false;
  let hasSingleLoop = false;
  let hasRecursion = false;
  let hasSort = false;
  let nestedForCount = 0;

  for (let i = 0; i < lines.length; i++) {
    const s = lines[i].trim();
    const indent = lines[i].length - lines[i].trimStart().length;
    const level = Math.floor(indent / 4);

    if (/\b(for|while)\b/.test(s)) {
      if (level >= 3) hasTripleNest = true;
      else if (level >= 2) hasDoubleNest = true;
      else hasSingleLoop = true;

      // Look ahead for nested loop
      const currIndent = indent;
      for (let j = i + 1; j < Math.min(i + 15, lines.length); j++) {
        const nextIndent = lines[j].length - lines[j].trimStart().length;
        if (/\b(for|while)\b/.test(lines[j].trim()) && nextIndent > currIndent) {
          nestedForCount++;
          break;
        }
      }
    }

    const fnMatch = s.match(/\b(?:def|function)\s+(\w+)/);
    if (fnMatch) {
      const fnName = fnMatch[1];
      if ((code.match(new RegExp(`${fnName}\\(`, 'g')) || []).length >= 2) {
        hasRecursion = true;
      }
    }

    if (/\.(sort|sorted)\b|\bsort\s*\(|\bArrays\.sort|std::sort/.test(s)) {
      hasSort = true;
    }
  }

  if (nestedForCount >= 2 || hasTripleNest) return "O(n³)";
  if (nestedForCount >= 1 || hasDoubleNest) return "O(n²)";
  if (hasRecursion && hasSort) return "O(n log n)";
  if (hasRecursion) return "O(2ⁿ) / O(n log n)";
  if (hasSort) return "O(n log n)";
  if (hasSingleLoop) return "O(n)";
  return "O(1)";
}

// ── Speedup Calculator ──────────────────────────────────────────────

function calculateSpeedup(cb, ca) {
  const cbl = cb.toLowerCase().replace(/\s/g, "");
  const cal = ca.toLowerCase().replace(/\s/g, "");

  if (/2\^n|2ⁿ|o\(2/.test(cbl)) return "Exponential Speedup (~10,000x - 1,000,000x for N > 30)";
  if (/n\^3|n³/.test(cbl)) {
    if (/n\^2|n²/.test(cal)) return "Cubic to Quadratic (~1,000x faster on N = 1,000)";
    return "Cubic to Linear (~1,000,000x faster on N = 1,000)";
  }
  if (/n\^2|n²/.test(cbl)) {
    if (/^o\(n\)$/.test(cal) || (cal.includes("n") && !cal.includes("log") && !cal.includes("2"))) {
      return "Quadratic to Linear (~1,000x - 100,000x faster on large inputs)";
    }
    if (/log/.test(cal)) return "Quadratic to Linearithmic (~100x - 500x faster)";
  }
  if (cbl !== cal) return `Order-of-magnitude reduction from ${cb} to ${ca}`;
  return "~1.5x - 3.0x speedup via eliminated redundant iterations and allocations";
}

// ── Helper: Find end of indented block ──────────────────────────────

function findBlockEnd(lines, start) {
  if (start >= lines.length) return start;
  const baseIndent = lines[start].length - lines[start].trimStart().length;
  let j = start + 1;
  while (j < lines.length) {
    const currIndent = lines[j].length - lines[j].trimStart().length;
    if (lines[j].trim() === "") { j++; continue; }
    if (currIndent > baseIndent) { j++; } else { break; }
  }
  return j;
}

// ── Helper: Detect bubble sort ──────────────────────────────────────

function isBubbleSortBlock(lines, start) {
  const block = lines.slice(start, start + 15).join("\n");
  return looksLikeBubbleSort(block);
}

function looksLikeBubbleSort(code) {
  const hasNested = /for\s+.*:.*\n\s+for\s+/s.test(code);
  const hasSwap = /(\w+)\[(\w+)\],\s*\1\[(\w+)\]\s*=\s*\1\[\3\],\s*\1\[\2\]/.test(code);
  const hasComparison = /if\s+\w+\[\w+\]\s*[>]\s*\w+\[\w+\+?\s*\d*\]/.test(code);
  return hasNested && (hasSwap || hasComparison);
}

// ── Helper: Detect if-elif chain ────────────────────────────────────

function detectIfChain(lines, start) {
  const branches = [];
  let i = start;
  let totalLines = 0;

  while (i < lines.length) {
    const stripped = lines[i].trim();
    if (stripped.startsWith("if ") || stripped.startsWith("elif ")) {
      const eqMatch = stripped.match(/(\w+)\s*==\s*["']([^"']+)["']/);
      if (eqMatch && i + 1 < lines.length) {
        branches.push({ var: eqMatch[1], val: eqMatch[2], body: lines[i + 1].trim() });
        i += 2;
        totalLines += 2;
        continue;
      }
    } else if (stripped.startsWith("else")) {
      if (i + 1 < lines.length) {
        branches.push({ var: "_else_", val: "_else_", body: lines[i + 1].trim() });
        totalLines += 2;
      }
      break;
    } else {
      break;
    }
    i++;
  }

  if (branches.length >= 3) return { branches, totalLines };
  return null;
}

function renderResults(data) {
  const resultsContainer = document.getElementById("optimizer-results");
  if (resultsContainer) {
    resultsContainer.style.display = "block";
    resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Metric: Complexity
  const compEl = document.getElementById("metric-complexity");
  if (compEl) {
    compEl.innerHTML = `
      <span class="badge-complexity-old">${escapeHtml(data.complexity_before)}</span>
      <span style="color:var(--text-muted);">&rarr;</span>
      <span class="badge-complexity-new">${escapeHtml(data.complexity_after)}</span>
    `;
  }

  // Metric: Speedup
  const speedEl = document.getElementById("metric-speedup");
  if (speedEl) {
    speedEl.textContent = data.speedup_estimate || "Order-of-magnitude faster";
  }

  // Metric: Reduction
  const redEl = document.getElementById("metric-reduction");
  if (redEl) {
    const linesSaved = data.lines_before - data.lines_after;
    const pct = Math.round((linesSaved / Math.max(data.lines_before, 1)) * 100);
    if (linesSaved > 0) {
      redEl.textContent = `-${linesSaved} lines (${pct}% smaller)`;
    } else {
      redEl.textContent = `${data.lines_after} clean lines`;
    }
  }

  // Metric: Engine
  const engineVal = document.getElementById("metric-engine");
  const engineSub = document.getElementById("metric-engine-sub");
  if (engineVal) {
    engineVal.textContent = data.model_used || "Rule-based Engine";
  }
  if (engineSub) {
    if ((data.model_used || "").includes("Ollama")) {
      engineSub.textContent = "AI model analysis & time complexity reduction";
    } else {
      engineSub.textContent = "Algorithmic AST pattern & complexity reducer";
    }
  }

  // Summary message
  const summaryEl = document.getElementById("result-summary-text");
  if (summaryEl) {
    summaryEl.textContent = data.summary;
  }

  // Pane 1: Optimized Code
  const optCodePre = document.getElementById("code-display-optimized");
  if (optCodePre) {
    optCodePre.textContent = data.optimized_code;
  }

  // Pane 2: Frontend File
  const feCodePre = document.getElementById("code-display-frontend");
  if (feCodePre) {
    feCodePre.textContent = data.frontend_code || "<!-- No separate frontend generated -->";
  }

  // Pane 3: Backend File
  const beCodePre = document.getElementById("code-display-backend");
  if (beCodePre) {
    beCodePre.textContent = data.backend_code || "# No separate backend generated";
  }

  // Separation notice note
  const sepNoteEl = document.getElementById("separation-note-text");
  if (sepNoteEl) {
    sepNoteEl.textContent = data.separation_note || "Code separated into standalone Frontend and Backend files for easy revision.";
  }

  // Pane 4: Side-by-Side Diff
  renderDiffView(data.original_code, data.optimized_code);

  // Pane 5: Changelog & Breakdown
  renderChangesList(data.changes);

  // Default to optimized code tab
  switchTab("optimized");
}

function renderDiffView(original, optimized) {
  const container = document.getElementById("diff-view-mount");
  if (!container) return;

  const origLines = original.split("\n");
  const optLines = optimized.split("\n");
  const maxLines = Math.max(origLines.length, optLines.length);

  let origHtml = "";
  let optHtml = "";

  for (let i = 0; i < maxLines; i++) {
    const oLine = origLines[i] !== undefined ? origLines[i] : "";
    const nLine = optLines[i] !== undefined ? optLines[i] : "";

    const isDifferent = oLine !== nLine;
    const isOrigMissing = origLines[i] === undefined;
    const isOptMissing = optLines[i] === undefined;

    let origClass = "diff-line";
    let optClass = "diff-line";

    if (isDifferent) {
      if (!isOrigMissing) origClass += " diff-line-removed";
      if (!isOptMissing) optClass += " diff-line-added";
    }

    origHtml += `
      <div class="${origClass}">
        <div class="diff-line-num">${isOrigMissing ? "" : i + 1}</div>
        <div class="diff-line-content">${escapeHtml(oLine)}</div>
      </div>
    `;

    optHtml += `
      <div class="${optClass}">
        <div class="diff-line-num">${isOptMissing ? "" : i + 1}</div>
        <div class="diff-line-content">${escapeHtml(nLine)}</div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="diff-container">
      <div class="diff-pane">
        <div class="diff-pane-header original">Original Code (Before)</div>
        ${origHtml}
      </div>
      <div class="diff-pane">
        <div class="diff-pane-header" style="color:#10b981;">Optimized Code (After)</div>
        ${optHtml}
      </div>
    </div>
  `;
}

function renderChangesList(changes) {
  const listEl = document.getElementById("changes-list-mount");
  if (!listEl) return;

  if (!changes || changes.length === 0) {
    listEl.innerHTML = `
      <div class="change-item" style="text-align:center;color:var(--text-muted);padding:2rem;">
        No major algorithmic antipatterns detected. The code was minimized and reformatted cleanly.
      </div>
    `;
    return;
  }

  listEl.innerHTML = changes.map(ch => `
    <div class="change-item">
      <div class="change-item-title">
        <span style="color:var(--primary-blue);">&#9889;</span> ${escapeHtml(ch.title)}
      </div>
      <div class="change-item-desc">${escapeHtml(ch.description)}</div>
      <div class="change-item-diff">
        <div class="change-box-before"><strong>Before:</strong> ${escapeHtml(ch.before)}</div>
        <div class="change-box-after"><strong>After:</strong> ${escapeHtml(ch.after)}</div>
      </div>
    </div>
  `).join("");
}

function setupCopyBtn(btnId, getText) {
  const btn = document.getElementById(btnId);
  if (!btn) return;

  btn.addEventListener("click", () => {
    const text = getText();
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      const orig = btn.innerHTML;
      btn.innerHTML = "<span>&#10003; Copied!</span>";
      setTimeout(() => btn.innerHTML = orig, 2000);
    });
  });
}

function setupDownloadBtn(btnId, getText, getFilename) {
  const btn = document.getElementById(btnId);
  if (!btn) return;

  btn.addEventListener("click", () => {
    const text = getText();
    if (!text) return;

    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = getFilename();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });
}

function getFilenameForLang(prefix) {
  const lang = currentOptimizationResult ? currentOptimizationResult.language : "python";
  const extMap = {
    python: "py",
    javascript: "js",
    typescript: "ts",
    cpp: "cpp",
    c: "c",
    java: "java",
    html: "html",
    css: "css"
  };
  const ext = extMap[lang] || "txt";
  return `${prefix}.${ext}`;
}

function hideResults() {
  const resultsContainer = document.getElementById("optimizer-results");
  if (resultsContainer) resultsContainer.style.display = "none";
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
