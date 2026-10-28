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
