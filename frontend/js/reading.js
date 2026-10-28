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
