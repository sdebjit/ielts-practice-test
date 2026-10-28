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
