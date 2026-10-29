// =====================================================================
// IELTS MASTER: GLOBAL APPLICATION STATE & CONSTANTS
// =====================================================================

const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? window.location.origin
    : '';

// User Authentication & Session State
let authToken = localStorage.getItem('ielts_auth_token') || null;
let currentUser = null;

// Global Fetch Interceptor to seamlessly route Authorization token to all backend API calls
const _originalFetch = window.fetch;
window.fetch = function(resource, init = {}) {
    if (typeof resource === 'string' && resource.includes('/api/') && !resource.includes('googleapis.com')) {
        init = init || {};
        const headers = new Headers(init.headers || {});
        if (authToken && !headers.has('Authorization')) {
            headers.set('Authorization', `Bearer ${authToken}`);
        }
        init.headers = headers;
    }
    return _originalFetch(resource, init);
};

// Application Settings & Diagnostics State
let appSettings = {};
let appDiagnostics = {};
let radarChartInstance = null;
let trendChartInstance = null;

// Test Catalog & UI Preferences
let availableTests = {
    listening: [],
    reading: [],
    writing: [],
    speaking: []
};

let clockHiddenState = {
    reading: false,
    listening: false,
    writing: false,
    speaking: false
};

// Audio Engine & Synthesis State
let currentAudioEngine = localStorage.getItem('ielts_audio_engine') || 'gemini';
let currentGeminiPersona = localStorage.getItem('ielts_gemini_persona') || 'Puck';
let selectedBrowserVoiceURI = localStorage.getItem('ielts_browser_voice') || '';
let availableBrowserVoices = [];
let bestNaturalVoice = null;
let voicesPopulatedAlready = false;
const audioBlobCache = new Map();
let currentAudioElement = null;

// Listening Module State
let currentListeningTest = null;
let currentListeningResults = null;
let listeningAudioUtterance = null;
let isAudioPlaying = false;
let audioSpeechRate = 1.0;
let listeningAnswers = {};
let listeningTimerInterval = null;
let listeningTimeLeftSec = 1800; // 30:00 mins
let listeningPassagePlaying = false;
let listeningSentencesQueue = [];
let listeningSentenceIndex = 0;
let listeningTimeoutId = null;

// Reading Module State
let currentReadingTest = null;
let currentReadingResults = null;
let activeReadingPassageIdx = 0;
let readingFontSizePx = 14;
let readingAnswers = {};
let flaggedQuestions = new Set();
let readingTimerInterval = null;
let readingTimeLeftSec = 3600; // 60:00 mins
let currentActiveQId = null;

// Writing Module State
let currentWritingTask = null;
let writingTimerInterval = null;
let writingTimeLeftSec = 2400; // 40:00 mins default (Task 2) or 20:00 (Task 1)

// Speaking Module State
let currentSpeakingTest = null;
let activeSpeakingPart = 1;
let speakingResponses = {};
let speechRecognitionInstance = null;
let isRecording = false;
let prepTimerInterval = null;
let speakingTimerInterval = null;
let overallSpeakingTimerInterval = null;
let speakingTimeLeftSec = 840; // 14:00 mins overall mock window

// Vocabulary State
let vocabularyList = [];

// Exit Exam Session & Exclusion Tracking
let pendingExitTargetView = null;
let pendingExitModule = null;
const lastExitedTestId = {
    reading: null,
    listening: null,
    writing: null,
    speaking: null
};
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

// =====================================================================
// IELTS MASTER: UNIVERSAL CD IELTS TIMER ENGINE (ALL 4 MODULES)
// =====================================================================

// 1. Reading Timer Controller (60:00 Official Window)
function updateReadingTimerDisplay() {
    const timeStr = formatTimeMMSS(readingTimeLeftSec);
    const timerEl = document.getElementById('reading-timer');
    const subTimerEl = document.getElementById('reading-sub-timer');
    if (timerEl) timerEl.innerText = timeStr;
    if (subTimerEl) subTimerEl.innerText = timeStr;
}

function startReadingTimer() {
    if (readingTimerInterval) clearInterval(readingTimerInterval);
    updateReadingTimerDisplay();
    readingTimerInterval = setInterval(() => {
        readingTimeLeftSec--;
        if (readingTimeLeftSec <= 0) {
            readingTimeLeftSec = 0;
            clearInterval(readingTimerInterval);
            readingTimerInterval = null;
            updateReadingTimerDisplay();
            alert('Time is up for IELTS Academic Reading! Submitting your answers for automated assessment.');
            if (typeof submitReadingTest === 'function') submitReadingTest();
            return;
        }
        updateReadingTimerDisplay();
    }, 1000);
}

function pauseReadingTimer() {
    if (readingTimerInterval) {
        clearInterval(readingTimerInterval);
        readingTimerInterval = null;
    }
}

function resetReadingTimer() {
    pauseReadingTimer();
    readingTimeLeftSec = 3600;
    updateReadingTimerDisplay();
}

// 2. Listening Timer Controller (30:00 Official Window)
function updateListeningTimerDisplay() {
    const timeStr = formatTimeMMSS(listeningTimeLeftSec);
    const timerEl = document.getElementById('listening-timer');
    const subTimerEl = document.getElementById('listening-sub-timer');
    if (timerEl) timerEl.innerText = timeStr;
    if (subTimerEl) subTimerEl.innerText = timeStr;
}

function startListeningTimer() {
    if (listeningTimerInterval) clearInterval(listeningTimerInterval);
    updateListeningTimerDisplay();
    listeningTimerInterval = setInterval(() => {
        listeningTimeLeftSec--;
        if (listeningTimeLeftSec <= 0) {
            listeningTimeLeftSec = 0;
            clearInterval(listeningTimerInterval);
            listeningTimerInterval = null;
            updateListeningTimerDisplay();
            if (typeof stopAnyActiveAudio === 'function') stopAnyActiveAudio();
            alert('Time is up for IELTS Listening Test! Submitting your answers for automated assessment.');
            if (typeof submitListeningTest === 'function') submitListeningTest();
            return;
        }
        updateListeningTimerDisplay();
    }, 1000);
}

function pauseListeningTimer() {
    if (listeningTimerInterval) {
        clearInterval(listeningTimerInterval);
        listeningTimerInterval = null;
    }
}

function resetListeningTimer() {
    pauseListeningTimer();
    listeningTimeLeftSec = 1800;
    updateListeningTimerDisplay();
}

// 3. Writing Timer Controller (40:00 / 20:00 Official Window)
function updateWritingTimerDisplay() {
    const timeStr = formatTimeMMSS(writingTimeLeftSec);
    const timerEl = document.getElementById('writing-timer');
    const countdownBadge = document.getElementById('writing-countdown');
    if (timerEl) timerEl.innerText = timeStr;
    if (countdownBadge) countdownBadge.innerText = `⏱️ ${timeStr} remaining`;
}

function startWritingTimer(durationSeconds = null) {
    if (writingTimerInterval) clearInterval(writingTimerInterval);
    if (durationSeconds) {
        writingTimeLeftSec = durationSeconds;
    } else if (!writingTimeLeftSec || writingTimeLeftSec <= 0) {
        const isTask1 = currentWritingTask?.content?.task_type === 'Task 1' ||
                        (currentWritingTask?.id && parseInt(currentWritingTask.id.replace('W-', ''), 10) % 2 === 0);
        writingTimeLeftSec = isTask1 ? 1200 : 2400;
    }
    updateWritingTimerDisplay();
    writingTimerInterval = setInterval(() => {
        writingTimeLeftSec--;
        if (writingTimeLeftSec <= 0) {
            writingTimeLeftSec = 0;
            clearInterval(writingTimerInterval);
            writingTimerInterval = null;
            updateWritingTimerDisplay();
            const badge = document.getElementById('writing-countdown');
            if (badge) badge.innerText = "⏱️ 00:00 (Time's up)";
            alert('Time is up for IELTS Writing! Submitting your response for automated Band assessment.');
            if (typeof submitWritingEvaluation === 'function') submitWritingEvaluation();
            return;
        }
        updateWritingTimerDisplay();
    }, 1000);
}

function pauseWritingTimer() {
    if (writingTimerInterval) {
        clearInterval(writingTimerInterval);
        writingTimerInterval = null;
    }
}

function resetWritingTimer(duration = null) {
    pauseWritingTimer();
    if (duration) {
        writingTimeLeftSec = duration;
    } else {
        const isTask1 = currentWritingTask?.content?.task_type === 'Task 1' ||
                        (currentWritingTask?.id && parseInt(currentWritingTask.id.replace('W-', ''), 10) % 2 === 0);
        writingTimeLeftSec = isTask1 ? 1200 : 2400;
    }
    updateWritingTimerDisplay();
}

// 4. Speaking Overall Timer Controller (14:00 Official Window)
function updateSpeakingExamTimerDisplay() {
    const timeStr = formatTimeMMSS(speakingTimeLeftSec);
    const timerEl = document.getElementById('speaking-timer');
    const subTimerEl = document.getElementById('speaking-sub-timer');
    if (timerEl) timerEl.innerText = timeStr;
    if (subTimerEl) subTimerEl.innerText = timeStr;
}

function startOverallSpeakingTimer() {
    if (overallSpeakingTimerInterval) clearInterval(overallSpeakingTimerInterval);
    updateSpeakingExamTimerDisplay();
    overallSpeakingTimerInterval = setInterval(() => {
        speakingTimeLeftSec--;
        if (speakingTimeLeftSec <= 0) {
            speakingTimeLeftSec = 0;
            clearInterval(overallSpeakingTimerInterval);
            overallSpeakingTimerInterval = null;
            updateSpeakingExamTimerDisplay();
            if (typeof stopSpeechRecognition === 'function') stopSpeechRecognition();
            alert('Official 14-minute interview window completed. Submitting speaking mock for comprehensive Band evaluation.');
            if (typeof submitSpeakingEvaluation === 'function') submitSpeakingEvaluation();
            return;
        }
        updateSpeakingExamTimerDisplay();
    }, 1000);
}

function pauseOverallSpeakingTimer() {
    if (overallSpeakingTimerInterval) {
        clearInterval(overallSpeakingTimerInterval);
        overallSpeakingTimerInterval = null;
    }
}

function resetOverallSpeakingTimer() {
    pauseOverallSpeakingTimer();
    speakingTimeLeftSec = 840;
    updateSpeakingExamTimerDisplay();
}

function pauseAllExamTimers() {
    pauseReadingTimer();
    pauseListeningTimer();
    pauseWritingTimer();
    pauseOverallSpeakingTimer();
}
// =====================================================================
// IELTS MASTER: MULTIUSER AUTHENTICATION CONTROLLER
// =====================================================================

function updateCurrentUserUI(user) {
    currentUser = user;
    if (!user) {
        ['mobile-user-avatar', 'drawer-user-avatar', 'sidebar-user-avatar', 'header-user-avatar'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = '👤';
        });
        const headerNameEl = document.getElementById('header-user-name');
        if (headerNameEl) headerNameEl.innerText = 'Sign In / Register';
        const headerIdEl = document.getElementById('header-user-id');
        if (headerIdEl) headerIdEl.innerText = 'Guest Candidate';

        const btnHeader = document.getElementById('btn-header-user-profile');
        if (btnHeader) btnHeader.title = 'Sign In / Register';

        ['drawer-user-name', 'sidebar-user-name'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = 'Sign In / Register';
        });
        ['drawer-user-email', 'sidebar-user-email'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = 'Click to access account';
        });
        ['hero-user-name', 'cd-reading-candidate-name', 'cd-listening-candidate-name', 'cd-writing-candidate-name', 'cd-speaking-candidate-name'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = 'Guest Candidate';
        });
        ['cd-reading-candidate-id', 'cd-listening-candidate-id', 'cd-writing-candidate-id', 'cd-speaking-candidate-id'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = 'GUEST-000';
        });

        // Hide logout buttons if unauthenticated
        const btnSidebarLogout = document.getElementById('btn-sidebar-logout');
        if (btnSidebarLogout) btnSidebarLogout.classList.add('hidden');
        const btnDrawerLogout = document.getElementById('btn-drawer-logout');
        if (btnDrawerLogout) btnDrawerLogout.classList.add('hidden');

        return;
    }

    // Show logout buttons
    const btnSidebarLogout = document.getElementById('btn-sidebar-logout');
    if (btnSidebarLogout) btnSidebarLogout.classList.remove('hidden');
    const btnDrawerLogout = document.getElementById('btn-drawer-logout');
    if (btnDrawerLogout) btnDrawerLogout.classList.remove('hidden');

    const btnHeader = document.getElementById('btn-header-user-profile');
    if (btnHeader) btnHeader.title = 'Candidate Profile & Credentials (Click to view)';

    // Compute candidate initials (e.g. "Alex Morgan" -> "AM")
    const names = (user.name || 'Candidate').trim().split(/\s+/);
    const initials = names.length > 1
        ? (names[0][0] + names[names.length - 1][0]).toUpperCase()
        : (names[0].substring(0, 2)).toUpperCase();

    ['mobile-user-avatar', 'drawer-user-avatar', 'sidebar-user-avatar', 'header-user-avatar'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = initials;
    });

    const candidateNameIds = [
        'drawer-user-name', 'sidebar-user-name', 'header-user-name', 'hero-user-name',
        'cd-reading-candidate-name', 'cd-listening-candidate-name', 'cd-writing-candidate-name', 'cd-speaking-candidate-name'
    ];
    candidateNameIds.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = user.name;
    });

    // Official Candidate ID (e.g. 849201)
    const candId = (849000 + (parseInt(user.id, 10) || 201)).toString();
    ['cd-reading-candidate-id', 'cd-listening-candidate-id', 'cd-writing-candidate-id', 'cd-speaking-candidate-id'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = candId;
    });
    const headerIdEl = document.getElementById('header-user-id');
    if (headerIdEl) headerIdEl.innerText = `ID: ${candId}`;

    ['drawer-user-email', 'sidebar-user-email'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = user.email;
    });

    if (user.target_band) {
        const headerTargetEl = document.getElementById('header-target-band');
        if (headerTargetEl) headerTargetEl.innerText = Number(user.target_band).toFixed(1);
    }

    const setUserNameEl = document.getElementById('set-user-name');
    if (setUserNameEl) setUserNameEl.value = user.name || '';
    const setUserEmailEl = document.getElementById('set-user-email');
    if (setUserEmailEl) setUserEmailEl.value = user.email || '';
}

function handleUserProfileClick() {
    if (currentUser && authToken) {
        openCandidateProfileModal();
    } else {
        openAuthModal('signin');
    }
}

function openCandidateProfileModal() {
    const modal = document.getElementById('modal-candidate-profile');
    if (!modal) return;
    if (!currentUser) {
        openAuthModal('signin');
        return;
    }

    // Candidate initials
    const names = (currentUser.name || 'Candidate').trim().split(/\s+/);
    const initials = names.length > 1
        ? (names[0][0] + names[names.length - 1][0]).toUpperCase()
        : (names[0].substring(0, 2)).toUpperCase();

    const avatarEl = document.getElementById('prof-modal-avatar');
    if (avatarEl) avatarEl.innerText = initials;

    const nameEl = document.getElementById('prof-modal-name');
    if (nameEl) nameEl.innerText = currentUser.name || 'Candidate';

    const emailEl = document.getElementById('prof-modal-email');
    if (emailEl) emailEl.innerText = currentUser.email || '—';

    const candId = (849000 + (parseInt(currentUser.id, 10) || 201)).toString();
    const candIdEl = document.getElementById('prof-modal-cand-id');
    if (candIdEl) candIdEl.innerText = candId;

    const examTypeEl = document.getElementById('prof-modal-exam-type');
    if (examTypeEl) examTypeEl.innerText = `${currentUser.exam_type || (window.appSettings && window.appSettings.examType) || 'Academic'} Module`;

    // Diagnostics snapshot
    const ov = window.appDiagnostics ? window.appDiagnostics.overview : null;
    const isOverallAssessed = ov && ov.is_assessed && ov.overall_band !== null && ov.overall_band !== undefined;

    const overallBandEl = document.getElementById('prof-modal-overall-band');
    if (overallBandEl) {
        if (isOverallAssessed) {
            overallBandEl.innerText = `Band ${ov.overall_band.toFixed(1)}`;
            overallBandEl.className = 'text-lg font-black text-emerald-600 mt-0.5';
        } else {
            overallBandEl.innerText = 'Not yet assessed';
            overallBandEl.className = 'text-sm font-bold text-rose-500 mt-0.5 italic';
        }
    }

    const targetBandEl = document.getElementById('prof-modal-target-band');
    if (targetBandEl) {
        const targetVal = currentUser.target_band || (ov && ov.target_band) || (window.appSettings && window.appSettings.targetBand) || '7.5';
        targetBandEl.innerText = `Band ${Number(targetVal).toFixed(1)}`;
    }

    const streakEl = document.getElementById('prof-modal-streak');
    if (streakEl) {
        const streakDays = ov ? ov.streak_days : 1;
        streakEl.innerText = `${streakDays} Day${streakDays === 1 ? '' : 's'}`;
    }

    const testsCountEl = document.getElementById('prof-modal-tests-count');
    if (testsCountEl) {
        const total = ov ? (ov.total_sessions || 0) : 0;
        testsCountEl.innerText = `${total}`;
    }

    // Sub-skills scores
    const skills = ['listening', 'reading', 'writing', 'speaking'];
    skills.forEach(skill => {
        const el = document.getElementById(`prof-modal-${skill}-band`);
        if (!el) return;
        const score = ov && ov.module_scores ? ov.module_scores[skill] : null;
        if (score !== null && score !== undefined) {
            el.innerText = `Band ${Number(score).toFixed(1)}`;
            el.className = 'font-bold text-emerald-600';
        } else {
            el.innerText = 'Not assessed';
            el.className = 'font-bold text-slate-400 italic';
        }
    });

    modal.classList.remove('hidden');
}

function closeCandidateProfileModal() {
    const modal = document.getElementById('modal-candidate-profile');
    if (modal) modal.classList.add('hidden');
}

function goToSettingsFromProfile() {
    closeCandidateProfileModal();
    if (typeof switchView === 'function') switchView('settings');
}

function switchAccountFromProfile() {
    closeCandidateProfileModal();
    openAuthModal('signin');
}

function logoutFromProfile() {
    closeCandidateProfileModal();
    handleLogout();
}

function openAuthModal(tab = 'signin') {
    const modal = document.getElementById('modal-auth');
    if (!modal) return;
    modal.classList.remove('hidden');
    setAuthTab(tab);
    clearAuthAlert();
}

function closeAuthModal() {
    // Only allow closing if a user is authenticated
    if (!currentUser && !authToken) {
        showAuthAlert('Please sign in or use 1-Click Demo Login to access your practice modules.', 'amber');
        return;
    }
    const modal = document.getElementById('modal-auth');
    if (modal) modal.classList.add('hidden');
    clearAuthAlert();
}

function setAuthTab(tab) {
    const tabSignIn = document.getElementById('tab-auth-signin');
    const tabRegister = document.getElementById('tab-auth-register');
    const formSignIn = document.getElementById('form-signin');
    const formRegister = document.getElementById('form-register');
    clearAuthAlert();

    if (tab === 'signin') {
        if (tabSignIn) tabSignIn.className = 'flex-1 py-2 rounded-lg bg-white text-slate-900 shadow-sm transition-all';
        if (tabRegister) tabRegister.className = 'flex-1 py-2 rounded-lg text-slate-300 hover:text-white transition-all';
        if (formSignIn) formSignIn.classList.remove('hidden');
        if (formRegister) formRegister.classList.add('hidden');
    } else {
        if (tabSignIn) tabSignIn.className = 'flex-1 py-2 rounded-lg text-slate-300 hover:text-white transition-all';
        if (tabRegister) tabRegister.className = 'flex-1 py-2 rounded-lg bg-white text-slate-900 shadow-sm transition-all';
        if (formSignIn) formSignIn.classList.add('hidden');
        if (formRegister) formRegister.classList.remove('hidden');
    }
}

