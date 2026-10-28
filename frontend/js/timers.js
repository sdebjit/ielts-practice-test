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
