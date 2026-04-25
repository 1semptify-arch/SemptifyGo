/**
 * Semptify55 - Mobile App
 * Tenant rights platform frontend
 */

// API Base URL
const API_BASE = '';

// App State
const state = {
    user: null,
    cases: [],
    tidbits: [],
    currentView: 'auth'
};

// DOM Elements
const elements = {
    authSection: document.getElementById('auth-section'),
    casesSection: document.getElementById('cases-section'),
    tidbitsSection: document.getElementById('tidbits-section'),
    casesList: document.getElementById('cases-list'),
    tidbitsList: document.getElementById('tidbits-list'),
    appNav: document.querySelector('.app-nav'),
    caseModal: document.getElementById('case-modal'),
    caseForm: document.getElementById('case-form'),
    newCaseBtn: document.getElementById('new-case-btn'),
    cancelCaseBtn: document.getElementById('cancel-case')
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    checkAuth();
});

// Event Listeners
function initEventListeners() {
    // Storage provider buttons
    document.querySelectorAll('.btn-storage').forEach(btn => {
        btn.addEventListener('click', () => {
            const provider = btn.dataset.provider;
            handleAuth(provider);
        });
    });

    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
        });
    });

    // Case modal
    elements.newCaseBtn?.addEventListener('click', showCaseModal);
    elements.cancelCaseBtn?.addEventListener('click', hideCaseModal);
    elements.caseForm?.addEventListener('submit', handleCreateCase);

    // Close modal on backdrop click
    elements.caseModal?.addEventListener('click', (e) => {
        if (e.target === elements.caseModal) hideCaseModal();
    });
}

// Auth Handlers
function handleAuth(provider) {
    // Redirect to OAuth
    window.location.href = `${API_BASE}/auth/${provider}`;
}

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/api/me`);
        if (response.ok) {
            state.user = await response.json();
            showAuthenticatedUI();
            loadData();
        }
    } catch (err) {
        console.log('Not authenticated');
    }
}

function showAuthenticatedUI() {
    elements.authSection.classList.add('hidden');
    elements.casesSection.classList.remove('hidden');
    elements.tidbitsSection.classList.remove('hidden');
    elements.appNav.classList.remove('hidden');
}

// Data Loading
async function loadData() {
    await Promise.all([loadCases(), loadTidbits()]);
}

async function loadCases() {
    try {
        const response = await fetch(`${API_BASE}/api/cases`);
        if (response.ok) {
            state.cases = await response.json();
            renderCases();
        }
    } catch (err) {
        console.error('Failed to load cases:', err);
    }
}

async function loadTidbits() {
    try {
        const response = await fetch(`${API_BASE}/api/tidbits`);
        if (response.ok) {
            state.tidbits = await response.json();
            renderTidbits();
        }
    } catch (err) {
        console.error('Failed to load tidbits:', err);
    }
}

// Rendering
function renderCases() {
    if (state.cases.length === 0) {
        elements.casesList.innerHTML = '<p class="empty-state">No cases yet. Create your first case.</p>';
        return;
    }

    elements.casesList.innerHTML = state.cases.map(c => `
        <div class="card" data-case-id="${c.id}">
            <div class="card-title">${escapeHtml(c.title)}</div>
            <div class="card-meta">${escapeHtml(c.case_type)} • ${formatDate(c.created_at)}</div>
            <span class="card-status status-${c.status}">${c.status}</span>
        </div>
    `).join('');
}

function renderTidbits() {
    if (state.tidbits.length === 0) {
        elements.tidbitsList.innerHTML = '<p class="empty-state">No tips available.</p>';
        return;
    }

    elements.tidbitsList.innerHTML = state.tidbits.map(t => `
        <div class="tidbit">
            <div class="tidbit-title">${escapeHtml(t.title)}</div>
            <div class="tidbit-content">${escapeHtml(t.content)}</div>
            <div class="tidbit-meta">${escapeHtml(t.category)}${t.jurisdiction ? ` • ${escapeHtml(t.jurisdiction)}` : ''}</div>
        </div>
    `).join('');
}

// Case Modal
function showCaseModal() {
    elements.caseModal.classList.remove('hidden');
    document.getElementById('case-title').focus();
}

function hideCaseModal() {
    elements.caseModal.classList.add('hidden');
    elements.caseForm.reset();
}

async function handleCreateCase(e) {
    e.preventDefault();

    const data = {
        title: document.getElementById('case-title').value,
        case_type: document.getElementById('case-type').value,
        description: document.getElementById('case-description').value
    };

    try {
        const response = await fetch(`${API_BASE}/api/cases`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const newCase = await response.json();
            state.cases.unshift(newCase);
            renderCases();
            hideCaseModal();
        } else {
            const error = await response.json();
            alert(error.detail || 'Failed to create case');
        }
    } catch (err) {
        console.error('Failed to create case:', err);
        alert('Failed to create case. Please try again.');
    }
}

// View Switching
function switchView(view) {
    // Update nav
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Show/hide sections
    elements.casesSection.classList.toggle('hidden', view !== 'cases');
    elements.tidbitsSection.classList.toggle('hidden', view !== 'tidbits');
    // Settings view would go here

    state.currentView = view;
}

// Utilities
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}