function showAuthAlert(message, type = 'rose') {
    const alertEl = document.getElementById('auth-alert');
    if (!alertEl) return;
    alertEl.className = 'p-3 rounded-xl text-xs font-semibold border';
    if (type === 'emerald') {
        alertEl.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
    } else if (type === 'amber') {
        alertEl.classList.add('bg-amber-50', 'text-amber-700', 'border-amber-200');
    } else {
        alertEl.classList.add('bg-rose-50', 'text-rose-700', 'border-rose-200');
    }
    alertEl.innerText = message;
    alertEl.classList.remove('hidden');
}

function clearAuthAlert() {
    const alertEl = document.getElementById('auth-alert');
    if (alertEl) {
        alertEl.classList.add('hidden');
        alertEl.innerText = '';
    }
}

async function handleSignIn(e) {
    e.preventDefault();
    const email = document.getElementById('signin-email').value.trim();
    const password = document.getElementById('signin-password').value;
    const btn = document.getElementById('btn-signin-submit');

    if (!email || !password) {
        showAuthAlert('Please enter your email and password.');
        return;
    }

    btn.disabled = true;
    btn.innerText = 'Signing in...';

    try {
        const res = await _originalFetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();

        if (!res.ok || data.error) {
            showAuthAlert(data.error || 'Failed to sign in. Please verify your credentials.');
            btn.disabled = false;
            btn.innerText = 'Sign In to Workspace';
            return;
        }

        authToken = data.token;
        localStorage.setItem('ielts_auth_token', authToken);
        updateCurrentUserUI(data.user);

        showAuthAlert(`Welcome back, ${data.user.name}!`, 'emerald');
        setTimeout(async () => {
            closeAuthModal();
            btn.disabled = false;
            btn.innerText = 'Sign In to Workspace';
            if (typeof refreshData === 'function') await refreshData();
            if (typeof loadSettings === 'function') await loadSettings();
            if (typeof loadVocabulary === 'function') await loadVocabulary();
        }, 400);

    } catch (err) {
        showAuthAlert('Network error: ' + err.message);
        btn.disabled = false;
        btn.innerText = 'Sign In to Workspace';
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    const target_band = parseFloat(document.getElementById('reg-target-band').value) || 7.5;
    const exam_type = document.getElementById('reg-exam-type').value || 'Academic';
    const btn = document.getElementById('btn-register-submit');

    if (!name || !email || !password) {
        showAuthAlert('Please fill out all registration fields.');
        return;
    }

    btn.disabled = true;
    btn.innerText = 'Creating account...';

    try {
        const res = await _originalFetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password, target_band, exam_type })
        });
        const data = await res.json();

        if (!res.ok || data.error) {
            showAuthAlert(data.error || 'Failed to create account.');
            btn.disabled = false;
            btn.innerText = 'Create Account & Start Practice';
            return;
        }

        authToken = data.token;
        localStorage.setItem('ielts_auth_token', authToken);
        updateCurrentUserUI(data.user);

        showAuthAlert(`Welcome to IELTS Master, ${data.user.name}! Workspace ready.`, 'emerald');
        setTimeout(async () => {
            closeAuthModal();
            btn.disabled = false;
            btn.innerText = 'Create Account & Start Practice';
            if (typeof refreshData === 'function') await refreshData();
            if (typeof loadSettings === 'function') await loadSettings();
            if (typeof loadVocabulary === 'function') await loadVocabulary();
        }, 500);

    } catch (err) {
        showAuthAlert('Network error: ' + err.message);
        btn.disabled = false;
        btn.innerText = 'Create Account & Start Practice';
    }
}

async function handleDemoLogin() {
    try {
        const res = await _originalFetch(`${API_BASE}/api/auth/demo`);
        const data = await res.json();

        if (data.success && data.token) {
            authToken = data.token;
            localStorage.setItem('ielts_auth_token', authToken);
            updateCurrentUserUI(data.user);
            showAuthAlert('Logged in as Demo Candidate (Alex Morgan)!', 'emerald');
            setTimeout(async () => {
                closeAuthModal();
                if (typeof refreshData === 'function') await refreshData();
                if (typeof loadSettings === 'function') await loadSettings();
                if (typeof loadVocabulary === 'function') await loadVocabulary();
            }, 350);
        }
    } catch (err) {
        showAuthAlert('Failed demo login: ' + err.message);
    }
}

async function handleLogout() {
    closeCandidateProfileModal();
    if (authToken) {
        try {
            await _originalFetch(`${API_BASE}/api/auth/logout`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
        } catch (e) {
            console.warn('Logout notification error:', e);
        }
    }

    authToken = null;
    currentUser = null;
    localStorage.removeItem('ielts_auth_token');
    updateCurrentUserUI(null);

    // Open auth modal
    openAuthModal('signin');
    showAuthAlert('You have signed out. Sign in or switch candidate to access your practice history.', 'amber');
}

async function initAuth() {
    if (authToken) {
        try {
            const res = await _originalFetch(`${API_BASE}/api/auth/me`, {
                headers: { 'Authorization': `Bearer ${authToken}` }
            });
            const data = await res.json();
            if (data.authenticated && data.user) {
                updateCurrentUserUI(data.user);
                return true;
            }
        } catch (e) {
            console.warn('Auth check error:', e);
        }
    }

    // Default to prompt login modal
    openAuthModal('signin');
    return false;
}
// =====================================================================
// IELTS MASTER: SETTINGS & GEMINI CONFIGURATION CONTROLLER
// =====================================================================

async function loadSettings() {
    try {
        const res = await fetch(`${API_BASE}/api/settings`);
        appSettings = await res.json();
        
        const setSidebar = document.getElementById('sidebar-target-band');
        if (setSidebar) setSidebar.innerText = appSettings.target_band || '7.5';
        const mobTarget = document.getElementById('mobile-sidebar-target-band');
        if (mobTarget) mobTarget.innerText = appSettings.target_band || '7.5';
        const headerTarget = document.getElementById('header-target-band');
        if (headerTarget) headerTarget.innerText = appSettings.target_band || '7.5';
        const dashTarget = document.getElementById('dash-target-band');
        if (dashTarget) dashTarget.innerText = appSettings.target_band || '7.5';
        const setTargetInput = document.getElementById('set-target-band');
        if (setTargetInput) setTargetInput.value = appSettings.target_band || 7.5;
        const setTargetVal = document.getElementById('set-target-band-val');
        if (setTargetVal) setTargetVal.innerText = appSettings.target_band || '7.5';
        
        const setExamType = document.getElementById('set-exam-type');
        if (setExamType) setExamType.value = appSettings.exam_type || 'Academic';
        const examTypeBadge = document.getElementById('exam-type-badge');
        if (examTypeBadge) examTypeBadge.innerText = appSettings.exam_type || 'Academic';
        const setExamDate = document.getElementById('set-exam-date');
        if (setExamDate) setExamDate.value = appSettings.exam_date || '';
        const setGeminiModel = document.getElementById('set-gemini-model');
        if (setGeminiModel) setGeminiModel.value = appSettings.gemini_model || 'gemini-3.8-flash';
        
        if (appSettings.exam_date) {
            const dashExamDate = document.getElementById('dash-exam-date');
            if (dashExamDate) dashExamDate.innerText = `Target: ${appSettings.exam_date}`;
        }

        const setUserNameEl = document.getElementById('set-user-name');
        if (setUserNameEl && (appSettings.name || currentUser?.name)) setUserNameEl.value = appSettings.name || currentUser.name;
        const setUserEmailEl = document.getElementById('set-user-email');
        if (setUserEmailEl && (appSettings.email || currentUser?.email)) setUserEmailEl.value = appSettings.email || currentUser.email;

        const pill = document.getElementById('gemini-status-pill');
        if (pill) {
            if (appSettings.has_api_key) {
                pill.className = 'inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700';
                pill.innerText = 'Gemini Live AI Active';
            } else {
                pill.className = 'inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-amber-50 text-amber-700';
                pill.innerText = 'Heuristic Examiner Ready';
            }
        }
    } catch (err) {
        console.error('Failed loading settings:', err);
    }
}

async function saveSettings(e) {
    if (e) e.preventDefault();
    const payload = {
        target_band: parseFloat(document.getElementById('set-target-band').value),
        exam_type: document.getElementById('set-exam-type').value,
        exam_date: document.getElementById('set-exam-date').value,
        gemini_model: document.getElementById('set-gemini-model').value
    };

    const userName = document.getElementById('set-user-name')?.value.trim();
    if (userName) payload.name = userName;

    const keyInput = document.getElementById('set-gemini-key').value.trim();
    if (keyInput) {
        payload.gemini_api_key = keyInput;
    }

    try {
        const res = await fetch(`${API_BASE}/api/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const updated = await res.json();
        if (currentUser && userName) {
            currentUser.name = userName;
            if (typeof updateCurrentUserUI === 'function') updateCurrentUserUI(currentUser);
        }
        alert('Candidate settings and profile saved successfully!');
        await loadSettings();
        if (typeof loadAllAvailableTests === 'function') await loadAllAvailableTests();
        if (typeof loadInitialTests === 'function') await loadInitialTests();
        if (typeof refreshData === 'function') await refreshData();
        if (typeof switchView === 'function') switchView('dashboard');
    } catch (err) {
        alert('Error saving settings: ' + err.message);
    }
}

async function testGeminiConnection() {
    const keyInput = document.getElementById('set-gemini-key');
    const key = keyInput.value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');
    const modelSelect = document.getElementById('set-gemini-model');
    const model = modelSelect.value || 'gemini-3.8-flash';

    if (!key) {
        alert('Please enter your Gemini API Key first.');
        return;
    }

    const testBtn = window.event?.target || document.querySelector("button[onclick='testGeminiConnection()']");
    if (testBtn) {
        testBtn.innerText = 'Testing...';
        testBtn.disabled = true;
    }

    let isSuccess = false;
    let foundModels = [];
    let errorDetail = '';

    // Step 1: Direct Browser Probe (Fastest, zero Python timeout/proxy hurdles)
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);
        const probeUrl = `https://generativelanguage.googleapis.com/v1beta/models?key=${key}`;
        
        const bRes = await fetch(probeUrl, { signal: controller.signal });
        clearTimeout(timeoutId);

        if (bRes.ok) {
            const bData = await bRes.json();
            isSuccess = true;
            if (bData.models) {
                foundModels = bData.models.map(m => m.name.replace('models/', ''));
            }
        } else if (bRes.status === 400 || bRes.status === 403) {
            const errObj = await bRes.json().catch(() => ({}));
            errorDetail = errObj.error?.message || `Google rejected key (HTTP ${bRes.status})`;
        }
    } catch (browserErr) {
        console.warn('Direct browser probe note:', browserErr.message);
    }

    // Step 2: Backend Probe fallback if browser probe didn't resolve
    if (!isSuccess && !errorDetail) {
        try {
            const res = await fetch(`${API_BASE}/api/gemini/test`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: key, model: model })
            });
            const data = await res.json();
            if (data.success) {
                isSuccess = true;
                foundModels = data.models || [];
            } else {
                errorDetail = data.error || 'Connection timed out';
            }
        } catch (backendErr) {
            errorDetail = backendErr.message;
        }
    }

    if (isSuccess) {
        // Save key in localStorage and backend database
        localStorage.setItem('gemini_api_key', key);
        appSettings.gemini_api_key = key;
        appSettings.has_api_key = true;

        // Update UI pill
        const pill = document.getElementById('gemini-status-pill');
        if (pill) {
            pill.className = 'inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-emerald-50 text-emerald-700';
            pill.innerText = 'Gemini Live AI Active';
        }

        alert('✅ Success! Google Gemini API connected successfully.\nYour API key is active and ready for live examiner evaluations.');
        
        // Auto-save settings
        await saveSettings();
    } else {
        alert('Gemini connection notice:\n' + (errorDetail || 'Connection timed out. Please verify your internet connection or API key.'));
    }

    if (testBtn) {
        testBtn.innerText = 'Test Key';
        testBtn.disabled = false;
    }
}
// =====================================================================
// IELTS MASTER: DIAGNOSTICS & DASHBOARD CONTROLLER
// =====================================================================

async function loadDiagnostics() {
    try {
        const res = await fetch(`${API_BASE}/api/diagnostics`);
        appDiagnostics = await res.json();
        const ov = appDiagnostics.overview;
        const diag = appDiagnostics.diagnostics;
        const isOverallAssessed = ov.is_assessed && ov.overall_band !== null && ov.overall_band !== undefined;

        // Overall Cards
        const dashBandEl = document.getElementById('dash-overall-band');
        const dashMaxEl = document.getElementById('dash-overall-max');
        const dashTrendEl = document.getElementById('dash-overall-trend-badge');
        const headerBandEl = document.getElementById('header-overall-band');
        const mobBandEl = document.getElementById('mobile-overall-band');

        if (isOverallAssessed) {
            dashBandEl.innerText = ov.overall_band.toFixed(1);
            dashBandEl.className = 'text-4xl font-extrabold tracking-tight text-white';
            if (dashMaxEl) dashMaxEl.classList.remove('hidden');
            if (headerBandEl) headerBandEl.innerText = `Band ${ov.overall_band.toFixed(1)}`;
            if (mobBandEl) mobBandEl.innerText = `Band ${ov.overall_band.toFixed(1)}`;

            // Dynamic Trend Indicator: Improved vs Declined vs Stable
            if (dashTrendEl) {
                if (ov.overall_trend === 'improved') {
                    dashTrendEl.innerText = `↑ +${ov.overall_delta} Improved`;
                    dashTrendEl.className = 'text-[10px] bg-emerald-500/30 text-emerald-100 border border-emerald-400/30 px-2 py-0.5 rounded-full font-bold';
                } else if (ov.overall_trend === 'declined') {
                    dashTrendEl.innerText = `↓ ${ov.overall_delta} Declined`;
                    dashTrendEl.className = 'text-[10px] bg-rose-500/30 text-rose-100 border border-rose-400/30 px-2 py-0.5 rounded-full font-bold';
                } else if (ov.overall_trend === 'stable') {
                    dashTrendEl.innerText = '→ Stable';
                    dashTrendEl.className = 'text-[10px] bg-white/20 text-indigo-100 px-2 py-0.5 rounded-full font-semibold';
                } else {
                    dashTrendEl.innerText = '● Baseline Set';
                    dashTrendEl.className = 'text-[10px] bg-emerald-500/20 text-emerald-200 border border-emerald-400/20 px-2 py-0.5 rounded-full font-semibold';
                }
            }
        } else {
            dashBandEl.innerText = 'Not yet assessed';
            dashBandEl.className = 'text-2xl font-bold tracking-tight text-amber-200/90 italic';
            if (dashMaxEl) dashMaxEl.classList.add('hidden');
            if (headerBandEl) headerBandEl.innerText = 'Not yet assessed';
            if (mobBandEl) mobBandEl.innerText = 'Not assessed';
            if (dashTrendEl) {
                dashTrendEl.innerText = 'Not yet assessed';
                dashTrendEl.className = 'text-[10px] bg-white/20 px-2 py-0.5 rounded-full font-semibold';
            }
        }

        const streakDays = document.getElementById('dash-streak-days');
        if (streakDays) streakDays.innerText = ov.streak_days;
        const sideStreak = document.getElementById('sidebar-streak-days');
        if (sideStreak) sideStreak.innerText = ov.streak_days;
        const totalSess = document.getElementById('dash-total-sessions');
        if (totalSess) totalSess.innerText = ov.total_sessions;
        const totalMins = document.getElementById('dash-total-mins');
        if (totalMins) totalMins.innerText = ov.total_minutes;

        // Gap calculation
        const gapTextEl = document.getElementById('dash-band-gap-text');
        if (gapTextEl) {
            if (!isOverallAssessed) {
                gapTextEl.innerText = `Target: Band ${ov.target_band} • Complete practice tests to establish your baseline`;
            } else if (ov.target_achieved) {
                gapTextEl.innerText = '🎉 Target band score achieved!';
            } else {
                const gap = ov.band_gap;
                const moduleInfo = ov.assessed_count < 4 ? ` (${ov.assessed_count}/4 modules assessed)` : '';
                gapTextEl.innerText = `${gap > 0 ? '+' + gap : gap} band needed to reach target ${ov.target_band}${moduleInfo}`;
            }
        }

        // Progress bar in sidebar and dashboard
        const pct = isOverallAssessed
            ? Math.min(100, Math.max(10, Math.round((ov.overall_band / ov.target_band) * 100)))
            : 0;
        const sideProg = document.getElementById('sidebar-progress-bar');
        if (sideProg) sideProg.style.width = `${pct}%`;
        const dashProg = document.getElementById('dash-target-progress');
        if (dashProg) dashProg.style.width = `${pct}%`;
        const mobProgEl = document.getElementById('mobile-sidebar-progress-bar');
        if (mobProgEl) mobProgEl.style.width = `${pct}%`;

        // Update module details & badges helper
        const updateModuleUI = (modKey, badgeId, mobBadgeId, diagBandId, diagTrendId, diagWeakId, diagAdviceId, defaultWeakText, adviceText) => {
            const modMeta = ov.module_details ? ov.module_details[modKey] : null;
            const score = ov.module_scores[modKey];
            const isAssessed = modMeta ? modMeta.status === 'assessed' : (score !== null && score !== undefined);

            const badgeEl = document.getElementById(badgeId);
            const mobBadgeEl = document.getElementById(mobBadgeId);
            const diagBandEl = document.getElementById(diagBandId);
            const diagTrendEl = document.getElementById(diagTrendId);
            const diagWeakEl = document.getElementById(diagWeakId);
            const diagAdviceEl = document.getElementById(diagAdviceId);

            if (isAssessed) {
                const trendIcon = modMeta && modMeta.trend === 'improved' ? ' ↑' : (modMeta && modMeta.trend === 'declined' ? ' ↓' : '');
                const scoreText = `Band ${score.toFixed(1)}${trendIcon}`;

                if (badgeEl) {
                    badgeEl.innerText = scoreText;
                    badgeEl.className = 'px-2 py-0.5 text-xs font-semibold rounded-full bg-slate-800 text-brand-300 font-mono border border-slate-700';
                }
                if (mobBadgeEl) {
                    mobBadgeEl.innerText = scoreText;
                    mobBadgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-brand-50 text-brand-700 font-mono border border-brand-200';
                }
                if (diagBandEl) {
                    diagBandEl.innerText = `Band ${score.toFixed(1)}`;
                    diagBandEl.className = 'font-bold text-xs px-2 py-0.5 rounded-full bg-brand-100 text-brand-800';
                }
                if (diagTrendEl && modMeta) {
                    diagTrendEl.classList.remove('hidden');
                    if (modMeta.trend === 'improved') {
                        diagTrendEl.innerText = `↑ +${modMeta.delta} Improved`;
                        diagTrendEl.className = 'text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800';
                    } else if (modMeta.trend === 'declined') {
                        diagTrendEl.innerText = `↓ ${modMeta.delta} Declined`;
                        diagTrendEl.className = 'text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800';
                    } else if (modMeta.trend === 'stable') {
                        diagTrendEl.innerText = '→ Stable';
                        diagTrendEl.className = 'text-[10px] font-semibold px-1.5 py-0.5 rounded bg-slate-200 text-slate-700';
                    } else {
                        diagTrendEl.innerText = '● Baseline Set';
                        diagTrendEl.className = 'text-[10px] font-semibold px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-700';
                    }
                }
                if (diagWeakEl) {
                    diagWeakEl.innerText = defaultWeakText;
                    diagWeakEl.className = 'text-xs font-bold text-rose-600 mb-2';
                }
            } else {
                if (badgeEl) {
                    badgeEl.innerText = 'Not assessed';
                    badgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-slate-100 text-slate-500';
                }
                if (mobBadgeEl) {
                    mobBadgeEl.innerText = 'Not assessed';
                    mobBadgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-slate-100 text-slate-500';
                }
                if (diagBandEl) {
                    diagBandEl.innerText = 'Not assessed';
                    diagBandEl.className = 'font-bold text-xs bg-slate-200/70 text-slate-600 px-2 py-0.5 rounded-full';
                }
                if (diagTrendEl) diagTrendEl.classList.add('hidden');
                if (diagWeakEl) {
                    diagWeakEl.innerText = 'Not yet assessed';
                    diagWeakEl.className = 'text-xs font-semibold text-slate-500 mb-2';
                }
            }

            if (diagAdviceEl) diagAdviceEl.innerText = adviceText;
        };

        // Update each module
        updateModuleUI('listening', 'badge-listening-band', 'mobile-badge-listening-band', 'dash-diag-l-band', 'dash-diag-l-trend', 'dash-diag-l-weakest', 'dash-diag-l-advice', diag.listening.weakest_question_type || 'Multiple Choice', diag.listening.key_advice || '');
        updateModuleUI('reading', 'badge-reading-band', 'mobile-badge-reading-band', 'dash-diag-r-band', 'dash-diag-r-trend', 'dash-diag-r-weakest', 'dash-diag-r-advice', diag.reading.weakest_question_type || 'True / False / Not Given', diag.reading.key_advice || '');
        updateModuleUI('writing', 'badge-writing-band', 'mobile-badge-writing-band', 'dash-diag-w-band', 'dash-diag-w-trend', 'dash-diag-w-bottleneck', 'dash-diag-w-advice', diag.writing.bottleneck_criterion || 'Grammar Range & Accuracy', diag.writing.key_advice || '');
        updateModuleUI('speaking', 'badge-speaking-band', 'mobile-badge-speaking-band', 'dash-diag-s-band', 'dash-diag-s-trend', 'dash-diag-s-bottleneck', 'dash-diag-s-advice', diag.speaking.bottleneck_criterion || 'Fluency & Coherence', diag.speaking.key_advice || '');

        // Render Action Priorities
        renderPriorities(appDiagnostics.priorities);

        // Render Charts
        renderCharts(ov.module_scores, ov.target_band, appDiagnostics.chart_data);

    } catch (err) {
        console.error('Failed loading diagnostics:', err);
    }
}

