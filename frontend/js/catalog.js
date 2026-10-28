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
        const res = await fetch(`${API_BASE}/api/tests/random?module=reading&type=${encodeURIComponent(examType)}`);
        const test = await res.json();
        if (test && test.id) {
            await loadReadingTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('reading');
            return;
        }
    } catch (err) {
        console.warn('API random reading fetch fallback:', err);
    }
    if (availableTests.reading && availableTests.reading.length > 0) {
        const randomItem = availableTests.reading[Math.floor(Math.random() * availableTests.reading.length)];
        await loadReadingTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('reading');
    }
}

async function loadRandomListeningTest(shouldSwitchView = true) {
    try {
        const res = await fetch(`${API_BASE}/api/tests/random?module=listening`);
        const test = await res.json();
        if (test && test.id) {
            await loadListeningTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('listening');
            return;
        }
    } catch (err) {
        console.warn('API random listening fetch fallback:', err);
    }
    if (availableTests.listening && availableTests.listening.length > 0) {
        const randomItem = availableTests.listening[Math.floor(Math.random() * availableTests.listening.length)];
        await loadListeningTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('listening');
    }
}

async function loadRandomWritingTask(shouldSwitchView = true) {
    try {
        const examType = appSettings.exam_type || currentUser?.exam_type || 'Academic';
        const res = await fetch(`${API_BASE}/api/tests/random?module=writing&type=${encodeURIComponent(examType)}`);
        const test = await res.json();
        if (test && test.id) {
            await loadWritingTask(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('writing');
            return;
        }
    } catch (err) {
        console.warn('API random writing fetch fallback:', err);
    }
    if (availableTests.writing && availableTests.writing.length > 0) {
        const randomItem = availableTests.writing[Math.floor(Math.random() * availableTests.writing.length)];
        await loadWritingTask(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('writing');
    }
}

async function loadRandomSpeakingTest(shouldSwitchView = true) {
    try {
        const res = await fetch(`${API_BASE}/api/tests/random?module=speaking`);
        const test = await res.json();
        if (test && test.id) {
            await loadSpeakingTest(test.id);
            if (shouldSwitchView && typeof switchView === 'function') switchView('speaking');
            return;
        }
    } catch (err) {
        console.warn('API random speaking fetch fallback:', err);
    }
    if (availableTests.speaking && availableTests.speaking.length > 0) {
        const randomItem = availableTests.speaking[Math.floor(Math.random() * availableTests.speaking.length)];
        await loadSpeakingTest(randomItem.id);
        if (shouldSwitchView && typeof switchView === 'function') switchView('speaking');
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
