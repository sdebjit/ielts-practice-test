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