function renderPriorities(priorities) {
    const container = document.getElementById('dash-priorities-list');
    if (!container) return;
    if (!priorities || priorities.length === 0) {
        container.innerHTML = '<div class="text-xs text-slate-400">Complete practice tests across modules to generate your custom AI improvement roadmap.</div>';
        return;
    }

    container.innerHTML = priorities.map((p, idx) => `
        <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/70 hover:bg-white hover:border-brand-200 transition-all">
            <div class="flex items-start gap-3">
                <span class="w-6 h-6 rounded-full ${p.urgency === 'High' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'} flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                    ${idx + 1}
                </span>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs font-bold text-slate-800">${p.title}</span>
                        <span class="text-[10px] font-semibold px-2 py-0.5 rounded ${p.status === 'not_assessed' ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : (p.urgency === 'High' ? 'bg-rose-50 text-rose-600' : 'bg-amber-50 text-amber-600')}">
                            ${p.status === 'not_assessed' ? 'Baseline Pending' : p.urgency + ' Priority'}
                        </span>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-0.5 leading-relaxed">${p.description}</p>
                </div>
            </div>
            <button onclick="switchView('${p.target_route}')" class="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-brand-50 hover:text-brand-700 hover:border-brand-200 text-xs font-semibold shrink-0 transition-colors">
                ${p.action_label} →
            </button>
        </div>
    `).join('');
}

function renderCharts(moduleScores, targetBand, chartData) {
    // 1. Radar Chart: 4-Segment Competency
    const radarEl = document.getElementById('radarChart');
    if (radarEl) {
        const radarCtx = radarEl.getContext('2d');
        if (radarChartInstance) radarChartInstance.destroy();

        const lScore = moduleScores.listening || 0;
        const rScore = moduleScores.reading || 0;
        const wScore = moduleScores.writing || 0;
        const sScore = moduleScores.speaking || 0;
        const anyAssessed = lScore > 0 || rScore > 0 || wScore > 0 || sScore > 0;

        radarChartInstance = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Listening', 'Reading', 'Writing', 'Speaking'],
                datasets: [
                    {
                        label: anyAssessed ? 'Current Assessed Band' : 'Current Band (Not yet assessed)',
                        data: [lScore, rScore, wScore, sScore],
                        backgroundColor: anyAssessed ? 'rgba(99, 102, 241, 0.2)' : 'rgba(148, 163, 184, 0.1)',
                        borderColor: anyAssessed ? '#4f46e5' : '#94a3b8',
                        pointBackgroundColor: anyAssessed ? '#4f46e5' : '#94a3b8',
                        borderDash: anyAssessed ? [] : [4, 4],
                        borderWidth: 2
                    },
                    {
                        label: 'Target Goal',
                        data: [targetBand, targetBand, targetBand, targetBand],
                        backgroundColor: 'rgba(16, 185, 129, 0.05)',
                        borderColor: '#10b981',
                        borderDash: [4, 4],
                        pointBackgroundColor: '#10b981',
                        borderWidth: 1.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        min: 0.0,
                        max: 9.0,
                        ticks: { stepSize: 1.5, font: { size: 10 } }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                if (context.datasetIndex === 0) {
                                    const val = context.raw;
                                    return val > 0 ? `Current Band: ${val.toFixed(1)}` : 'Current Band: Not yet assessed';
                                }
                                return `Target Goal: Band ${context.raw}`;
                            }
                        }
                    },
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
                }
            }
        });
    }

    // 2. Progression Timeline Line Chart
    const trendEl = document.getElementById('trendChart');
    if (trendEl) {
        const trendCtx = trendEl.getContext('2d');
        if (trendChartInstance) trendChartInstance.destroy();

        const hasAttempts = chartData && chartData.dates && chartData.dates.length > 0;
        const dates = hasAttempts ? chartData.dates : ['Baseline'];
        const listeningData = hasAttempts ? chartData.listening : [null];
        const readingData = hasAttempts ? chartData.reading : [null];
        const writingData = hasAttempts ? chartData.writing : [null];
        const speakingData = hasAttempts ? chartData.speaking : [null];

        trendChartInstance = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    { label: 'Listening', data: listeningData, borderColor: '#6366f1', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Reading', data: readingData, borderColor: '#0ea5e9', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Writing', data: writingData, borderColor: '#f59e0b', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Speaking', data: speakingData, borderColor: '#10b981', tension: 0.3, fill: false, spanGaps: true }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 4.0, max: 9.0, ticks: { stepSize: 0.5, font: { size: 10 } } },
                    x: { ticks: { font: { size: 10 } } }
                },
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const val = context.raw;
                                return val !== null && val !== undefined ? `${context.dataset.label}: Band ${val.toFixed(1)}` : `${context.dataset.label}: Not yet assessed`;
                            }
                        }
                    }
                }
            }
        });
    }
}

async function confirmResetAttempts() {
    if (!confirm('Are you sure you want to reset all practice test attempts for this candidate account?\n\nYour scores across all 4 segments will return to "Not yet assessed", allowing you to start fresh.')) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/attempts/reset`, { method: 'POST' });
        const data = await res.json();
        alert('✅ ' + (data.message || 'Practice attempts have been reset to Not yet assessed.'));
        if (typeof refreshData === 'function') await refreshData();
        if (typeof switchView === 'function') switchView('dashboard');
    } catch (err) {
        alert('Error resetting attempts: ' + err.message);
    }
}

async function loadRecentAttempts() {
    try {
        const res = await fetch(`${API_BASE}/api/attempts?limit=10`);
        const attempts = await res.json();
        const tbody = document.getElementById('dash-attempts-tbody');
        if (!tbody) return;

        if (!attempts || attempts.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="p-5 text-center text-slate-400">No practice attempts recorded yet. Choose a module above to get started!</td></tr>`;
            return;
        }

        const moduleColors = {
            listening: 'bg-indigo-50 text-indigo-700',
            reading: 'bg-sky-50 text-sky-700',
            writing: 'bg-amber-50 text-amber-700',
            speaking: 'bg-emerald-50 text-emerald-700'
        };

        tbody.innerHTML = attempts.map(att => {
            const dateStr = att.created_at ? att.created_at.substring(0, 10) : 'Today';
            const mod = att.module.toLowerCase();
            const colorClass = moduleColors[mod] || 'bg-slate-100 text-slate-700';

            // Key metric summary
            let metricText = '';
            if (mod === 'listening' || mod === 'reading') {
                const raw = att.criterion_scores?.raw_score ?? 0;
                const tot = att.criterion_scores?.total ?? 10;
                metricText = `Raw Score: ${raw}/${tot}`;
            } else if (mod === 'writing') {
                const ta = att.criterion_scores?.task_achievement?.band ?? 6.0;
                const gr = att.criterion_scores?.grammatical_range_accuracy?.band ?? 6.0;
                metricText = `TA: ${ta} | GRA: ${gr}`;
            } else if (mod === 'speaking') {
                const fc = att.criterion_scores?.fluency_coherence?.band ?? 6.0;
                metricText = `Fluency: ${fc} | Lex: ${att.criterion_scores?.lexical_resource?.band ?? 6.5}`;
            }

            return `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-3.5 pl-5 text-slate-500">${dateStr}</td>
                    <td class="p-3.5">
                        <span class="px-2 py-0.5 rounded-full font-semibold uppercase text-[10px] ${colorClass}">
                            ${att.module}
                        </span>
                    </td>
                    <td class="p-3.5 font-medium text-slate-800 max-w-[200px] truncate">${att.test_title || att.test_id}</td>
                    <td class="p-3.5 font-bold text-slate-900">
                        <span class="px-2 py-0.5 rounded bg-slate-100">Band ${att.band_score.toFixed(1)}</span>
                    </td>
                    <td class="p-3.5 text-slate-500 font-mono text-[11px]">${metricText}</td>
                    <td class="p-3.5 pr-5 text-right">
                        <button onclick='viewAttemptDetails(${JSON.stringify(att).replace(/'/g, "&#39;")})' class="text-brand-600 hover:text-brand-800 font-semibold text-xs">
                            Review AI Critique →
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error('Failed loading attempts:', err);
    }
}

function viewAttemptDetails(att) {
    if (att.module === 'writing') {
        if (typeof renderWritingReport === 'function') renderWritingReport(att.ai_feedback);
        if (typeof switchView === 'function') switchView('writing');
        const rEl = document.getElementById('writing-report-container');
        if (rEl) rEl.scrollIntoView({ behavior: 'smooth' });
    } else if (att.module === 'speaking') {
        if (typeof renderSpeakingReport === 'function') renderSpeakingReport(att.ai_feedback);
        if (typeof switchView === 'function') switchView('speaking');
        const rEl = document.getElementById('speaking-report-container');
        if (rEl) rEl.scrollIntoView({ behavior: 'smooth' });
    } else {
        alert(`Attempt Details for ${att.module.toUpperCase()}:\nBand Score: ${att.band_score}\n${JSON.stringify(att.criterion_scores, null, 2)}`);
    }
}
// =====================================================================
// IELTS MASTER: 480 CAMBRIDGE TEST CATALOG & RANDOMIZER
// =====================================================================

async function loadAllAvailableTests() {
    try {
        const modules = ['reading', 'listening', 'writing', 'speaking'];
        const examType = appSettings.exam_type || currentUser?.exam_type || 'Academic';
        await Promise.all(modules.map(async (mod) => {
            const res = await fetch(`${API_BASE}/api/tests?module=${mod}&type=${encodeURIComponent(examType)}`);
            const data = await res.json();
            availableTests[mod] = data;
            populateTestDropdown(mod, data);
        }));
    } catch (err) {
        console.error('Failed loading tests catalog:', err);
    }
}

function populateTestDropdown(mod, tests) {
    const selectEl = document.getElementById(`select-${mod}-test`);
    const badgeEl = document.getElementById(`badge-${mod}-count`);
    if (badgeEl) {
        badgeEl.innerText = `${tests.length} ${mod === 'writing' ? 'Tasks' : 'Sets'}`;
    }
    if (!selectEl) return;

    selectEl.innerHTML = tests.map(t => {
        let label = t.title;
        if (label.length > 55) label = label.substring(0, 52) + '...';
        return `<option value="${t.id}">${t.id}: ${label}</option>`;
    }).join('');
}

async function loadRandomReadingTest(shouldSwitchView = true) {
    try {
        const examType = appSettings.exam_type || currentUser?.exam_type || 'Academic';
        const excludeParam = lastExitedTestId.reading ? `&exclude=${encodeURIComponent(lastExitedTestId.reading)}` : '';
        const res = await fetch(`${API_BASE}/api/tests/random?module=reading&type=${encodeURIComponent(examType)}${excludeParam}`);
        const test = await res.json();
        if (test && test.id) {
            await loadReadingTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('reading', true);
            return;
        }
    } catch (err) {
        console.warn('API random reading fetch fallback:', err);
    }
    if (availableTests.reading && availableTests.reading.length > 0) {
        const pool = availableTests.reading.filter(t => t.id !== lastExitedTestId.reading);
        const candidates = pool.length > 0 ? pool : availableTests.reading;
        const randomItem = candidates[Math.floor(Math.random() * candidates.length)];
        await loadReadingTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('reading', true);
    }
}

async function loadRandomListeningTest(shouldSwitchView = true) {
    try {
        const excludeParam = lastExitedTestId.listening ? `&exclude=${encodeURIComponent(lastExitedTestId.listening)}` : '';
        const res = await fetch(`${API_BASE}/api/tests/random?module=listening${excludeParam}`);
        const test = await res.json();
        if (test && test.id) {
            await loadListeningTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('listening', true);
            return;
        }
    } catch (err) {
        console.warn('API random listening fetch fallback:', err);
    }
    if (availableTests.listening && availableTests.listening.length > 0) {
        const pool = availableTests.listening.filter(t => t.id !== lastExitedTestId.listening);
        const candidates = pool.length > 0 ? pool : availableTests.listening;
        const randomItem = candidates[Math.floor(Math.random() * candidates.length)];
        await loadListeningTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('listening', true);
    }
}

async function loadRandomWritingTask(shouldSwitchView = true) {
    try {
        const examType = appSettings.exam_type || currentUser?.exam_type || 'Academic';
        const excludeParam = lastExitedTestId.writing ? `&exclude=${encodeURIComponent(lastExitedTestId.writing)}` : '';
        const res = await fetch(`${API_BASE}/api/tests/random?module=writing&type=${encodeURIComponent(examType)}${excludeParam}`);
        const test = await res.json();
        if (test && test.id) {
            await loadWritingTask(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('writing', true);
            return;
        }
    } catch (err) {
        console.warn('API random writing fetch fallback:', err);
    }
    if (availableTests.writing && availableTests.writing.length > 0) {
        const pool = availableTests.writing.filter(t => t.id !== lastExitedTestId.writing);
        const candidates = pool.length > 0 ? pool : availableTests.writing;
        const randomItem = candidates[Math.floor(Math.random() * candidates.length)];
        await loadWritingTask(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('writing', true);
    }
}

async function loadRandomSpeakingTest(shouldSwitchView = true) {
    try {
        const excludeParam = lastExitedTestId.speaking ? `&exclude=${encodeURIComponent(lastExitedTestId.speaking)}` : '';
        const res = await fetch(`${API_BASE}/api/tests/random?module=speaking${excludeParam}`);
        const test = await res.json();
        if (test && test.id) {
            await loadSpeakingTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('speaking', true);
            return;
        }
    } catch (err) {
        console.warn('API random speaking fetch fallback:', err);
    }
    if (availableTests.speaking && availableTests.speaking.length > 0) {
        const pool = availableTests.speaking.filter(t => t.id !== lastExitedTestId.speaking);
        const candidates = pool.length > 0 ? pool : availableTests.speaking;
        const randomItem = candidates[Math.floor(Math.random() * candidates.length)];
        await loadSpeakingTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('speaking', true);
    }
}

async function switchWritingTaskType(targetType) {
    if (!availableTests.writing || availableTests.writing.length === 0) return;
    const taskKeyword = targetType === 1 ? 'Task 1' : 'Task 2';
    const matching = availableTests.writing.filter(t => t.title && t.title.includes(taskKeyword));
    if (matching.length > 0) {
        let picked = null;
        if (currentWritingTask && currentWritingTask.id) {
            const prefix = currentWritingTask.id.startsWith('GTW-') ? 'GTW-' : 'W-';
            const num = parseInt(currentWritingTask.id.replace(prefix, ''), 10);
            if (!isNaN(num)) {
                const pairedNum = (num % 2 !== 0) ? num + 1 : num - 1;
                const pairedId = `${prefix}${String(pairedNum).padStart(2, '0')}`;
                picked = matching.find(t => t.id === pairedId);
            }
        }
        if (!picked) {
            picked = matching[Math.floor(Math.random() * matching.length)];
        }
        await loadWritingTask(picked.id);
    }
}

async function loadInitialTests() {
    await loadAllAvailableTests();
    // Automatically assign fresh randomized Cambridge sets across all 4 modules
    await Promise.allSettled([
        loadRandomListeningTest(false),
        loadRandomReadingTest(false),
        loadRandomWritingTask(false),
        loadRandomSpeakingTest(false)
    ]);
    if (typeof pauseAllExamTimers === 'function') pauseAllExamTimers();
    if (typeof resetListeningTimer === 'function') resetListeningTimer();
    if (typeof resetReadingTimer === 'function') resetReadingTimer();
    if (typeof resetWritingTimer === 'function') resetWritingTimer();
    if (typeof resetOverallSpeakingTimer === 'function') resetOverallSpeakingTimer();
}
// =====================================================================
// IELTS MASTER: HIGH-DEFINITION AUDIO ENGINE (GEMINI NEURAL AI + SYSTEM NATURAL VOICES)
// =====================================================================

function initAudioEngine() {
    const savedEngine = localStorage.getItem('ielts_audio_engine');
    if (savedEngine) currentAudioEngine = savedEngine;

    const savedPersona = localStorage.getItem('ielts_gemini_persona');
    if (savedPersona) currentGeminiPersona = savedPersona;

    const savedBrowserVoice = localStorage.getItem('ielts_browser_voice');
    if (savedBrowserVoice) selectedBrowserVoiceURI = savedBrowserVoice;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => {
            loadAndRankVoices();
        };
        loadAndRankVoices();
        setTimeout(loadAndRankVoices, 100);
        setTimeout(loadAndRankVoices, 300);
        setTimeout(loadAndRankVoices, 800);
        setTimeout(loadAndRankVoices, 1500);
    }
    syncVoiceUI();
}

function pcm16ToWavBlob(base64Pcm, sampleRate = 24000) {
    const binary = atob(base64Pcm);
    const pcmLen = binary.length;
    const buffer = new ArrayBuffer(44 + pcmLen);
    const view = new DataView(buffer);

    const writeStr = (offset, str) => {
        for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
    };

    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + pcmLen, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // Mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // Byte rate (sampleRate * 1 channel * 2 bytes/sample)
    view.setUint16(32, 2, true);  // Block align
    view.setUint16(34, 16, true); // 16 bits
    writeStr(36, 'data');
    view.setUint32(40, pcmLen, true);

    const pcmView = new Uint8Array(buffer, 44);
    for (let i = 0; i < pcmLen; i++) {
        pcmView[i] = binary.charCodeAt(i);
    }
    return new Blob([buffer], { type: 'audio/wav' });
}

function loadAndRankVoices() {
    if (!('speechSynthesis' in window)) return;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return;

    const scored = voices.map(v => {
        let score = 0;
        const name = v.name.toLowerCase();
        const lang = v.lang.toLowerCase();

        // Demote known robotic/metallic synthesizers heavily
        const robotic = [
            'bad news', 'bahh', 'bells', 'boing', 'bubbles', 'cellos',
            'good news', 'jester', 'junior', 'organ', 'superstar',
            'trinoids', 'whisper', 'zarvox', 'compact', 'wobble', 'deranged', 'hysterical'
        ];
        if (robotic.some(r => name.includes(r))) score -= 2000;

        // Neural, Online, Enhanced, Siri, Google (ultra-realistic natural voices)
        if (name.includes('natural') || name.includes('online')) score += 800;
        if (name.includes('google')) score += 700;
        if (name.includes('enhanced') || name.includes('premium')) score += 600;
        if (name.includes('siri') || name.includes('oliver') || name.includes('stephanie') || name.includes('martha') || name.includes('arthur') || name.includes('serena') || name.includes('kate') || name.includes('daniel')) score += 500;

        // Preferred IELTS accents
        if (lang.includes('en-gb') || lang.includes('en_gb')) score += 350;
        else if (lang.includes('en-au') || lang.includes('en_au')) score += 250;
        else if (lang.includes('en-ca') || lang.includes('en-nz') || lang.includes('en-ie')) score += 200;
        else if (lang.includes('en-us') || lang.includes('en_us')) score += 150;
        else if (lang.startsWith('en')) score += 50;
        else score -= 1000;

        return { voice: v, score, name: v.name, lang: v.lang, voiceURI: v.voiceURI };
    });

    scored.sort((a, b) => b.score - a.score);
    availableBrowserVoices = scored.filter(s => s.score > -500);
    bestNaturalVoice = availableBrowserVoices.length > 0 ? availableBrowserVoices[0].voice : null;

    populateAllVoiceSelectors();
}

function populateAllVoiceSelectors(force = false) {
    if (!('speechSynthesis' in window)) return;
    const listeningSel = document.getElementById('select-listening-voice');
    const speakingSel = document.getElementById('select-speaking-persona');
    const settingsBrowserSel = document.getElementById('set-browser-voice');

    if (!force && voicesPopulatedAlready && availableBrowserVoices.length > 0) {
        return;
    }

    // 1. Gemini AI Studio Personas
    const geminiGroup = `
    <optgroup label="🌟 Gemini AI Studio Neural Personas">
        <option value="gemini:Puck">👨‍🏫 Puck (Natural British - Cambridge Standard)</option>
        <option value="gemini:Aoede">👩‍🏫 Aoede (Expressive British / Academic)</option>
        <option value="gemini:Charon">👨‍💼 Charon (Senior Cambridge Examiner - Deep)</option>
        <option value="gemini:Kore">👩‍💼 Kore (Calm & Clear Professional)</option>
        <option value="gemini:Fenrir">🎙️ Fenrir (Authoritative Deep Male)</option>
    </optgroup>
    `;

    // 2. High-Def System / Browser Voices (Grouped by Region/Accent)
    const gbOptions = [];
    const auOptions = [];
    const usOptions = [];
    const otherOptions = [];

    availableBrowserVoices.forEach(item => {
        const lang = (item.lang || '').toLowerCase();
        const label = `${item.name} (${item.lang})`;
        const val = `browser:${item.voiceURI || item.name}`;

        if (lang.includes('en-gb') || lang.includes('en_gb')) {
            gbOptions.push(`<option value="${val}">🇬🇧 ${label}</option>`);
        } else if (lang.includes('en-au') || lang.includes('en_au') || lang.includes('en-nz')) {
            auOptions.push(`<option value="${val}">🇦🇺 ${label}</option>`);
        } else if (lang.includes('en-us') || lang.includes('en_us') || lang.includes('en-ca')) {
            usOptions.push(`<option value="${val}">🇺🇸 ${label}</option>`);
        } else {
            otherOptions.push(`<option value="${val}">🎙️ ${label}</option>`);
        }
    });

    let systemGroup = '';
    if (gbOptions.length > 0) {
        systemGroup += `<optgroup label="🇬🇧 British System Voices (Cambridge Standard)">${gbOptions.join('')}</optgroup>`;
    }
    if (auOptions.length > 0) {
        systemGroup += `<optgroup label="🇦🇺 Australian / Kiwi Voices">${auOptions.join('')}</optgroup>`;
    }
    if (usOptions.length > 0) {
        systemGroup += `<optgroup label="🇺🇸 North American Voices">${usOptions.join('')}</optgroup>`;
    }
    if (otherOptions.length > 0) {
        systemGroup += `<optgroup label="🎙️ Other Natural System Voices">${otherOptions.join('')}</optgroup>`;
    }

    const defaultAuto = `<optgroup label="⚡ Quick Preset"><option value="browser:auto">⚡ Auto-Select Best Cambridge Voice</option></optgroup>`;
    const fullHtml = defaultAuto + geminiGroup + systemGroup;

    if (listeningSel) listeningSel.innerHTML = fullHtml;
    if (speakingSel) speakingSel.innerHTML = fullHtml;

    if (settingsBrowserSel) {
        let bHtml = '<option value="">Auto-Detect Best Natural Voice (Recommended)</option>';
        availableBrowserVoices.forEach(item => {
            bHtml += `<option value="${item.voiceURI || item.name}">${item.name} (${item.lang}) - ${item.score >= 500 ? '🌟 Ultra-Realistic' : 'Natural'}</option>`;
        });
        settingsBrowserSel.innerHTML = bHtml;
        if (selectedBrowserVoiceURI) settingsBrowserSel.value = selectedBrowserVoiceURI;
    }

    if (availableBrowserVoices.length > 0) {
        voicesPopulatedAlready = true;
    }
    syncVoiceUI();
}

function populateBrowserVoiceDropdown() {
    populateAllVoiceSelectors(true);
}

function resolveSpeechParameters(engine, persona, browserVoiceURI) {
    // 1. If explicit browser voice is chosen
    if (engine === 'browser' && browserVoiceURI && browserVoiceURI !== 'auto') {
        const found = availableBrowserVoices.find(v => v.voiceURI === browserVoiceURI || v.name === browserVoiceURI);
        if (found) {
            return {
                voice: found.voice,
                pitch: 1.0,
                rate: 1.0,
                name: found.name,
                accent: found.lang
            };
        }
    }

    // 2. Persona mapping to distinct acoustic profiles & voices
    const femaleKeywords = ['female', 'serena', 'stephanie', 'karen', 'samantha', 'martha', 'victoria', 'moira', 'fiona', 'kate', 'susan', 'zira', 'flo', 'sandy', 'shelley', 'grandma', 'tara', 'tessa', 'kathy', 'alice'];
    const maleKeywords = ['male', 'daniel', 'oliver', 'arthur', 'george', 'alex', 'david', 'russell', 'lee', 'rishi', 'eddy', 'reed', 'rocko', 'grandpa', 'fred', 'albert', 'ralph', 'tom'];

    const femaleVoices = availableBrowserVoices.filter(v => femaleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
    const maleVoices = availableBrowserVoices.filter(v => maleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
    const pool = availableBrowserVoices.length > 0 ? availableBrowserVoices : [];

    const getVoice = (preferredList, fallbackIdx = 0) => {
        if (preferredList && preferredList.length > 0) return preferredList[0].voice;
        if (pool.length > fallbackIdx) return pool[fallbackIdx].voice;
        return bestNaturalVoice;
    };

    const getVoice2 = (preferredList, fallbackIdx = 1) => {
        if (preferredList && preferredList.length > 1) return preferredList[1].voice;
        if (preferredList && preferredList.length > 0) return preferredList[0].voice;
        if (pool.length > fallbackIdx) return pool[fallbackIdx].voice;
        return bestNaturalVoice;
    };

    if (persona === 'Aoede') {
        // Expressive British Female Academic
        const voice = getVoice(femaleVoices, 1);
        return {
            voice,
            pitch: 1.25, // Noticeably brighter, expressive female academic pitch
            rate: 1.02,
            name: voice ? `${voice.name} (Aoede Academic Female)` : 'Aoede Academic Female'
        };
    } else if (persona === 'Charon') {
        // Senior Cambridge Examiner (Deep, authoritative, deliberate cadence)
        const voice = getVoice(maleVoices, 0);
        return {
            voice,
            pitch: 0.75, // Noticeably deeper, authoritative pitch
            rate: 0.88,  // Deliberate examiner pacing
            name: voice ? `${voice.name} (Charon Senior Examiner)` : 'Charon Senior Examiner'
        };
    } else if (persona === 'Kore') {
        // Calm & Professional Female
        const voice = getVoice2(femaleVoices, 2);
        return {
            voice,
            pitch: 1.08,
            rate: 0.95,
            name: voice ? `${voice.name} (Kore Calm Professional)` : 'Kore Calm Professional'
        };
    } else if (persona === 'Fenrir') {
        // Deep Resonant Male
        const voice = getVoice2(maleVoices, 1);
        return {
            voice,
            pitch: 0.65, // Deep resonant pitch
            rate: 0.90,
            name: voice ? `${voice.name} (Fenrir Resonant Male)` : 'Fenrir Resonant Male'
        };
    } else {
        // Puck: Natural British Cambridge Male Standard
        const voice = getVoice(maleVoices, 0);
        return {
            voice,
            pitch: 0.98, // Natural British male pitch
            rate: 1.00,
            name: voice ? `${voice.name} (Puck British Examiner)` : 'Puck British Examiner'
        };
    }
}

async function synthesizeGeminiAudio(text, persona = null) {
    persona = persona || currentGeminiPersona || 'Puck';
    const cleanText = text.trim();
    if (!cleanText) return null;

    const cacheKey = `gemini_${persona}_${cleanText}`;
    if (audioBlobCache.has(cacheKey)) {
        return audioBlobCache.get(cacheKey);
    }

    const clientKey = document.getElementById('set-gemini-key')?.value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');

    // 1. Direct Browser Fetch (Fastest, zero Python proxy latency) if client has entered an API key
    if (clientKey) {
        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${clientKey}`;
            const payload = {
                contents: [{
                    role: 'user',
                    parts: [{
                        text: `Read the following IELTS text aloud with authentic British Cambridge IELTS examiner cadence, clear human breathing, natural pauses, and warm articulation:\n\n"${cleanText}"`
                    }]
                }],
                generationConfig: {
                    responseModalities: ["AUDIO"],
                    speechConfig: {
                        voiceConfig: {
                            prebuiltVoiceConfig: {
                                voiceName: persona
                            }
                        }
                    }
                }
            };

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000);
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (res.ok) {
                const data = await res.json();
                const part = data.candidates?.[0]?.content?.parts?.find(p => p.inlineData && p.inlineData.data);
                if (part) {
                    const mimeType = part.inlineData.mimeType || 'audio/pcm;rate=24000';
                    const base64Data = part.inlineData.data;

                    let blobUrl;
                    if (mimeType.startsWith('audio/pcm') || mimeType.includes('rate=')) {
                        let rate = 24000;
                        const m = mimeType.match(/rate=(\d+)/);
                        if (m) rate = parseInt(m[1]);
                        const blob = pcm16ToWavBlob(base64Data, rate);
                        blobUrl = URL.createObjectURL(blob);
                    } else {
                        const binary = atob(base64Data);
                        const bytes = new Uint8Array(binary.length);
                        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                        const blob = new Blob([bytes], { type: mimeType });
                        blobUrl = URL.createObjectURL(blob);
                    }

                    audioBlobCache.set(cacheKey, blobUrl);
                    return blobUrl;
                }
            }
        } catch (err) {
            console.warn('Direct browser Gemini audio synthesis skipped:', err.message);
        }
    }

    // 2. Fallback: Backend TTS endpoint (uses admin / system key)
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        const backendRes = await fetch(`${API_BASE}/api/tts`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ text: cleanText, voice: persona, api_key: clientKey || '' })
        });
        if (backendRes.ok) {
            const ttsData = await backendRes.json();
            if (ttsData.success && ttsData.audio_base64) {
                const mime = ttsData.mime_type || 'audio/wav';
                let blobUrl;
                if (mime.startsWith('audio/pcm') || mime.includes('rate=')) {
                    let rate = 24000;
                    const m = mime.match(/rate=(\d+)/);
                    if (m) rate = parseInt(m[1]);
                    const blob = pcm16ToWavBlob(ttsData.audio_base64, rate);
                    blobUrl = URL.createObjectURL(blob);
                } else {
                    const binary = atob(ttsData.audio_base64);
                    const bytes = new Uint8Array(binary.length);
                    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                    const blob = new Blob([bytes], { type: mime });
                    blobUrl = URL.createObjectURL(blob);
                }
                audioBlobCache.set(cacheKey, blobUrl);
                return blobUrl;
            }
        }
    } catch (bErr) {
        console.warn('Backend TTS endpoint skipped:', bErr.message);
    }

    return null;
}

