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
