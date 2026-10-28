/**
 * IELTS Master - Main Application Orchestrator
 * Coordinates view switching, timer lifecycle between tabs, and bootstrap initialization.
 */

function switchView(viewName) {
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