function stopAnyActiveAudio() {
    if (currentAudioElement) {
        try {
            currentAudioElement.pause();
            currentAudioElement.currentTime = 0;
        } catch (e) {}
        currentAudioElement = null;
    }
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    if (listeningTimeoutId) {
        clearTimeout(listeningTimeoutId);
        listeningTimeoutId = null;
    }
    listeningPassagePlaying = false;
    isAudioPlaying = false;
    updateAudioPlayerUI();
}

async function playExaminerVoice(text, btnElement = null) {
    if (!text) return;
    stopAnyActiveAudio();

    let origHtml = null;
    if (btnElement) {
        origHtml = btnElement.innerHTML;
        btnElement.innerHTML = '<span>🔊 Speaking...</span>';
    }

    const resetButton = () => {
        if (btnElement && origHtml) {
            btnElement.innerHTML = origHtml;
        }
    };

    if (currentAudioEngine === 'gemini') {
        const audioUrl = await synthesizeGeminiAudio(text, currentGeminiPersona);
        if (audioUrl) {
            const audio = new Audio(audioUrl);
            currentAudioElement = audio;
            audio.onended = () => {
                currentAudioElement = null;
                resetButton();
            };
            audio.onerror = () => {
                currentAudioElement = null;
                playBrowserExaminerVoice(text, resetButton);
            };
            try {
                await audio.play();
                return;
            } catch (err) {
                console.warn('Audio play error, falling back to browser voice:', err);
            }
        }
    }

    playBrowserExaminerVoice(text, resetButton);
}

function playBrowserExaminerVoice(text, onComplete = null) {
    if (!('speechSynthesis' in window)) {
        if (onComplete) onComplete();
        return;
    }

    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);

    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);
    if (params.voice) utt.voice = params.voice;
    utt.pitch = params.pitch;
    utt.rate = (audioSpeechRate || 1.0) * params.rate;

    utt.onend = () => {
        if (onComplete) onComplete();
    };
    utt.onerror = () => {
        if (onComplete) onComplete();
    };

    window.speechSynthesis.speak(utt);
}

function toggleAudioPlayback() {
    if (listeningPassagePlaying || isAudioPlaying) {
        stopAnyActiveAudio();
        return;
    }

    const scriptBox = document.getElementById('listening-script-box');
    const script = scriptBox ? scriptBox.innerText.trim() : '';
    if (!script) {
        alert('Audio transcript is empty for this test.');
        return;
    }

    isAudioPlaying = true;
    listeningPassagePlaying = true;
    updateAudioPlayerUI();

    // Split text into natural spoken sentences
    const sentences = script
        .replace(/Section \d+:?/gi, '')
        .split(/(?<=[.!?])\s+/)
        .map(s => s.trim())
        .filter(s => s.length > 2);

    listeningSentencesQueue = sentences;
    listeningSentenceIndex = 0;
    playNextListeningSentence();
}

async function playNextListeningSentence() {
    if (!listeningPassagePlaying || listeningSentenceIndex >= listeningSentencesQueue.length) {
        stopAnyActiveAudio();
        return;
    }

    const sentence = listeningSentencesQueue[listeningSentenceIndex];
    listeningSentenceIndex++;

    const statusText = document.getElementById('audio-status-text');
    if (statusText) {
        statusText.innerText = `Examiner Audio Playing (${listeningSentenceIndex}/${listeningSentencesQueue.length})...`;
    }

    if (currentAudioEngine === 'gemini') {
        try {
            const audioUrl = await synthesizeGeminiAudio(sentence, currentGeminiPersona);
            if (audioUrl && listeningPassagePlaying) {
                const audio = new Audio(audioUrl);
                currentAudioElement = audio;
                audio.playbackRate = audioSpeechRate || 1.0;
                audio.onended = () => {
                    currentAudioElement = null;
                    if (listeningPassagePlaying) {
                        listeningTimeoutId = setTimeout(playNextListeningSentence, 200);
                    }
                };
                audio.onerror = () => {
                    currentAudioElement = null;
                    speakSentenceWithBrowser(sentence);
                };
                await audio.play();
                return;
            }
        } catch (err) {
            console.warn('Gemini listening audio error, falling back to calibrated browser voice:', err);
        }
    }

    // High-definition browser synthesis with calibrated persona voice & pitch
    speakSentenceWithBrowser(sentence);
}

function speakSentenceWithBrowser(sentence) {
    if (!('speechSynthesis' in window)) {
        stopAnyActiveAudio();
        return;
    }

    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(sentence);
    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);

    if (params.voice) utt.voice = params.voice;
    utt.pitch = params.pitch;
    utt.rate = (audioSpeechRate || 1.0) * params.rate;

    utt.onend = () => {
        if (listeningPassagePlaying) {
            // Natural human inter-sentence breath pause (220ms)
            listeningTimeoutId = setTimeout(playNextListeningSentence, 220);
        }
    };

    utt.onerror = () => {
        if (listeningPassagePlaying) {
            listeningTimeoutId = setTimeout(playNextListeningSentence, 150);
        }
    };

    window.speechSynthesis.speak(utt);
}

function setAudioSpeed(rate) {
    audioSpeechRate = rate;
    document.querySelectorAll('.audio-speed-btn').forEach(btn => {
        btn.className = btn.innerText.includes(rate) 
            ? 'audio-speed-btn px-2 py-1 text-xs font-medium rounded bg-brand-600 text-white'
            : 'audio-speed-btn px-2 py-1 text-xs font-medium rounded bg-slate-800 text-slate-300 hover:bg-slate-700';
    });
}

function updateAudioPlayerUI() {
    const playIcon = document.getElementById('audio-icon-play');
    const pauseIcon = document.getElementById('audio-icon-pause');
    const statusText = document.getElementById('audio-status-text');
    const waveforms = document.getElementById('audio-waveforms');

    if (isAudioPlaying || listeningPassagePlaying) {
        if (playIcon) playIcon.classList.add('hidden');
        if (pauseIcon) pauseIcon.classList.remove('hidden');
        if (statusText) statusText.innerText = 'Examiner Audio Playing...';
        if (waveforms) waveforms.classList.remove('opacity-20');
    } else {
        if (playIcon) playIcon.classList.remove('hidden');
        if (pauseIcon) pauseIcon.classList.add('hidden');
        if (statusText) statusText.innerText = 'Audio Paused / Ready';
        if (waveforms) waveforms.classList.add('opacity-20');
    }
}

function toggleAudioScript() {
    const box = document.getElementById('listening-script-box');
    const btn = document.getElementById('btn-toggle-script');
    if (!box) return;
    box.classList.toggle('hidden');
    if (btn) btn.innerText = box.classList.contains('hidden') ? '📜 Audio Transcript' : '✕ Hide Audio Transcript';
}

async function previewExaminerVoice() {
    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);
    const personaLabel = currentAudioEngine === 'gemini' 
        ? `${currentGeminiPersona || 'Puck'} (Gemini AI Studio)` 
        : (params.voice ? `${params.name}` : 'System Cambridge Voice');

    const sample = `Good afternoon. This is the official IELTS examiner audio test using ${personaLabel}.`;
    const testBtns = [
        document.getElementById('btn-listening-test-voice'),
        document.getElementById('btn-preview-voice'),
        document.getElementById('btn-settings-preview-voice')
    ];
    testBtns.forEach(btn => {
        if (btn) btn.innerHTML = `<span>🔊 Testing...</span>`;
    });

    await playExaminerVoice(sample);
    setTimeout(() => {
        testBtns.forEach(btn => {
            if (btn) btn.innerHTML = '<span>🔊 Test</span>';
        });
    }, 2500);
}

function applyVoiceSelection(val) {
    if (!val) return;

    if (val.startsWith('gemini:')) {
        currentAudioEngine = 'gemini';
        currentGeminiPersona = val.replace('gemini:', '');
    } else if (val.startsWith('browser:')) {
        currentAudioEngine = 'browser';
        const uri = val.replace('browser:', '');
        selectedBrowserVoiceURI = (uri === 'auto' || uri === '') ? null : uri;
        if (selectedBrowserVoiceURI) {
            localStorage.setItem('ielts_browser_voice', selectedBrowserVoiceURI);
        } else {
            localStorage.removeItem('ielts_browser_voice');
        }
    } else if (['Puck', 'Aoede', 'Charon', 'Kore', 'Fenrir'].includes(val)) {
        currentAudioEngine = 'gemini';
        currentGeminiPersona = val;
    } else if (val === 'browser') {
        currentAudioEngine = 'browser';
        selectedBrowserVoiceURI = null;
    } else {
        currentAudioEngine = 'browser';
        selectedBrowserVoiceURI = val;
        localStorage.setItem('ielts_browser_voice', val);
    }

    syncVoiceUI();
}

