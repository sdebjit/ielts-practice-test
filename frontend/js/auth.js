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
