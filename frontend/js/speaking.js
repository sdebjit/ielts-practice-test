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