function updateListeningVoiceSelection(val) {
    applyVoiceSelection(val);

    // If listening audio is playing, immediately switch voice and re-speak current sentence!
    if (listeningPassagePlaying) {
        if (currentAudioElement) {
            try { currentAudioElement.pause(); } catch(e){}
            currentAudioElement = null;
        }
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        if (listeningTimeoutId) {
            clearTimeout(listeningTimeoutId);
            listeningTimeoutId = null;
        }
        if (listeningSentenceIndex > 0) {
            listeningSentenceIndex--;
        }
        playNextListeningSentence();
    } else {
        const testBtn = document.getElementById('btn-listening-test-voice');
        if (testBtn) {
            const orig = testBtn.innerHTML;
            testBtn.innerHTML = '<span>✓ Voice Set!</span>';
            setTimeout(() => { testBtn.innerHTML = orig; }, 1400);
        }
    }
}

function updateSpeakingPersonaSelection(val) {
    applyVoiceSelection(val);
}

function updateAudioEnginePreference(val) {
    currentAudioEngine = val;
    syncVoiceUI();
}

function updateGeminiPersonaPreference(val) {
    currentGeminiPersona = val;
    syncVoiceUI();
}

function updateBrowserVoicePreference(val) {
    selectedBrowserVoiceURI = val;
    if (val) localStorage.setItem('ielts_browser_voice', val);
    else localStorage.removeItem('ielts_browser_voice');
    syncVoiceUI();
}

function syncVoiceUI() {
    localStorage.setItem('ielts_audio_engine', currentAudioEngine);
    localStorage.setItem('ielts_gemini_persona', currentGeminiPersona);
    if (selectedBrowserVoiceURI) {
        localStorage.setItem('ielts_browser_voice', selectedBrowserVoiceURI);
    }

    const currentSelectVal = currentAudioEngine === 'gemini' 
        ? `gemini:${currentGeminiPersona || 'Puck'}` 
        : (selectedBrowserVoiceURI ? `browser:${selectedBrowserVoiceURI}` : 'browser:auto');

    const listenVoice = document.getElementById('select-listening-voice');
    if (listenVoice) {
        if ([...listenVoice.options].some(o => o.value === currentSelectVal)) {
            listenVoice.value = currentSelectVal;
        } else if (currentAudioEngine === 'gemini' && [...listenVoice.options].some(o => o.value === `gemini:${currentGeminiPersona}`)) {
            listenVoice.value = `gemini:${currentGeminiPersona}`;
        } else if ([...listenVoice.options].some(o => o.value === currentGeminiPersona)) {
            listenVoice.value = currentGeminiPersona;
        } else {
            listenVoice.value = 'browser:auto';
        }
    }

    const speakPersona = document.getElementById('select-speaking-persona');
    if (speakPersona) {
        if ([...speakPersona.options].some(o => o.value === currentSelectVal)) {
            speakPersona.value = currentSelectVal;
        } else if (currentAudioEngine === 'gemini' && [...speakPersona.options].some(o => o.value === `gemini:${currentGeminiPersona}`)) {
            speakPersona.value = `gemini:${currentGeminiPersona}`;
        } else {
            speakPersona.value = 'browser:auto';
        }
    }

    const setEngine = document.getElementById('set-audio-engine');
    if (setEngine) setEngine.value = currentAudioEngine;

    const setPersona = document.getElementById('set-gemini-persona');
    if (setPersona) setPersona.value = currentGeminiPersona || 'Puck';

    const setBrowser = document.getElementById('set-browser-voice');
    if (setBrowser && selectedBrowserVoiceURI) setBrowser.value = selectedBrowserVoiceURI;
}
// =====================================================================
// IELTS MASTER: LISTENING TEST MODULE
// =====================================================================

async function loadListeningTest(testId) {
    try {
        currentListeningResults = null;
        listeningAnswers = {};
        if (typeof stopAnyActiveAudio === 'function') stopAnyActiveAudio();
        const res = await fetch(`${API_BASE}/api/tests/${testId}`);
        currentListeningTest = await res.json();
        
        const titleEl = document.getElementById('listening-test-title');
        if (titleEl) titleEl.innerText = currentListeningTest.title;

        // Update assigned exam badge
        const badgeEl = document.getElementById('badge-listening-test-id');
        if (badgeEl) badgeEl.innerText = `Exam Set: ${testId}`;

        // Sync dropdown if exists
        const selectEl = document.getElementById('select-listening-test');
        if (selectEl) selectEl.value = testId;

        // Render Questions
        renderListeningSections();

        // Reset official CD IELTS 30-minute listening countdown
        if (typeof resetListeningTimer === 'function') resetListeningTimer();
        if (typeof isViewActive === 'function' && isViewActive('listening')) {
            if (typeof startListeningTimer === 'function') startListeningTimer();
        }

    } catch (err) {
        console.error('Failed loading listening test:', err);
    }
}

function renderListeningSections() {
    if (!currentListeningTest) return;
    const container = document.getElementById('listening-sections-container');
    if (!container) return;
    const sections = currentListeningTest.content.sections || [];
    
    // Combine full script for audio player & script box
    const fullScript = sections.map(s => `[${s.title}]\n${s.audio_script}\n`).join('\n\n');
    const scriptBox = document.getElementById('listening-script-box');
    if (scriptBox) scriptBox.innerText = fullScript;

    container.innerHTML = sections.map(sec => `
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                <div>
                    <h4 class="font-bold text-slate-900 text-sm">${sec.title}</h4>
                    <p class="text-xs text-slate-500">${sec.context}</p>
                </div>
                <span class="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">Section ${sec.section_num}</span>
            </div>

            <div class="space-y-4">
                ${sec.questions.map(q => renderListeningQuestion(q)).join('')}
            </div>
        </div>
    `).join('');
}

function renderListeningQuestion(q) {
    const res = currentListeningResults ? currentListeningResults[q.id] : null;
    const userVal = listeningAnswers[q.id] || '';

    const qNumMatch = q.id.match(/-Q(\d+)$/);
    const qNum = qNumMatch ? parseInt(qNumMatch[1]) : 0;

    let instructionBannerHTML = '';
    if (qNum === 1) {
        instructionBannerHTML = `
            <div class="mb-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 1 – 10</span>
                <p class="font-medium text-slate-800 mt-0.5">Complete the notes below. Write <strong class="text-indigo-900 font-bold uppercase underline">NO MORE THAN TWO WORDS AND/OR A NUMBER</strong> for each answer.</p>
            </div>
        `;
    } else if (qNum === 11) {
        instructionBannerHTML = `
            <div class="mb-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 11 – 15</span>
                <p class="font-medium text-slate-800 mt-0.5">Choose the correct letter, <strong>A, B, C or D</strong>.</p>
            </div>
        `;
    } else if (qNum === 16) {
        instructionBannerHTML = `
            <div class="my-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 16 – 20</span>
                <p class="font-medium text-slate-800 mt-0.5">Complete the sentences below. Write <strong class="text-indigo-900 font-bold uppercase underline">NO MORE THAN TWO WORDS</strong> for each answer.</p>
            </div>
        `;
    } else if (qNum === 21) {
        instructionBannerHTML = `
            <div class="mb-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 21 – 26</span>
                <p class="font-medium text-slate-800 mt-0.5">Choose the correct letter, <strong>A, B, C or D</strong>.</p>
            </div>
        `;
    } else if (qNum === 27) {
        instructionBannerHTML = `
            <div class="my-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 27 – 30</span>
                <p class="font-medium text-slate-800 mt-0.5">Complete the notes below. Write <strong class="text-indigo-900 font-bold uppercase underline">NO MORE THAN TWO WORDS AND/OR A NUMBER</strong> for each answer.</p>
            </div>
        `;
    } else if (qNum === 31) {
        instructionBannerHTML = `
            <div class="mb-3 p-3.5 rounded-xl bg-indigo-50/90 border border-indigo-200 text-xs text-indigo-950">
                <span class="font-bold text-indigo-900 text-sm">Questions 31 – 40</span>
                <p class="font-medium text-slate-800 mt-0.5">Complete the lecture notes below. Write <strong class="text-indigo-900 font-bold uppercase underline">NO MORE THAN TWO WORDS AND/OR A NUMBER</strong> for each answer.</p>
            </div>
        `;
    }

    let cardBorder = 'border-slate-200/60 bg-slate-50';
    let feedbackHTML = '<div id="l-feedback-' + q.id + '" class="hidden mt-2 text-xs"></div>';

    if (res) {
        if (res.is_correct) {
            cardBorder = 'border-emerald-300 bg-emerald-50/70 ring-1 ring-emerald-200';
            feedbackHTML = `
                <div class="mt-2.5 p-2.5 rounded-lg bg-emerald-100/80 border border-emerald-200 text-xs text-emerald-900 font-medium">
                    <span class="font-bold">✓ Correct!</span> ${res.explanation || ''}
                </div>
            `;
        } else {
            cardBorder = 'border-rose-300 bg-rose-50/70 ring-1 ring-rose-200';
            feedbackHTML = `
                <div class="mt-2.5 p-2.5 rounded-lg bg-rose-100/80 border border-rose-200 text-xs text-rose-900">
                    <span class="font-bold">✗ Incorrect.</span> Correct Answer: <strong class="underline">${res.correct_answer}</strong> (You answered: "${res.user_answer || 'blank'}").
                    <div class="mt-1 text-slate-600">${res.explanation || ''}</div>
                </div>
            `;
        }
    }

    let qBody = '';
    if (q.type === 'Multiple Choice' && q.options && q.options.length > 0) {
        qBody = `
            <div class="p-3.5 rounded-xl border transition-all ${cardBorder}" id="l-q-container-${q.id}">
                <div class="text-xs font-bold text-slate-800 mb-2.5">${q.id}: ${q.question_text}</div>
                <div class="space-y-1.5">
                    ${q.options.map(opt => `
                        <label class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-white text-xs text-slate-700 cursor-pointer ${userVal === opt ? 'bg-indigo-50 font-semibold' : ''}">
                            <input type="radio" name="${q.id}" value="${opt}" ${userVal === opt ? 'checked' : ''} onchange="listeningAnswers['${q.id}'] = this.value" class="text-brand-600 focus:ring-brand-500">
                            <span>${opt}</span>
                        </label>
                    `).join('')}
                </div>
                ${feedbackHTML}
            </div>
        `;
    } else {
        qBody = `
            <div class="p-3.5 rounded-xl border transition-all ${cardBorder}" id="l-q-container-${q.id}">
                <div class="text-xs font-bold text-slate-800 mb-2">${q.id}: ${q.question_text}</div>
                <div class="flex items-center gap-2">
                    <input type="text" value="${userVal}" placeholder="Type your answer..." oninput="listeningAnswers['${q.id}'] = this.value" class="flex-1 p-2 rounded-lg border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white font-medium">
                </div>
                ${feedbackHTML}
            </div>
        `;
    }

    return instructionBannerHTML + qBody;
}

async function submitListeningTest() {
    if (!currentListeningTest) return;

    try {
        const res = await fetch(`${API_BASE}/api/attempts/listening`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_id: currentListeningTest.id,
                answers: listeningAnswers,
                time_spent_seconds: 900
            })
        });

        const data = await res.json();
        
        currentListeningResults = {};
        if (data.detailed_results) {
            data.detailed_results.forEach(res => {
                currentListeningResults[res.id] = res;
            });
        }

        renderListeningSections();

        alert(`Listening Test Complete!\nOverall Score: ${data.raw_score}/${data.total_questions}\nEstimated Band Score: ${data.band_score.toFixed(1)}`);
        if (typeof refreshData === 'function') await refreshData();
    } catch (err) {
        alert('Error grading listening test: ' + err.message);
    }
}
// =====================================================================
// IELTS MASTER: ACADEMIC READING MODULE (SPLIT-SCREEN 40 QUESTIONS)
// =====================================================================

let currentContrastTheme = 'standard';
let currentReadingMobileTab = 'passage';

async function loadReadingTest(testId) {
    try {
        currentReadingResults = null;
        readingAnswers = {};
        flaggedQuestions.clear();
        const res = await fetch(`${API_BASE}/api/tests/${testId}`);
        currentReadingTest = await res.json();
        
        const titleEl = document.getElementById('reading-test-title');
        if (titleEl) titleEl.innerText = currentReadingTest.title;

        // Update assigned exam badge
        const isGT = currentReadingTest?.type === 'General Training';
        const badgeEl = document.getElementById('badge-reading-test-id');
        if (badgeEl) badgeEl.innerText = `Exam Set: ${testId} [${isGT ? 'General Training' : 'Academic'}]`;

        // Update tab buttons for Section vs Passage
        const unitLabel = isGT ? 'Section' : 'Passage';
        [0, 1, 2].forEach(i => {
            const btn = document.getElementById(`btn-passage-${i}`);
            const ranges = isGT ? ['1–14', '15–27', '28–40'] : ['1–13', '14–26', '27–40'];
            if (btn) btn.innerText = `${unitLabel} ${i + 1} (${ranges[i]})`;
        });

        // Sync dropdown
        const selectEl = document.getElementById('select-reading-test');
        if (selectEl) selectEl.value = testId;

        currentActiveQId = `${testId}-Q1`;
        renderReadingPalette();
        selectReadingPassage(0);
        if (typeof resetReadingTimer === 'function') resetReadingTimer();
        if (typeof isViewActive === 'function' && isViewActive('reading')) {
            if (typeof startReadingTimer === 'function') startReadingTimer();
        }
    } catch (err) {
        console.error('Failed loading reading test:', err);
    }
}

function selectReadingPassage(idx) {
    activeReadingPassageIdx = idx;
    [0, 1, 2].forEach(i => {
        const btn = document.getElementById(`btn-passage-${i}`);
        if (btn) {
            btn.className = (i === idx) 
                ? 'px-3 py-1.5 rounded-lg bg-white shadow-xs text-slate-900 font-bold'
                : 'px-3 py-1.5 rounded-lg text-slate-600 hover:text-slate-900';
        }
    });

    renderReadingPassage(idx);
}

function renderReadingPassage(idx) {
    if (!currentReadingTest) return;
    const passage = currentReadingTest.content.passages[idx];
    if (!passage) return;

    const isGT = currentReadingTest?.type === 'General Training';
    const prefix = isGT ? 'Section' : 'Passage';

    const headingEl = document.getElementById('reading-passage-heading');
    if (headingEl) {
        if (passage.title && (passage.title.toLowerCase().startsWith('section') || passage.title.toLowerCase().startsWith('passage'))) {
            headingEl.innerText = passage.title;
        } else {
            headingEl.innerText = `${prefix} ${passage.passage_num}: ${passage.title}`;
        }
    }
    
    // Heading for questions
    const qRangeLabels = isGT
        ? ['Questions 1 – 14 (Section 1)', 'Questions 15 – 27 (Section 2)', 'Questions 28 – 40 (Section 3)']
        : ['Questions 1 – 13 (Passage 1)', 'Questions 14 – 26 (Passage 2)', 'Questions 27 – 40 (Passage 3)'];
    const qHeadingEl = document.getElementById('reading-passage-q-heading');
    if (qHeadingEl) qHeadingEl.innerText = qRangeLabels[idx] || `Questions`;
    
    // Paragraph format with authentic CD IELTS letter markers [ Paragraph A ]
    const paragraphs = passage.text.split('\n\n');
    const bodyEl = document.getElementById('reading-passage-body');
    if (bodyEl) {
        bodyEl.innerHTML = paragraphs.map(p => {
            const cleanP = p.trim();
            const markerMatch = cleanP.match(/^(Paragraph\s+[A-Z]|Section\s+[A-Z]|[A-Z]\.)\s*(.*)$/s);
            if (markerMatch) {
                return `
                    <div class="mb-5">
                        <span class="cd-paragraph-marker">${markerMatch[1].replace('.', '')}</span>
                        <p class="leading-relaxed text-slate-800 font-serif mt-1">${markerMatch[2]}</p>
                    </div>
                `;
            }
            return `<p class="leading-relaxed text-slate-800 font-serif mb-4">${cleanP}</p>`;
        }).join('');
    }

    // Render questions for this passage
    const qContainer = document.getElementById('reading-questions-container');
    if (qContainer) {
        qContainer.innerHTML = passage.questions.map(q => renderSingleReadingQuestion(q)).join('');
    }

    updateReadingAnsweredCount();
}

