/* Semptify Go — mobile PWA JS */

// ── Screen navigation ─────────────────────────────────────────────────────
document.querySelectorAll('.go-nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.screen;
    document.querySelectorAll('.go-screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.go-nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('screen-' + target).classList.add('active');
    btn.classList.add('active');
    if (target === 'timeline') loadTimeline();
    if (target === 'inbox')    loadInbox();
  });
});

// ── File input → show meta form ───────────────────────────────────────────
const fileInput  = document.getElementById('file-input');
const uploadMeta = document.getElementById('upload-meta');
const uploadZone = document.getElementById('upload-zone');

fileInput.addEventListener('change', () => {
  if (fileInput.files.length) {
    uploadZone.style.borderStyle = 'solid';
    uploadZone.querySelector('.go-upload-label').textContent = fileInput.files[0].name;
    uploadMeta.classList.remove('hidden');
    loadCasesIntoSelect();
  }
});

// ── Load cases into select ────────────────────────────────────────────────
async function loadCasesIntoSelect() {
  try {
    const resp = await fetch('/api/cases');
    if (!resp.ok) return;
    const cases = await resp.json();
    const sel = document.getElementById('upload-case');
    sel.innerHTML = '<option value="">— Select a case —</option>';
    for (const c of cases) {
      const opt = document.createElement('option');
      opt.value = c.id;
      opt.textContent = c.title;
      sel.appendChild(opt);
    }
  } catch (_) {}
}

// ── Upload submit ─────────────────────────────────────────────────────────
document.getElementById('upload-submit').addEventListener('click', async () => {
  const file    = fileInput.files[0];
  const caseId  = document.getElementById('upload-case').value;
  const docType = document.getElementById('upload-type').value;
  const note    = document.getElementById('upload-note').value.trim();
  const result  = document.getElementById('upload-result');

  if (!file) return;

  const fd = new FormData();
  fd.append('file', file);
  fd.append('document_type', docType);
  if (caseId) fd.append('case_id', caseId);
  if (note)   fd.append('note', note);

  result.className = 'go-result';
  result.textContent = 'Uploading…';
  result.classList.remove('hidden');

  try {
    const resp = await fetch('/api/documents/upload', { method: 'POST', body: fd });
    if (resp.ok) {
      result.classList.add('success');
      result.textContent = 'Uploaded successfully.';
      fileInput.value = '';
      uploadMeta.classList.add('hidden');
      uploadZone.querySelector('.go-upload-label').textContent = 'Tap to choose a file';
      uploadZone.style.borderStyle = 'dashed';
    } else {
      const err = await resp.json().catch(() => ({}));
      result.classList.add('error');
      result.textContent = err.detail || 'Upload failed.';
    }
  } catch (e) {
    result.classList.add('error');
    result.textContent = 'Network error — check your connection.';
  }
});

// ── Timeline ──────────────────────────────────────────────────────────────
async function loadTimeline() {
  const list = document.getElementById('timeline-list');
  list.innerHTML = '<p class="go-empty">Loading…</p>';
  try {
    const resp = await fetch('/api/documents');
    if (!resp.ok) throw new Error();
    const docs = await resp.json();
    if (!docs.length) {
      list.innerHTML = '<p class="go-empty">No events yet. Upload a document to start your record.</p>';
      return;
    }
    list.innerHTML = docs.map(d => `
      <div class="go-timeline-item">
        <div class="go-timeline-date">${d.created_at ? new Date(d.created_at).toLocaleDateString() : '—'}</div>
        <div class="go-timeline-title">${esc(d.filename || d.title || 'Document')}</div>
        <div class="go-timeline-type">${esc(d.document_type || '')}</div>
      </div>`).join('');
  } catch (_) {
    list.innerHTML = '<p class="go-empty">Could not load timeline.</p>';
  }
}

// ── Inbox ─────────────────────────────────────────────────────────────────
async function loadInbox() {
  const list = document.getElementById('inbox-list');
  list.innerHTML = '<p class="go-empty">Loading…</p>';
  try {
    const resp = await fetch('/api/tidbits');
    if (!resp.ok) throw new Error();
    const items = await resp.json();
    if (!items.length) {
      list.innerHTML = '<p class="go-empty">No messages.</p>';
      return;
    }
    list.innerHTML = items.map(t => `
      <div class="go-inbox-item">
        <div class="go-inbox-from">${esc(t.category || 'Info')}</div>
        <div class="go-inbox-msg">${esc(t.content || '')}</div>
      </div>`).join('');
  } catch (_) {
    list.innerHTML = '<p class="go-empty">No messages.</p>';
  }
}

// ── Utility ───────────────────────────────────────────────────────────────
function esc(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── PWA Service Worker ────────────────────────────────────────────────────
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/sw.js').catch(() => {});
}
