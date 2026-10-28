// =====================================================================
// IELTS MASTER: COMMON UTILITY & UI HELPERS
// =====================================================================

function isViewActive(viewName) {
    const el = document.getElementById(`view-${viewName}`);
    return !!(el && !el.classList.contains('hidden'));
}

function formatTimeMMSS(totalSec) {
    if (isNaN(totalSec) || totalSec < 0) totalSec = 0;
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function toggleMobileDrawer(forceState = null) {
    const drawer = document.getElementById('mobile-drawer');
    const backdrop = document.getElementById('mobile-drawer-backdrop');
    if (!drawer || !backdrop) return;

    const isOpen = drawer.classList.contains('drawer-open');
    const shouldOpen = (forceState !== null) ? forceState : !isOpen;

    if (shouldOpen) {
        drawer.classList.remove('drawer-closed');
        drawer.classList.add('drawer-open');
        backdrop.classList.remove('backdrop-closed');
        backdrop.classList.add('backdrop-open');
        document.body.style.overflow = 'hidden';
    } else {
        drawer.classList.remove('drawer-open');
        drawer.classList.add('drawer-closed');
        backdrop.classList.remove('backdrop-open');
        backdrop.classList.add('backdrop-closed');
        document.body.style.overflow = '';
    }
}

function toggleClockVisibility(module) {
    if (!module) return;
    module = module.toLowerCase();
    clockHiddenState[module] = !clockHiddenState[module];
    const isHidden = clockHiddenState[module];

    const timerMap = {
        reading: { timerId: 'reading-timer', btnId: 'btn-toggle-clock' },
        listening: { timerId: 'listening-timer', btnId: 'btn-toggle-listening-clock' },
        writing: { timerId: 'writing-timer', btnId: 'btn-toggle-writing-clock' },
        speaking: { timerId: 'speaking-timer', btnId: 'btn-toggle-speaking-clock' }
    };

    const conf = timerMap[module];
    if (conf) {
        const timerEl = document.getElementById(conf.timerId);
        const btnLabel = document.getElementById(conf.btnId);
        if (timerEl) {
            if (isHidden) {
                timerEl.classList.add('hidden');
            } else {
                timerEl.classList.remove('hidden');
            }
        }
        if (btnLabel) {
            btnLabel.innerText = isHidden ? 'Show Clock' : 'Hide Clock';
        }
    }
}

function getAuthHeaders(extraHeaders = {}) {
    const headers = { 'Content-Type': 'application/json', ...extraHeaders };
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    return headers;
}

// =====================================================================
// SIMPLISTIC THEME TOGGLE (LIGHT / DARK MODE)
// =====================================================================

function initTheme() {
    const savedTheme = localStorage.getItem('ielts_theme') || 'light';
    applyTheme(savedTheme);
}

function applyTheme(theme) {
    const isDark = theme === 'dark';
    document.body.classList.toggle('dark-mode', isDark);
    document.body.classList.toggle('cd-theme-dark', isDark);
    localStorage.setItem('ielts_theme', isDark ? 'dark' : 'light');

    // Update desktop button icons
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    const toggleBtn = document.getElementById('btn-theme-toggle');
    if (sunIcon) sunIcon.classList.toggle('hidden', !isDark);
    if (moonIcon) moonIcon.classList.toggle('hidden', isDark);
    if (toggleBtn) {
        toggleBtn.setAttribute('title', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');
    }

    // Update mobile button icons
    document.querySelectorAll('.theme-icon-sun-mob').forEach(el => el.classList.toggle('hidden', !isDark));
    document.querySelectorAll('.theme-icon-moon-mob').forEach(el => el.classList.toggle('hidden', isDark));
}

function toggleTheme() {
    const isCurrentlyDark = document.body.classList.contains('dark-mode') || document.body.classList.contains('cd-theme-dark');
    applyTheme(isCurrentlyDark ? 'light' : 'dark');
}

// Backward compatibility alias
function setContrastTheme(theme) {
    applyTheme(theme === 'dark' ? 'dark' : 'light');
}