function renderSingleReadingQuestion(q) {
    const isAnswered = readingAnswers[q.id] !== undefined && readingAnswers[q.id] !== '';
    const currentVal = readingAnswers[q.id] || '';
    const isFlagged = flaggedQuestions.has(q.id);
    const result = currentReadingResults ? currentReadingResults[q.id] : null;

    let answerControlHTML = '';

    if (q.type === 'True/False/Not Given') {
        answerControlHTML = `
            <div class="grid grid-cols-3 gap-2">
                ${['TRUE', 'FALSE', 'NOT GIVEN'].map(choice => {
                    const activeClass = (currentVal.toUpperCase() === choice || (choice === 'TRUE' && currentVal.toUpperCase() === 'T') || (choice === 'FALSE' && currentVal.toUpperCase() === 'F') || (choice === 'NOT GIVEN' && currentVal.toUpperCase() === 'NG'))
                        ? 'bg-sky-500 border-sky-500 text-white font-bold'
                        : 'border-slate-200 text-slate-700 hover:bg-sky-50';
                    return `
                        <button type="button" onclick="setReadingAnswer('${q.id}', '${choice}', this)" class="r-choice-btn py-1.5 rounded-lg border text-xs font-semibold transition-colors ${activeClass}">
                            ${choice}
                        </button>
                    `;
                }).join('')}
            </div>
        `;
    } else if (q.type === 'Yes/No/Not Given') {
        answerControlHTML = `
            <div class="grid grid-cols-3 gap-2">
                ${['YES', 'NO', 'NOT GIVEN'].map(choice => {
                    const activeClass = (currentVal.toUpperCase() === choice || (choice === 'YES' && currentVal.toUpperCase() === 'Y') || (choice === 'NO' && currentVal.toUpperCase() === 'N') || (choice === 'NOT GIVEN' && currentVal.toUpperCase() === 'NG'))
                        ? 'bg-sky-500 border-sky-500 text-white font-bold'
                        : 'border-slate-200 text-slate-700 hover:bg-sky-50';
                    return `
                        <button type="button" onclick="setReadingAnswer('${q.id}', '${choice}', this)" class="r-choice-btn py-1.5 rounded-lg border text-xs font-semibold transition-colors ${activeClass}">
                            ${choice}
                        </button>
                    `;
                }).join('')}
            </div>
        `;
    } else if (q.type === 'Matching Headings') {
        answerControlHTML = `
            <select onchange="setReadingAnswer('${q.id}', this.value, this)" class="w-full p-2.5 rounded-lg border border-slate-200 text-xs font-medium text-slate-800 focus:ring-2 focus:ring-sky-500 bg-white">
                <option value="">-- Select Heading for this Paragraph --</option>
                ${(q.options || []).map(opt => `
                    <option value="${opt}" ${currentVal === opt ? 'selected' : ''}>${opt}</option>
                `).join('')}
            </select>
        `;
    } else if (q.options && q.options.length > 0) {
        answerControlHTML = `
            <div class="space-y-1.5">
                ${q.options.map(opt => `
                    <label class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-white text-xs text-slate-700 cursor-pointer ${currentVal === opt ? 'bg-sky-50 font-semibold' : ''}">
                        <input type="radio" name="${q.id}" value="${opt}" ${currentVal === opt ? 'checked' : ''} onchange="setReadingAnswer('${q.id}', this.value, this)" class="text-sky-600 focus:ring-sky-500">
                        <span>${opt}</span>
                    </label>
                `).join('')}
            </div>
        `;
    } else {
        answerControlHTML = `
            <div class="flex items-center gap-2">
                <input type="text" value="${currentVal}" placeholder="Type exact word(s) from passage..." oninput="setReadingAnswer('${q.id}', this.value, this)" class="w-full p-2.5 rounded-lg border border-slate-200 text-xs focus:ring-2 focus:ring-sky-500 bg-white font-medium">
            </div>
        `;
    }

    let cardBorder = isFlagged ? 'border-amber-300 ring-1 ring-amber-300 bg-slate-50' : 'border-slate-200/80 bg-slate-50';
    let feedbackHTML = `<div id="r-feedback-${q.id}" class="hidden mt-2 text-xs"></div>`;

    if (result) {
        if (result.is_correct) {
            cardBorder = 'bg-emerald-50/70 border-emerald-300 ring-1 ring-emerald-200';
            feedbackHTML = `
                <div id="r-feedback-${q.id}" class="mt-2.5 p-2.5 rounded-lg bg-emerald-100/80 border border-emerald-200 text-xs text-emerald-900 font-medium">
                    <span class="font-bold">✓ Correct!</span> ${result.explanation || ''}
                </div>
            `;
        } else {
            cardBorder = 'bg-rose-50/70 border-rose-300 ring-1 ring-rose-200';
            feedbackHTML = `
                <div id="r-feedback-${q.id}" class="mt-2.5 p-2.5 rounded-lg bg-rose-100/80 border border-rose-200 text-xs text-rose-900">
                    <span class="font-bold">✗ Incorrect.</span> Correct Answer: <strong class="underline">${result.correct_answer}</strong> (You answered: "${result.user_answer || 'blank'}").
                    <div class="mt-1 text-slate-600">${result.explanation || ''}</div>
                </div>
            `;
        }
    }

    const qNumMatch = q.id.match(/-Q(\d+)$/);
    const qNum = qNumMatch ? parseInt(qNumMatch[1]) : 0;
    const isGT = currentReadingTest?.type === 'General Training';

    let instructionBannerHTML = '';

    if (isGT) {
        // Official IELTS General Training Reading Instructions
        if (qNum === 1) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 1 – 7</div>
                    <p class="font-medium text-slate-800 mb-2">Do the following statements agree with the information given in Section 1 (Texts A & B)?</p>
                    <div class="space-y-1 pl-2.5 border-l-2 border-sky-400 text-[11px] text-slate-700 font-mono">
                        <div><strong class="text-sky-900 font-bold">TRUE</strong> — if the statement agrees with the information</div>
                        <div><strong class="text-sky-900 font-bold">FALSE</strong> — if the statement contradicts the information</div>
                        <div><strong class="text-sky-900 font-bold">NOT GIVEN</strong> — if there is no information on this</div>
                    </div>
                </div>
            `;
        } else if (qNum === 8) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 8 – 14</div>
                    <p class="font-medium text-slate-800">Complete the sentences below from Section 1 (Texts A & B).</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose <strong class="text-sky-900 font-bold uppercase underline">NO MORE THAN TWO WORDS AND/OR A NUMBER</strong> from the text for each answer.</p>
                </div>
            `;
        } else if (qNum === 15) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 15 – 21</div>
                    <p class="font-medium text-slate-800">Complete the sentences below from Section 2 (Workplace Texts C & D).</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose <strong class="text-sky-900 font-bold uppercase underline">NO MORE THAN THREE WORDS AND/OR A NUMBER</strong> from the text for each answer.</p>
                </div>
            `;
        } else if (qNum === 22) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 22 – 27</div>
                    <p class="font-medium text-slate-800 mb-2">Do the following statements agree with the workplace guidelines given in Section 2?</p>
                    <div class="space-y-1 pl-2.5 border-l-2 border-sky-400 text-[11px] text-slate-700 font-mono">
                        <div><strong class="text-sky-900 font-bold">TRUE</strong> — if the statement agrees with the information</div>
                        <div><strong class="text-sky-900 font-bold">FALSE</strong> — if the statement contradicts the information</div>
                        <div><strong class="text-sky-900 font-bold">NOT GIVEN</strong> — if there is no information on this</div>
                    </div>
                </div>
            `;
        } else if (qNum === 28) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 28 – 33</div>
                    <p class="font-medium text-slate-800 mb-2">Do the following statements agree with the claims of the writer in Section 3?</p>
                    <div class="space-y-1 pl-2.5 border-l-2 border-sky-400 text-[11px] text-slate-700 font-mono">
                        <div><strong class="text-sky-900 font-bold">YES</strong> — if the statement agrees with the claims of the writer</div>
                        <div><strong class="text-sky-900 font-bold">NO</strong> — if the statement contradicts the claims of the writer</div>
                        <div><strong class="text-sky-900 font-bold">NOT GIVEN</strong> — if it is impossible to say what the writer thinks about this</div>
                    </div>
                </div>
            `;
        } else if (qNum === 34) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 34 – 40</div>
                    <p class="font-medium text-slate-800">Complete the summary / answer the questions below.</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose <strong class="text-sky-900 font-bold uppercase underline">NO MORE THAN TWO WORDS</strong> from the passage for each answer.</p>
                </div>
            `;
        }
    } else {
        // Official IELTS Academic Reading Instructions
        if (qNum === 1) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 1 – 7</div>
                    <p class="font-medium text-slate-800 mb-2">Do the following statements agree with the information given in Reading Passage 1?</p>
                    <div class="space-y-1 pl-2.5 border-l-2 border-sky-400 text-[11px] text-slate-700 font-mono">
                        <div><strong class="text-sky-900 font-bold">TRUE</strong> — if the statement agrees with the information</div>
                        <div><strong class="text-sky-900 font-bold">FALSE</strong> — if the statement contradicts the information</div>
                        <div><strong class="text-sky-900 font-bold">NOT GIVEN</strong> — if there is no information on this</div>
                    </div>
                </div>
            `;
        } else if (qNum === 8) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 8 – 13</div>
                    <p class="font-medium text-slate-800">Complete the sentences below.</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose <strong class="text-sky-900 font-bold uppercase underline">NO MORE THAN TWO WORDS</strong> from the passage for each answer.</p>
                </div>
            `;
        } else if (qNum === 14) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 14 – 19</div>
                    <p class="font-medium text-slate-800">Reading Passage 2 has six sections, <strong>A–F</strong>.</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose the correct heading for each section from the list of headings below.</p>
                </div>
            `;
        } else if (qNum === 20) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 20 – 22</div>
                    <p class="font-medium text-slate-800">Choose the correct letter, <strong>A, B, C or D</strong>.</p>
                </div>
            `;
        } else if (qNum === 23) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 23 – 26</div>
                    <p class="font-medium text-slate-800">Look at the following statements and the list of researchers below.</p>
                    <p class="text-[11px] text-slate-600 mt-1">Match each statement with the correct researcher, <strong>A–D</strong>.</p>
                </div>
            `;
        } else if (qNum === 27) {
            instructionBannerHTML = `
                <div class="mb-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 27 – 32</div>
                    <p class="font-medium text-slate-800 mb-2">Do the following statements agree with the claims of the writer in Reading Passage 3?</p>
                    <div class="space-y-1 pl-2.5 border-l-2 border-sky-400 text-[11px] text-slate-700 font-mono">
                        <div><strong class="text-sky-900 font-bold">YES</strong> — if the statement agrees with the claims of the writer</div>
                        <div><strong class="text-sky-900 font-bold">NO</strong> — if the statement contradicts the claims of the writer</div>
                        <div><strong class="text-sky-900 font-bold">NOT GIVEN</strong> — if it is impossible to say what the writer thinks about this</div>
                    </div>
                </div>
            `;
        } else if (qNum === 33) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 33 – 36</div>
                    <p class="font-medium text-slate-800">Complete the summary below.</p>
                    <p class="text-[11px] text-slate-600 mt-1">Choose <strong class="text-sky-900 font-bold uppercase underline">NO MORE THAN TWO WORDS</strong> from the passage for each answer.</p>
                </div>
            `;
        } else if (qNum === 37) {
            instructionBannerHTML = `
                <div class="my-4 p-4 rounded-xl bg-sky-50/90 border border-sky-200 text-xs text-sky-950">
                    <div class="font-bold text-sky-900 text-sm mb-1">Questions 37 – 40</div>
                    <p class="font-medium text-slate-800">Choose the correct letter, <strong>A, B, C or D</strong>.</p>
                </div>
            `;
        }
    }

    const cardHTML = `
        <div class="p-4 rounded-xl border transition-all ${cardBorder}" id="r-q-container-${q.id}" onclick="setCurrentActiveQ('${q.id}')">
            <div class="flex items-start justify-between gap-2 mb-2">
                <span class="text-xs font-bold text-slate-800">${q.id}: ${q.question_text}</span>
                <button type="button" onclick="event.stopPropagation(); toggleFlagQuestion('${q.id}')" class="text-xs ${isFlagged ? 'text-amber-600 font-bold' : 'text-slate-400 hover:text-amber-500'}" title="Flag for review">
                    ${isFlagged ? '🚩 Flagged' : '🏳️ Flag'}
                </button>
            </div>
            ${answerControlHTML}
            ${feedbackHTML}
        </div>
    `;

    return instructionBannerHTML + cardHTML;
}

function renderReadingPalette() {
    const palette = document.getElementById('reading-palette-container');
    if (!palette) return;

    let html = '';
    const testPrefix = currentReadingTest ? currentReadingTest.id : 'R-01';
    for (let i = 1; i <= 40; i++) {
        const qid = `${testPrefix}-Q${i}`;
        const isAnswered = readingAnswers[qid] !== undefined && String(readingAnswers[qid]).trim() !== '';
        const isFlagged = flaggedQuestions.has(qid);
        const isCurrent = (currentActiveQId === qid);
        const result = currentReadingResults ? currentReadingResults[qid] : null;

        let btnClass = 'cd-palette-btn ';
        
        if (result) {
            btnClass += result.is_correct ? 'graded-correct ' : 'graded-incorrect ';
            if (isCurrent) btnClass += 'active-q ';
        } else {
            if (isAnswered) btnClass += 'answered ';
            else btnClass += 'unanswered ';

            if (isCurrent) btnClass += 'active-q ';
            if (isFlagged) btnClass += 'flagged ';
        }

        // Add passage/section break divider after Section 1/2 or Passage 1/2
        const isGT = currentReadingTest?.type === 'General Training';
        let divider = '';
        if (isGT) {
            if (i === 14 || i === 27) {
                divider = '<div class="h-6 w-px bg-slate-300 mx-1 shrink-0"></div>';
            }
        } else {
            if (i === 13 || i === 26) {
                divider = '<div class="h-6 w-px bg-slate-300 mx-1 shrink-0"></div>';
            }
        }

        html += `<button type="button" onclick="jumpToReadingQuestion(${i})" class="${btnClass}" id="palette-btn-${qid}" title="Question ${i}${isFlagged ? ' (Flagged)' : ''}">${i}</button>${divider}`;
    }
    palette.innerHTML = html;
}

function jumpToReadingQuestion(qNum) {
    const testPrefix = currentReadingTest ? currentReadingTest.id : 'R-01';
    const qid = `${testPrefix}-Q${qNum}`;
    currentActiveQId = qid;

    const isGT = currentReadingTest?.type === 'General Training';
    let targetPassageIdx = 0;
    if (isGT) {
        if (qNum >= 28) targetPassageIdx = 2;
        else if (qNum >= 15) targetPassageIdx = 1;
        else targetPassageIdx = 0;
    } else {
        if (qNum >= 27) targetPassageIdx = 2;
        else if (qNum >= 14) targetPassageIdx = 1;
        else targetPassageIdx = 0;
    }

    if (activeReadingPassageIdx !== targetPassageIdx) {
        selectReadingPassage(targetPassageIdx);
    }

    const flagCheckbox = document.getElementById('reading-flag-toggle');
    if (flagCheckbox) {
        flagCheckbox.checked = flaggedQuestions.has(qid);
    }

    setTimeout(() => {
        const el = document.getElementById(`r-q-container-${qid}`);
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.classList.add('ring-2', 'ring-sky-500');
            setTimeout(() => el.classList.remove('ring-2', 'ring-sky-500'), 1800);
        }
    }, 100);

    renderReadingPalette();
}

function nextReadingQuestion() {
    const match = currentActiveQId.match(/-Q(\d+)$/);
    const currNum = match ? parseInt(match[1], 10) : 1;
    if (currNum < 40) {
        jumpToReadingQuestion(currNum + 1);
    }
}

function prevReadingQuestion() {
    const match = currentActiveQId.match(/-Q(\d+)$/);
    const currNum = match ? parseInt(match[1], 10) : 1;
    if (currNum > 1) {
        jumpToReadingQuestion(currNum - 1);
    }
}

function setContrastTheme(theme) {
    if (typeof applyTheme === 'function') {
        applyTheme(theme === 'dark' ? 'dark' : 'light');
    }
}


function setCurrentActiveQ(qid) {
    currentActiveQId = qid;
    const flagCheckbox = document.getElementById('reading-flag-toggle');
    if (flagCheckbox) {
        flagCheckbox.checked = flaggedQuestions.has(qid);
    }
    renderReadingPalette();
}

function toggleFlagQuestion(qid) {
    if (flaggedQuestions.has(qid)) {
        flaggedQuestions.delete(qid);
    } else {
        flaggedQuestions.add(qid);
    }
    renderReadingPalette();
    const el = document.getElementById(`r-q-container-${qid}`);
    if (el) {
        const isFlagged = flaggedQuestions.has(qid);
        el.className = `p-4 rounded-xl bg-slate-50 border ${isFlagged ? 'border-amber-300 ring-1 ring-amber-300' : 'border-slate-200/80'} transition-all`;
    }
}

function toggleFlagCurrentQuestion() {
    if (currentActiveQId) {
        toggleFlagQuestion(currentActiveQId);
    }
}

function setReadingAnswer(qid, choice, btnEl) {
    readingAnswers[qid] = choice;

    if (btnEl && btnEl.classList.contains('r-choice-btn')) {
        const parent = btnEl.closest(`#r-q-container-${qid}`);
        if (parent) {
            parent.querySelectorAll('.r-choice-btn').forEach(b => {
                b.className = 'r-choice-btn py-1.5 rounded-lg border text-xs font-semibold border-slate-200 text-slate-700 hover:bg-sky-50 transition-colors';
            });
            btnEl.className = 'r-choice-btn py-1.5 rounded-lg border text-xs font-semibold bg-sky-500 border-sky-500 text-white font-bold transition-colors';
        }
    }

    updateReadingAnsweredCount();
    renderReadingPalette();
}

function updateReadingAnsweredCount() {
    const answeredCount = Object.values(readingAnswers).filter(v => v !== undefined && String(v).trim() !== '').length;
    const badge = document.getElementById('reading-answered-badge');
    if (badge) {
        badge.innerText = `${answeredCount} / 40 Answered`;
        if (answeredCount === 40) {
            badge.className = 'text-xs text-emerald-600 font-bold';
        } else {
            badge.className = 'text-xs text-sky-600 font-semibold';
        }
    }
    const mobileBadge = document.getElementById('mobile-reading-answered-count');
    if (mobileBadge) {
        mobileBadge.innerText = `${answeredCount}/40`;
    }
}

function setReadingMobileTab(tab) {
    currentReadingMobileTab = tab;
    const passageCol = document.getElementById('reading-passage-column');
    const questionsCol = document.getElementById('reading-questions-column');
    const btnPassage = document.getElementById('btn-mobile-show-passage');
    const btnQuestions = document.getElementById('btn-mobile-show-questions');

    if (!passageCol || !questionsCol) return;

    if (tab === 'passage') {
        passageCol.classList.remove('hidden');
        passageCol.classList.add('flex');
        questionsCol.classList.remove('flex');
        questionsCol.classList.add('hidden');

        if (btnPassage) {
            btnPassage.className = 'flex-1 py-2 rounded-lg bg-white text-brand-600 font-bold shadow-sm flex items-center justify-center gap-1.5 transition-all';
        }
        if (btnQuestions) {
            btnQuestions.className = 'flex-1 py-2 rounded-lg text-slate-600 hover:text-slate-900 font-medium flex items-center justify-center gap-1.5 transition-all';
        }
    } else {
        passageCol.classList.remove('flex');
        passageCol.classList.add('hidden');
        questionsCol.classList.remove('hidden');
        questionsCol.classList.add('flex');

        if (btnPassage) {
            btnPassage.className = 'flex-1 py-2 rounded-lg text-slate-600 hover:text-slate-900 font-medium flex items-center justify-center gap-1.5 transition-all';
        }
        if (btnQuestions) {
            btnQuestions.className = 'flex-1 py-2 rounded-lg bg-white text-sky-600 font-bold shadow-sm flex items-center justify-center gap-1.5 transition-all';
        }
    }
}

function setReadingFontSize(size) {
    const el = document.getElementById('reading-passage-body');
    if (!el) return;

    el.classList.remove('reading-text-sm', 'reading-text-base', 'reading-text-lg');
    if (size === 'sm') {
        el.classList.add('reading-text-sm');
    } else if (size === 'lg') {
        el.classList.add('reading-text-lg');
    } else {
        el.classList.add('reading-text-base');
    }

    ['sm', 'base', 'lg'].forEach(s => {
        const btn = document.getElementById(`btn-font-${s}`);
        if (btn) {
            if (s === size) {
                btn.className = 'px-2.5 py-1 rounded bg-white text-brand-600 font-bold shadow-sm transition-colors';
            } else {
                btn.className = 'px-2.5 py-1 rounded text-slate-600 hover:text-slate-900 transition-colors';
            }
        }
    });
}

function adjustReadingFontSize(delta) {
    readingFontSizePx = Math.min(22, Math.max(12, readingFontSizePx + delta));
    const el = document.getElementById('reading-passage-body');
    if (el) el.style.fontSize = `${readingFontSizePx}px`;
}

function setupPassageHighlighting() {
    const passageEl = document.getElementById('reading-passage-body');
    if (!passageEl) return;

    passageEl.addEventListener('mouseup', () => {
        const selection = window.getSelection();
        if (!selection.rangeCount || selection.isCollapsed) return;

        const range = selection.getRangeAt(0);
        if (!passageEl.contains(range.commonAncestorContainer)) return;

        const span = document.createElement('span');
        span.className = 'highlighted';
        try {
            range.surroundContents(span);
        } catch (e) {
            // ignore non-clean boundary selections
        }
    });
}

async function submitReadingTest() {
    if (!currentReadingTest) return;

    try {
        const res = await fetch(`${API_BASE}/api/attempts/reading`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_id: currentReadingTest.id,
                answers: readingAnswers,
                time_spent_seconds: 3600 - readingTimeLeftSec
            })
        });

        const data = await res.json();
        
        currentReadingResults = {};
        if (data.detailed_results) {
            data.detailed_results.forEach(res => {
                currentReadingResults[res.id] = res;
            });
        }

        renderReadingPalette();
        renderReadingPassage(activeReadingPassageIdx);

        alert(`🎉 Reading Test Complete!\nRaw Score: ${data.raw_score} / ${data.total_questions}\nOfficial Estimated Band Score: Band ${data.band_score.toFixed(1)}`);
        if (typeof refreshData === 'function') await refreshData();
    } catch (err) {
        alert('Error submitting reading test: ' + err.message);
    }
}
/**
 * IELTS Master - Writing Module
 * Handles Task 1 & Task 2 loading, word counting, Gemini evaluation, model answer modal, and report rendering.
 */

async function loadWritingTask(taskId) {
    try {
        const res = await fetch(`${API_BASE}/api/tests/${taskId}`);
        currentWritingTask = await res.json();
        const content = currentWritingTask.content;

        document.getElementById('writing-prompt-title').innerText = content.title;
        
        let promptHTML = content.prompt;
        if (content.data_table) {
            promptHTML += `\n\n[DATA TABLE]\n` + content.data_table.headers.join(' | ') + '\n' +
                content.data_table.rows.map(r => r.join(' | ')).join('\n');
        }
        document.getElementById('writing-prompt-content').innerText = promptHTML;
        
        // Update model answer modal
        document.getElementById('modal-model-answer-content').innerText = content.band9_sample || 'Model answer not available';

        // Update assigned exam badge
        const isGT = currentWritingTask?.type === 'General Training';
        const badgeEl = document.getElementById('badge-writing-test-id');
        if (badgeEl) badgeEl.innerText = `Exam Task: ${taskId} [${isGT ? 'General Training' : 'Academic'}]`;

        // Set buttons for Task 1 vs Task 2
        const isTask1 = content.task_type === 'Task 1' || (parseInt(taskId.replace(/^(W|GTW)-/, ''), 10) % 2 === 0);
        const activeClass = 'px-3.5 py-1.5 rounded-lg text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300 transition-colors shadow-xs';
        const inactiveClass = 'px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:bg-slate-100 transition-colors';
        const btn1 = document.getElementById('btn-w-task1');
        const btn2 = document.getElementById('btn-w-task2');
        if (btn1) {
            btn1.className = isTask1 ? activeClass : inactiveClass;
            btn1.innerText = isGT ? 'Task 1: Letter Writing (150 words)' : 'Task 1: Visual Report (150 words)';
        }
        if (btn2) {
            btn2.className = !isTask1 ? activeClass : inactiveClass;
            btn2.innerText = 'Task 2: Discursive Essay (250 words)';
        }

        // Set contextual placeholder
        const textarea = document.getElementById('writing-textarea');
        if (textarea) {
            if (isGT && isTask1) {
                const subtype = content.subtype || 'Letter';
                textarea.placeholder = `IELTS General Training Task 1 (${subtype}).\n\nBegin your letter with an appropriate opening (e.g. "Dear Sir or Madam," or "Dear Mr. Davies," or "Dear Sarah,").\n\nClearly address all 3 bullet points with relevant details and appropriate tone...\n\nSign off appropriately (e.g. "Yours faithfully," / "Yours sincerely," / "Best regards,") followed by your name. (Minimum 150 words)`;
            } else if (!isGT && isTask1) {
                textarea.placeholder = `IELTS Academic Task 1 (Visual Data Report).\n\nSummarize the information by selecting and reporting the main features, and make comparisons where relevant...\n\nStructure with an introduction/paraphrase, a clear overview of main trends, and detailed data paragraphs. (Minimum 150 words)`;
            } else {
                textarea.placeholder = `IELTS Writing Task 2 (Discursive Essay).\n\nType your response here. Structure with an introduction and clear thesis statement, 2-3 body paragraphs with topic sentences, explanations and evidence, and a cohesive conclusion. (Minimum 250 words)`;
            }
        }

        // Sync dropdown
        const selectEl = document.getElementById('select-writing-test');
        if (selectEl) selectEl.value = taskId;

        updateWordCount();

        // Reset official writing countdown (20 min for Task 1, 40 min for Task 2)
        resetWritingTimer(isTask1 ? 1200 : 2400);
        if (isViewActive('writing')) {
            startWritingTimer();
        }

    } catch (err) {
        console.error('Failed loading writing task:', err);
    }
}

function selectWritingTask(taskId) {
    loadWritingTask(taskId);
}

function updateWordCount() {
    const text = document.getElementById('writing-textarea').value.trim();
    const count = text ? text.split(/\s+/).length : 0;
    const minWords = currentWritingTask?.content?.task_type === 'Task 1' ? 150 : 250;
    const badge = document.getElementById('writing-word-counter');

    badge.innerText = `${count} / ${minWords} words`;
    if (count >= minWords) {
        badge.className = 'text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200';
    } else {
        badge.className = 'text-xs font-bold px-2.5 py-1 rounded-full bg-rose-50 text-rose-600 border border-rose-200';
    }
}

async function callGeminiFromBrowser(prompt, systemInstruction) {
    const key = document.getElementById('set-gemini-key').value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');
    const model = document.getElementById('set-gemini-model').value || 'gemini-3.8-flash';
    if (!key) return null;

    const modelsToTry = [model, 'gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-1.5-flash'];
    for (const m of [...new Set(modelsToTry)]) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${key}`;
        const payload = {
            contents: [{ role: 'user', parts: [{ text: prompt }] }],
            generationConfig: {
                temperature: 0.2,
                responseMimeType: 'application/json'
            }
        };
        if (systemInstruction) {
            payload.systemInstruction = { parts: [{ text: systemInstruction }] };
        }

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 22000);
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!res.ok) continue;

            const data = await res.json();
            const candidateText = data.candidates?.[0]?.content?.parts?.[0]?.text;
            if (candidateText) {
                const cleaned = candidateText.replace(/^```json\s*/, '').replace(/```$/, '').trim();
                return JSON.parse(cleaned);
            }
        } catch (err) {
            console.warn(`Browser direct call to ${m} skipped/timed out:`, err.message);
        }
    }
    return null;
}

async function submitWritingEvaluation() {
    const essay = document.getElementById('writing-textarea').value.trim();
    if (essay.split(/\s+/).length < 20) {
        alert('Please write at least 20 words before submitting for examiner evaluation.');
        return;
    }

    const submitBtn = document.getElementById('btn-submit-writing');
    const label = document.getElementById('writing-submit-label');
    const spinner = document.getElementById('writing-spinner');

    submitBtn.disabled = true;
    label.innerText = 'Gemini Examiner Assessing...';
    spinner.classList.remove('hidden');

    try {
        let evaluation = null;
        const key = document.getElementById('set-gemini-key').value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');
        
        if (key) {
            const taskType = currentWritingTask?.content?.task_type || 'Task 2';
            const promptTitle = currentWritingTask?.content?.title || '';
            const promptText = currentWritingTask?.content?.prompt || '';
            const minWords = taskType === 'Task 1' ? 150 : 250;

            const isGT = currentWritingTask?.type === 'General Training';
            const sys = "You are an expert Cambridge/IDP Certified Senior IELTS Writing Examiner. Assess the student submission rigorously according to the official IELTS 9-band descriptors: 1. Task Achievement / Response, 2. Coherence and Cohesion, 3. Lexical Resource, 4. Grammatical Range and Accuracy. You must respond in strict JSON matching the requested schema.";
            
            let letterGuide = '';
            if (isGT && taskType === 'Task 1') {
                const subtype = currentWritingTask?.content?.subtype || 'Letter';
                letterGuide = `\nSpecial General Training Task 1 (${subtype}) Requirements:\n- Check opening salutation (e.g. Dear Sir or Madam / Dear Mr. Davies / Dear Sarah) and closing sign-off (e.g. Yours faithfully / Yours sincerely / Best regards).\n- Verify that all 3 bullet points in the prompt are addressed with clear, relevant extension.\n- Verify that the tone/register is consistent (${subtype}).\n`;
            }

            const userPrompt = `IELTS WRITING EVALUATION REQUEST\nExam Module: ${isGT ? 'General Training' : 'Academic'}\nTask Type: ${taskType}\nTarget Minimum Word Count: ${minWords} words\nPrompt Title: ${promptTitle}\nOfficial Question: """${promptText}"""${letterGuide}\nStudent Essay: """${essay}"""\n\nPlease evaluate this submission and return a JSON object with this EXACT structure:\n{\n  "overall_band": 6.5,\n  "criteria": {\n    "task_achievement": {"band": 6.5, "comment": "..."},\n    "coherence_cohesion": {"band": 6.5, "comment": "..."},\n    "lexical_resource": {"band": 7.0, "comment": "..."},\n    "grammatical_range_accuracy": {"band": 6.0, "comment": "..."}\n  },\n  "word_count": ${essay.split(/\s+/).length},\n  "strengths": ["...", "..."],\n  "areas_to_improve": ["...", "..."],\n  "line_by_line_corrections": [{"original": "...", "correction": "...", "explanation": "...", "type": "grammar"}],\n  "vocabulary_upgrades": [{"basic_word": "...", "band8_alternative": "...", "example_sentence": "..."}],\n  "model_paragraph": "..."\n}`;

            evaluation = await callGeminiFromBrowser(userPrompt, sys);
        }

        const res = await fetch(`${API_BASE}/api/attempts/writing`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_id: currentWritingTask.id,
                essay: essay,
                time_spent_seconds: 1200,
                evaluation: evaluation
            })
        });

        const data = await res.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        renderWritingReport(data.evaluation);
        await refreshData();
    } catch (err) {
        alert('Error evaluating essay: ' + err.message);
    } finally {
        submitBtn.disabled = false;
        label.innerText = 'Evaluate with Gemini Examiner';
        spinner.classList.add('hidden');
    }
}

function renderWritingReport(evalData) {
    const container = document.getElementById('writing-report-container');
    container.classList.remove('hidden');

    const c = evalData.criteria;

    container.innerHTML = `
        <!-- Evaluation Summary Banner -->
        <div class="bg-gradient-to-r from-brand-600 to-indigo-700 rounded-2xl p-6 text-white shadow-lg">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="text-xs uppercase tracking-wider text-indigo-200 font-bold">Official Examiner Assessment</span>
                    <h3 class="text-2xl font-black mt-1">Overall Band Score: ${evalData.overall_band.toFixed(1)}</h3>
                    <p class="text-xs text-indigo-100 mt-1">Word Count: ${evalData.word_count} words ${evalData.note || ''}</p>
                </div>
                <div class="flex items-center gap-2">
                    <span class="px-3 py-1 rounded-xl bg-white/20 backdrop-blur-sm text-xs font-semibold">
                        Certified IELTS Rubric
                    </span>
                </div>
            </div>
        </div>

        <!-- 4 Criteria Breakdown Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Task Achievement</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-brand-50 text-brand-700">Band ${c.task_achievement.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.task_achievement.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Coherence & Cohesion</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-brand-50 text-brand-700">Band ${c.coherence_cohesion.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.coherence_cohesion.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Lexical Resource</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-brand-50 text-brand-700">Band ${c.lexical_resource.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.lexical_resource.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Grammar Range & Acc.</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-brand-50 text-brand-700">Band ${c.grammatical_range_accuracy.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.grammatical_range_accuracy.comment}</p>
            </div>
        </div>

        <!-- Line-by-Line Grammar & Syntax Corrections -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <h4 class="font-bold text-slate-900 text-sm mb-3 flex items-center gap-2">
                <span class="text-amber-500">✍️</span> Precise Line-by-Line Corrections & Explanations
            </h4>
            <div class="space-y-3">
                ${(evalData.line_by_line_corrections || []).map(corr => `
                    <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 space-y-1.5 text-xs">
                        <div class="text-rose-600 line-through">"${corr.original}"</div>
                        <div class="text-emerald-700 font-bold">↳ "${corr.correction}"</div>
                        <div class="text-slate-500 italic text-[11px]">${corr.explanation}</div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Band 8+ Vocabulary Upgrades -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <h4 class="font-bold text-slate-900 text-sm mb-3 flex items-center gap-2">
                <span class="text-purple-500">💎</span> Band 8+ Lexical Upgrades (Click to Save to Notebook)
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                ${(evalData.vocabulary_upgrades || []).map(upg => `
                    <div class="p-3.5 rounded-xl bg-purple-50/50 border border-purple-200 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between text-xs mb-1">
                                <span class="text-slate-500">Original: <span class="font-semibold text-slate-700">${upg.basic_word}</span></span>
                                <span class="px-2 py-0.5 rounded bg-purple-100 text-purple-800 font-bold text-[10px]">Band 8+</span>
                            </div>
                            <div class="font-bold text-purple-900 text-sm mb-1">${upg.band8_alternative}</div>
                            <p class="text-[11px] text-slate-600 italic">"${upg.example_sentence}"</p>
                        </div>
                        <button onclick="quickSaveVocab('${upg.band8_alternative}', '${upg.example_sentence.replace(/'/g, "\\'")}', 'Writing')" class="mt-3 py-1 px-2.5 rounded-lg bg-white border border-purple-200 text-purple-700 hover:bg-purple-600 hover:text-white text-xs font-semibold transition-colors self-start">
                            + Add to Vocabulary Notebook
                        </button>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- Model Elevation Paragraph -->
        ${evalData.model_paragraph ? `
            <div class="bg-slate-900 rounded-2xl p-6 text-white shadow-sm">
                <div class="text-amber-400 text-xs font-bold uppercase tracking-wider mb-2">Examiner Model Paragraph Sample</div>
                <p class="text-xs text-slate-200 leading-relaxed font-serif">${evalData.model_paragraph}</p>
            </div>
        ` : ''}
    `;

    container.scrollIntoView({ behavior: 'smooth' });
}

function openModelAnswerModal() {
    document.getElementById('modal-model-answer').classList.remove('hidden');
}

function closeModelAnswerModal() {
    document.getElementById('modal-model-answer').classList.add('hidden');
}
/**
 * IELTS Master - Speaking Module
 * Handles Speaking Part 1/2/3 navigation, audio prompts, speech recognition / live mic transcribing,
 * cue-card prep and response countdown timers, Gemini live examiner evaluation, and detailed score reporting.
 */

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        speechRecognitionInstance = new SpeechRecognition();
        speechRecognitionInstance.continuous = true;
        speechRecognitionInstance.interimResults = true;
        speechRecognitionInstance.lang = 'en-US';
    }
}

async function loadSpeakingTest(testId) {
    try {
        const res = await fetch(`${API_BASE}/api/tests/${testId}`);
        currentSpeakingTest = await res.json();
        
        const titleEl = document.getElementById('speaking-test-title');
        if (titleEl) titleEl.innerText = currentSpeakingTest.title;

        // Update assigned exam badge
        const badgeEl = document.getElementById('badge-speaking-test-id');
        if (badgeEl) badgeEl.innerText = `Interview: ${testId}`;

        // Sync dropdown
        const selectEl = document.getElementById('select-speaking-test');
        if (selectEl) selectEl.value = testId;

        renderSpeakingPart(1);

        // Reset official 14-minute speaking window timer
        resetOverallSpeakingTimer();
        if (isViewActive('speaking')) {
            startOverallSpeakingTimer();
        }

    } catch (err) {
        console.error('Failed loading speaking test:', err);
    }
}

function switchSpeakingPart(partNum) {
    activeSpeakingPart = partNum;
    ['part1', 'part2', 'part3'].forEach((p, idx) => {
        const btn = document.getElementById(`btn-spk-${p}`);
        if (btn) {
            btn.className = (idx + 1) === partNum
                ? 'px-3 py-1 rounded-md bg-white shadow-sm text-slate-800 font-bold'
                : 'px-3 py-1 rounded-md text-slate-600 hover:text-slate-900';
        }
    });

    renderSpeakingPart(partNum);
}

function renderSpeakingPart(partNum) {
    if (!currentSpeakingTest) return;
    const content = currentSpeakingTest.content;
    const qaContainer = document.getElementById('speaking-qa-container');
    const p2Container = document.getElementById('speaking-part2-container');

    if (partNum === 2) {
        qaContainer.classList.add('hidden');
        p2Container.classList.remove('hidden');
        document.getElementById('cue-card-text').innerText = content.part2.cue_card;
    } else {
        qaContainer.classList.remove('hidden');
        p2Container.classList.add('hidden');

        const questions = partNum === 1 ? content.part1.questions : content.part3.questions;
        const partTitle = partNum === 1 ? content.part1.title : content.part3.title;

        qaContainer.innerHTML = `
            <div class="border-b border-slate-100 pb-2 mb-4 flex items-center justify-between">
                <span class="font-bold text-slate-800 text-xs uppercase tracking-wider">${partTitle}</span>
                <span class="text-xs text-slate-400">Click speaker to hear examiner voice</span>
            </div>
            ${questions.map((q, idx) => {
                const savedAnswer = speakingResponses[`Part ${partNum}_${q.text}`]?.answer || '';
                return `
                <div class="p-4 rounded-xl bg-slate-50 border border-slate-200/70 space-y-3">
                    <div class="flex items-start justify-between gap-3">
                        <div class="text-xs font-bold text-slate-800 leading-snug">
                            Examiner: "${q.text}"
                        </div>
                        <button onclick="playExaminerVoice('${q.audio_prompt.replace(/'/g, "\\'")}', this)" class="p-1.5 rounded-lg bg-white border border-slate-200 text-indigo-600 hover:bg-indigo-50 shrink-0" title="Listen to Examiner">
                            🔊
                        </button>
                    </div>

                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] text-slate-500 font-medium">Candidate Response:</span>
                            <button onclick="toggleSpeechRecognition('spk-ans-p${partNum}-${idx}')" id="btn-rec-p${partNum}-${idx}" class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-100 flex items-center gap-1 transition-colors">
                                <span>🎤 Transcribe Voice</span>
                            </button>
                        </div>
                        <textarea id="spk-ans-p${partNum}-${idx}" rows="3" oninput="saveSpeakingResponse('Part ${partNum}', '${q.text.replace(/'/g, "\\'")}', this.value)" class="w-full p-2.5 rounded-lg border border-slate-200 text-xs text-slate-800 focus:ring-2 focus:ring-emerald-500 bg-white" placeholder="Speak into mic or type your answer here...">${savedAnswer}</textarea>
                    </div>
                </div>
            `}).join('')}
        `;
    }
}

function saveSpeakingResponse(part, question, answer) {
    speakingResponses[`${part}_${question}`] = { part, question, answer };
}

let activeSpeechTargetId = null;
let speechBaseText = '';

function getMicButton(targetTextareaId) {
    if (targetTextareaId === 'part2-transcript') {
        return document.getElementById('btn-mic-part2');
    }
    const btnId = targetTextareaId.replace('spk-ans-', 'btn-rec-');
    return document.getElementById(btnId);
}

function stopSpeechRecognition() {
    if (speechRecognitionInstance) {
        try {
            speechRecognitionInstance.onresult = null;
            speechRecognitionInstance.onerror = null;
            speechRecognitionInstance.onend = null;
            speechRecognitionInstance.stop();
        } catch (e) {}
    }
    if (activeSpeechTargetId) {
        const btn = getMicButton(activeSpeechTargetId);
        if (btn) {
            if (activeSpeechTargetId === 'part2-transcript') {
                btn.className = 'px-3 py-1 text-xs font-bold rounded-lg bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-100 flex items-center gap-1.5 transition-colors';
                btn.innerHTML = '<span>🎤 Speak into Microphone</span>';
            } else {
                btn.className = 'px-2.5 py-1 text-[11px] font-bold rounded-lg bg-rose-50 text-rose-600 border border-rose-200 hover:bg-rose-100 flex items-center gap-1 transition-colors';
                btn.innerHTML = '<span>🎤 Transcribe Voice</span>';
            }
        }
    }
    isRecording = false;
    activeSpeechTargetId = null;
    speechBaseText = '';
}

function toggleSpeechRecognition(targetTextareaId) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Web Speech Recognition API is not supported in this browser. Please type your answer directly into the textarea.');
        return;
    }

    const textarea = document.getElementById(targetTextareaId);
    if (!textarea) return;

    // If already recording for this exact textarea, stop it
    if (isRecording && activeSpeechTargetId === targetTextareaId) {
        stopSpeechRecognition();
        return;
    }

    // If recording for a different textarea, stop that first
    if (isRecording) {
        stopSpeechRecognition();
    }

    activeSpeechTargetId = targetTextareaId;
    speechBaseText = textarea.value.trim();

    // Update active button UI to recording
    const btn = getMicButton(targetTextareaId);
    if (btn) {
        btn.className = 'px-2.5 py-1 text-[11px] font-bold rounded-lg bg-rose-600 text-white animate-pulse shadow-md flex items-center gap-1.5 transition-colors';
        btn.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-white mr-0.5 animate-ping"></span><span>⏹ Stop Recording</span>';
    }

    try {
        speechRecognitionInstance = new SpeechRecognition();
        speechRecognitionInstance.continuous = true;
        speechRecognitionInstance.interimResults = true;
        speechRecognitionInstance.lang = 'en-US';

        speechRecognitionInstance.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = 0; i < event.results.length; ++i) {
                const item = event.results[i];
                if (item.isFinal) {
                    finalTranscript += item[0].transcript + ' ';
                } else {
                    interimTranscript += item[0].transcript;
                }
            }

            finalTranscript = finalTranscript.trim();
            interimTranscript = interimTranscript.trim();

            let currentSpeech = '';
            if (finalTranscript && interimTranscript) {
                currentSpeech = finalTranscript + ' ' + interimTranscript;
            } else {
                currentSpeech = finalTranscript || interimTranscript;
            }

            if (speechBaseText) {
                textarea.value = speechBaseText + (currentSpeech ? ' ' + currentSpeech : '');
            } else {
                textarea.value = currentSpeech;
            }

            // Trigger input event to update state and listeners
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
        };

        speechRecognitionInstance.onerror = (event) => {
            console.warn('Speech recognition warning:', event.error);
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                alert('Microphone permission was denied. Please allow microphone access in your browser settings.');
                stopSpeechRecognition();
            } else if (event.error !== 'no-speech') {
                stopSpeechRecognition();
            }
        };

        speechRecognitionInstance.onend = () => {
            stopSpeechRecognition();
        };

        speechRecognitionInstance.start();
        isRecording = true;
    } catch (err) {
        console.error('Failed to start speech recognition:', err);
        stopSpeechRecognition();
    }
}

function startPrepTimer() {
    let timeLeft = 60;
    const timerEl = document.getElementById('timer-prep');
    const btn = document.getElementById('btn-start-prep');
    btn.disabled = true;

    if (prepTimerInterval) clearInterval(prepTimerInterval);
    prepTimerInterval = setInterval(() => {
        timeLeft--;
        timerEl.innerText = `00:${String(timeLeft).padStart(2, '0')}`;
        if (timeLeft <= 0) {
            clearInterval(prepTimerInterval);
            timerEl.innerText = "00:00 (Time's up! Begin speaking)";
            btn.disabled = false;
            playExaminerVoice("One minute preparation is up. Please begin speaking now.");
        }
    }, 1000);
}

function startSpeakingTimer() {
    let timeLeft = 120;
    const timerEl = document.getElementById('timer-speak');
    const btn = document.getElementById('btn-start-speak');
    btn.disabled = true;

    if (speakingTimerInterval) clearInterval(speakingTimerInterval);
    speakingTimerInterval = setInterval(() => {
        timeLeft--;
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        timerEl.innerText = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        if (timeLeft <= 0) {
            clearInterval(speakingTimerInterval);
            timerEl.innerText = "00:00 (Completed)";
            btn.disabled = false;
            playExaminerVoice("Thank you. That is two minutes. We will now move on.");
        }
    }, 1000);
}

async function submitSpeakingEvaluation() {
    stopSpeechRecognition();
    // Gather all responses
    const p2Ans = document.getElementById('part2-transcript').value.trim();
    if (p2Ans) {
        speakingResponses['Part2_CueCard'] = {
            part: 'Part 2',
            question: document.getElementById('cue-card-text').innerText,
            answer: p2Ans
        };
    }

    const responsesArray = Object.values(speakingResponses);
    if (responsesArray.length === 0) {
        alert('Please answer or record at least one question before requesting Gemini examiner evaluation.');
        return;
    }

    const submitBtn = document.getElementById('btn-submit-speaking');
    const label = document.getElementById('speaking-submit-label');
    const spinner = document.getElementById('speaking-spinner');

    submitBtn.disabled = true;
    label.innerText = 'Gemini Assessing Speech...';
    spinner.classList.remove('hidden');

    try {
        let evaluation = null;
        const key = document.getElementById('set-gemini-key').value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');
        
        if (key) {
            const qaFormatted = responsesArray.map(r => `[${r.part}] Examiner: ${r.question}\nCandidate: ${r.answer}\n`).join('\n');
            const sys = "You are an expert Cambridge/IDP Certified Senior IELTS Speaking Examiner. Assess the candidate spoken transcript across the 4 official IELTS criteria: 1. Fluency and Coherence, 2. Lexical Resource, 3. Grammatical Range and Accuracy, 4. Pronunciation & Delivery Insights. You must respond in strict JSON matching the requested schema.";
            const userPrompt = `IELTS SPEAKING INTERVIEW EVALUATION REQUEST\nInterview Transcript:\n${qaFormatted}\n\nPlease evaluate this interview transcript and return a JSON object with this EXACT structure:\n{\n  "overall_band": 6.5,\n  "criteria": {\n    "fluency_coherence": {"band": 6.5, "comment": "..."},\n    "lexical_resource": {"band": 7.0, "comment": "..."},\n    "grammatical_range_accuracy": {"band": 6.0, "comment": "..."},\n    "pronunciation": {"band": 6.5, "comment": "..."}\n  },\n  "filler_words_detected": ["..."],\n  "strengths": ["...", "..."],\n  "areas_to_improve": ["...", "..."],\n  "expansion_advice": "...",\n  "better_expressions": [{"spoken": "...", "upgraded": "...", "reason": "..."}]\n}`;

            evaluation = await callGeminiFromBrowser(userPrompt, sys);
        }

        const res = await fetch(`${API_BASE}/api/attempts/speaking`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_id: currentSpeakingTest.id,
                responses: responsesArray,
                time_spent_seconds: 700,
                evaluation: evaluation
            })
        });

        const data = await res.json();
        renderSpeakingReport(data.evaluation);
        await refreshData();
    } catch (err) {
        alert('Error evaluating speaking: ' + err.message);
    } finally {
        submitBtn.disabled = false;
        label.innerText = 'Evaluate Interview with Gemini AI';
        spinner.classList.add('hidden');
    }
}

function renderSpeakingReport(evalData) {
    const container = document.getElementById('speaking-report-container');
    container.classList.remove('hidden');
    const c = evalData.criteria;

    container.innerHTML = `
        <!-- Header Banner -->
        <div class="bg-gradient-to-r from-emerald-600 to-teal-700 rounded-2xl p-6 text-white shadow-lg">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="text-xs uppercase tracking-wider text-emerald-200 font-bold">IELTS Speaking Examiner Report</span>
                    <h3 class="text-2xl font-black mt-1">Estimated Band Score: ${evalData.overall_band.toFixed(1)}</h3>
                    <p class="text-xs text-emerald-100 mt-1">Assessed across 4 Cambridge/IDP criteria</p>
                </div>
                <div class="flex items-center gap-2">
                    <span class="px-3 py-1 rounded-xl bg-white/20 backdrop-blur-sm text-xs font-semibold">
                        Gemini Examiner Evaluation
                    </span>
                </div>
            </div>
        </div>

        <!-- 4 Criteria Breakdown -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Fluency & Coherence</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700">Band ${c.fluency_coherence.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.fluency_coherence.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Lexical Resource</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700">Band ${c.lexical_resource.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.lexical_resource.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Grammar Range & Acc.</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700">Band ${c.grammatical_range_accuracy.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.grammatical_range_accuracy.comment}</p>
            </div>

            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-700">Pronunciation / Delivery</span>
                    <span class="px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700">Band ${c.pronunciation.band}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed">${c.pronunciation.comment}</p>
            </div>
        </div>

        <!-- Filler Words & Fluency Markers -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <h4 class="font-bold text-slate-900 text-sm mb-2 flex items-center gap-2">
                <span>⏱️</span> Filler Words & Hesitation Analysis
            </h4>
            <div class="flex flex-wrap gap-2 mt-2">
                ${(evalData.filler_words_detected || []).map(f => `
                    <span class="px-3 py-1 rounded-lg text-xs font-medium bg-amber-50 text-amber-800 border border-amber-200">
                        ${f}
                    </span>
                `).join('')}
            </div>
            <p class="text-xs text-slate-500 mt-3 leading-relaxed">
                ${evalData.expansion_advice || 'Use the PREP framework to structure smooth discourse without hesitation.'}
            </p>
        </div>

        <!-- Better Native Expressions -->
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <h4 class="font-bold text-slate-900 text-sm mb-3 flex items-center gap-2">
                <span>🗣️</span> Upgraded Idiomatic Expressions (Band 8+ Conversational Native Style)
            </h4>
            <div class="space-y-3">
                ${(evalData.better_expressions || []).map(expr => `
                    <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                        <div>
                            <div class="text-slate-500">You said: <span class="font-medium text-slate-800">"${expr.spoken}"</span></div>
                            <div class="text-emerald-700 font-bold mt-0.5">↳ Native Upgrade: "${expr.upgraded}"</div>
                            <div class="text-slate-400 text-[11px] mt-0.5">${expr.reason}</div>
                        </div>
                        <button onclick="quickSaveVocab('${expr.upgraded}', 'Speaking collocation: ${expr.reason.replace(/'/g, "\\'")}', 'Speaking')" class="px-3 py-1 rounded-lg bg-white border border-slate-200 text-purple-700 hover:bg-purple-50 font-semibold self-start sm:self-auto shrink-0">
                            + Add to Vocab
                        </button>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    container.scrollIntoView({ behavior: 'smooth' });
}
/**
 * IELTS Master - Vocabulary Module
 * Handles Band 8+ academic collocation notebook, search/filtering, modal CRUD,
 * mastery toggling, and standards modal display.
 */

async function loadVocabulary() {
    try {
        const res = await fetch(`${API_BASE}/api/vocabulary`);
        vocabularyList = await res.json();
        renderVocabularyGrid(vocabularyList);
    } catch (err) {
        console.error('Failed loading vocabulary:', err);
    }
}

function renderVocabularyGrid(list) {
    const grid = document.getElementById('vocab-cards-grid');
    if (!grid) return;
    if (!list || list.length === 0) {
        grid.innerHTML = '<div class="col-span-full p-8 text-center text-xs text-slate-400">No vocabulary items added yet. Click "+ Add Collocation" or save suggestions from your Writing & Speaking reports!</div>';
        return;
    }

    grid.innerHTML = list.map(item => `
        <div class="p-4 rounded-xl bg-white border border-slate-200 shadow-sm flex flex-col justify-between hover:border-purple-300 transition-colors">
            <div>
                <div class="flex items-center justify-between mb-1.5">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700">${item.module_source || 'General'}</span>
                    <button onclick="toggleMastered(${item.id})" class="text-xs ${item.mastered ? 'text-emerald-600 font-bold' : 'text-slate-400 hover:text-slate-600'}">
                        ${item.mastered ? '✓ Mastered' : '○ Review'}
                    </button>
                </div>
                <h4 class="font-bold text-slate-900 text-sm mb-1">${item.word_or_phrase}</h4>
                <p class="text-xs text-slate-600 mb-2">${item.meaning || ''}</p>
                ${item.context ? `<p class="text-[11px] text-slate-500 italic bg-slate-50 p-2 rounded-lg border border-slate-100">"${item.context}"</p>` : ''}
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                <span>${item.band_level || 'Band 8+'}</span>
                <button onclick="deleteVocab(${item.id})" class="text-rose-500 hover:text-rose-700">Delete</button>
            </div>
        </div>
    `).join('');
}

function filterVocabulary() {
    const query = document.getElementById('vocab-search').value.toLowerCase();
    const mod = document.getElementById('vocab-filter-module').value;

    const filtered = vocabularyList.filter(item => {
        const matchesQuery = item.word_or_phrase.toLowerCase().includes(query) ||
                             (item.meaning && item.meaning.toLowerCase().includes(query)) ||
                             (item.context && item.context.toLowerCase().includes(query));
        const matchesMod = mod === 'all' || (item.module_source && item.module_source.toLowerCase().includes(mod.toLowerCase()));
        return matchesQuery && matchesMod;
    });

    renderVocabularyGrid(filtered);
}

async function quickSaveVocab(word, context, module_source) {
    try {
        await fetch(`${API_BASE}/api/vocabulary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                word: word,
                context: context,
                band_level: 'Band 8+',
                module_source: module_source
            })
        });
        alert(`Saved "${word}" to your Band 8+ Vocabulary Notebook!`);
        await loadVocabulary();
    } catch (err) {
        alert('Failed saving word: ' + err.message);
    }
}

function openAddVocabModal() {
    document.getElementById('modal-add-vocab').classList.remove('hidden');
}

function closeAddVocabModal() {
    document.getElementById('modal-add-vocab').classList.add('hidden');
}

async function saveNewVocabulary() {
    const word = document.getElementById('add-vocab-word').value.trim();
    const meaning = document.getElementById('add-vocab-meaning').value.trim();
    const context = document.getElementById('add-vocab-context').value.trim();
    const module_source = document.getElementById('add-vocab-module').value;

    if (!word) {
        alert('Please enter a word or collocation phrase.');
        return;
    }

    try {
        await fetch(`${API_BASE}/api/vocabulary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word, meaning, context, module_source, band_level: 'Band 8+' })
        });
        closeAddVocabModal();
        await loadVocabulary();
    } catch (err) {
        alert('Error saving word: ' + err.message);
    }
}

async function toggleMastered(id) {
    try {
        await fetch(`${API_BASE}/api/vocabulary/${id}/toggle`, { method: 'POST' });
        await loadVocabulary();
    } catch (err) {
        console.error('Failed toggling word:', err);
    }
}

async function deleteVocab(id) {
    if (!confirm('Are you sure you want to delete this word from your notebook?')) return;
    try {
        await fetch(`${API_BASE}/api/vocabulary/${id}`, { method: 'DELETE' });
        await loadVocabulary();
    } catch (err) {
        console.error('Failed deleting word:', err);
    }
}

function toggleIeltsStandardsModal(isOpen) {
    const modal = document.getElementById('modal-ielts-standards');
    if (!modal) return;
    if (isOpen) {
        modal.classList.remove('hidden');
    } else {
        modal.classList.add('hidden');
    }
}
/**
 * IELTS Master - Main Application Orchestrator
 * Coordinates view switching, timer lifecycle between tabs, and bootstrap initialization.
 */

function getActiveTestRunningModule() {
    const viewListening = document.getElementById('view-listening');
    if (viewListening && !viewListening.classList.contains('hidden') && currentListeningTest && !currentListeningResults) {
        return 'listening';
    }
    const viewReading = document.getElementById('view-reading');
    if (viewReading && !viewReading.classList.contains('hidden') && currentReadingTest && !currentReadingResults) {
        return 'reading';
    }
    const viewWriting = document.getElementById('view-writing');
    if (viewWriting && !viewWriting.classList.contains('hidden') && currentWritingTask) {
        return 'writing';
    }
    const viewSpeaking = document.getElementById('view-speaking');
    if (viewSpeaking && !viewSpeaking.classList.contains('hidden') && currentSpeakingTest) {
        return 'speaking';
    }
    return null;
}

function requestExitActiveTest(moduleName = null) {
    pendingExitModule = moduleName || getActiveTestRunningModule();
    pendingExitTargetView = 'dashboard';
    const modal = document.getElementById('modal-exit-test');
    if (modal) modal.classList.remove('hidden');
}

function cancelExitActiveTest() {
    pendingExitTargetView = null;
    pendingExitModule = null;
    const modal = document.getElementById('modal-exit-test');
    if (modal) modal.classList.add('hidden');
}

function confirmExitActiveTest() {
    const modal = document.getElementById('modal-exit-test');
    if (modal) modal.classList.add('hidden');

    const mod = pendingExitModule || getActiveTestRunningModule();
    if (mod === 'reading') {
        if (currentReadingTest) lastExitedTestId.reading = currentReadingTest.id;
        currentReadingTest = null;
        currentReadingResults = null;
        if (typeof resetReadingTimer === 'function') resetReadingTimer();
        const sheet = document.getElementById('reading-answer-sheet');
        if (sheet) sheet.innerHTML = '';
        const passageTextEl = document.getElementById('reading-passage-text');
        if (passageTextEl) passageTextEl.innerHTML = '';
        const passageTitleEl = document.getElementById('reading-passage-title');
        if (passageTitleEl) passageTitleEl.innerText = '';
    } else if (mod === 'listening') {
        if (currentListeningTest) lastExitedTestId.listening = currentListeningTest.id;
        currentListeningTest = null;
        currentListeningResults = null;
        if (typeof resetListeningTimer === 'function') resetListeningTimer();
        if (typeof stopAnyActiveAudio === 'function') stopAnyActiveAudio();
        const sheet = document.getElementById('listening-answer-sheet');
        if (sheet) sheet.innerHTML = '';
    } else if (mod === 'writing') {
        if (currentWritingTask) lastExitedTestId.writing = currentWritingTask.id;
        currentWritingTask = null;
        if (typeof resetWritingTimer === 'function') resetWritingTimer();
        const textInput = document.getElementById('writing-input');
        if (textInput) textInput.value = '';
    } else if (mod === 'speaking') {
        if (currentSpeakingTest) lastExitedTestId.speaking = currentSpeakingTest.id;
        currentSpeakingTest = null;
        if (typeof resetOverallSpeakingTimer === 'function') resetOverallSpeakingTimer();
        if (typeof stopSpeechRecognition === 'function') stopSpeechRecognition();
    }

    const targetView = pendingExitTargetView || 'dashboard';
    pendingExitTargetView = null;
    pendingExitModule = null;
    switchView(targetView, true);
}

function switchView(viewName, force = false) {
    if (!force) {
        const activeModule = getActiveTestRunningModule();
        // If candidate is actively taking a test and attempts to switch to a different view
        if (activeModule && activeModule !== viewName) {
            pendingExitModule = activeModule;
            pendingExitTargetView = viewName;
            const modal = document.getElementById('modal-exit-test');
            if (modal) {
                modal.classList.remove('hidden');
                return;
            }
        }
    }

    toggleMobileDrawer(false); // Dismiss drawer on mobile navigation
    const views = ['dashboard', 'listening', 'reading', 'writing', 'speaking', 'vocabulary', 'settings'];
    views.forEach(v => {
        const el = document.getElementById(`view-${v}`);
        const nav = document.getElementById(`nav-${v}`);
        const mobNav = document.getElementById(`mobile-nav-${v}`);
        if (el) el.classList.toggle('hidden', v !== viewName);
        if (nav) nav.classList.toggle('active', v === viewName);
        if (mobNav) mobNav.classList.toggle('active', v === viewName);
    });

    const isGT = (typeof appSettings !== 'undefined' && appSettings.exam_type === 'General Training') || (typeof currentUser !== 'undefined' && currentUser?.exam_type === 'General Training');
    const titles = {
        dashboard: 'Dashboard & Improvement Analytics',
        listening: 'IELTS Listening Practice & Simulator',
        reading: isGT ? 'IELTS General Training Reading (Split-Screen)' : 'IELTS Academic Reading (Split-Screen)',
        writing: isGT ? 'IELTS General Training Writing (Letter & Essay)' : 'IELTS Academic Writing (Report & Essay)',
        speaking: 'IELTS Speaking Live Examiner Mock',
        vocabulary: 'Band 8+ Academic Vocabulary Notebook',
        settings: 'Settings & Gemini AI Configuration'
    };
    const titleEl = document.getElementById('view-title');
    if (titleEl) {
        titleEl.innerText = titles[viewName] || 'IELTS Master';
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Clean up active listening audio if leaving listening
    if (viewName !== 'listening' && typeof stopAnyActiveAudio === 'function') {
        stopAnyActiveAudio();
    }
    // Clean up speech recognition if leaving speaking
    if (viewName !== 'speaking' && typeof stopSpeechRecognition === 'function') {
        stopSpeechRecognition();
    }

    // Pause all module timers to prevent background drain on dashboard / other tabs
    if (typeof pauseAllExamTimers === 'function') {
        pauseAllExamTimers();
    }

    // Start or resume timer for the currently entered module
    if (viewName === 'listening') {
        if (!currentListeningTest) {
            loadRandomListeningTest(false).then(() => {
                if (isViewActive('listening') && typeof startListeningTimer === 'function') startListeningTimer();
            });
        } else {
            if (typeof startListeningTimer === 'function') startListeningTimer();
        }
    } else if (viewName === 'reading') {
        if (!currentReadingTest) {
            loadRandomReadingTest(false).then(() => {
                if (isViewActive('reading') && typeof startReadingTimer === 'function') startReadingTimer();
            });
        } else {
            if (typeof startReadingTimer === 'function') startReadingTimer();
        }
    } else if (viewName === 'writing') {
        if (!currentWritingTask) {
            loadRandomWritingTask(false).then(() => {
                if (isViewActive('writing') && typeof startWritingTimer === 'function') startWritingTimer();
            });
        } else {
            if (typeof startWritingTimer === 'function') startWritingTimer();
        }
    } else if (viewName === 'speaking') {
        if (!currentSpeakingTest) {
            loadRandomSpeakingTest(false).then(() => {
                if (isViewActive('speaking') && typeof startOverallSpeakingTimer === 'function') startOverallSpeakingTimer();
            });
        } else {
            if (typeof startOverallSpeakingTimer === 'function') startOverallSpeakingTimer();
        }
    }
}

// Bootstrap on DOMContentLoaded
document.addEventListener('DOMContentLoaded', async () => {
    if (typeof initTheme === 'function') initTheme();
    if (typeof initAudioEngine === 'function') initAudioEngine();
    if (typeof initSpeechRecognition === 'function') initSpeechRecognition();
    if (typeof initAuth === 'function') await initAuth();
    if (typeof loadSettings === 'function') await loadSettings();
    if (typeof refreshData === 'function') await refreshData();
    if (typeof loadInitialTests === 'function') await loadInitialTests();
    if (typeof loadVocabulary === 'function') await loadVocabulary();
    if (typeof setupPassageHighlighting === 'function') setupPassageHighlighting();
});
