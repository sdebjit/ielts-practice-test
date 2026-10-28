// =====================================================================
// IELTS MASTER: DIAGNOSTICS & DASHBOARD CONTROLLER
// =====================================================================

async function loadDiagnostics() {
    try {
        const res = await fetch(`${API_BASE}/api/diagnostics`);
        appDiagnostics = await res.json();
        const ov = appDiagnostics.overview;
        const diag = appDiagnostics.diagnostics;
        const isOverallAssessed = ov.is_assessed && ov.overall_band !== null && ov.overall_band !== undefined;

        // Overall Cards
        const dashBandEl = document.getElementById('dash-overall-band');
        const dashMaxEl = document.getElementById('dash-overall-max');
        const dashTrendEl = document.getElementById('dash-overall-trend-badge');
        const headerBandEl = document.getElementById('header-overall-band');
        const mobBandEl = document.getElementById('mobile-overall-band');

        if (isOverallAssessed) {
            dashBandEl.innerText = ov.overall_band.toFixed(1);
            dashBandEl.className = 'text-4xl font-extrabold tracking-tight text-white';
            if (dashMaxEl) dashMaxEl.classList.remove('hidden');
            if (headerBandEl) headerBandEl.innerText = `Band ${ov.overall_band.toFixed(1)}`;
            if (mobBandEl) mobBandEl.innerText = `Band ${ov.overall_band.toFixed(1)}`;

            // Dynamic Trend Indicator: Improved vs Declined vs Stable
            if (dashTrendEl) {
                if (ov.overall_trend === 'improved') {
                    dashTrendEl.innerText = `↑ +${ov.overall_delta} Improved`;
                    dashTrendEl.className = 'text-[10px] bg-emerald-500/30 text-emerald-100 border border-emerald-400/30 px-2 py-0.5 rounded-full font-bold';
                } else if (ov.overall_trend === 'declined') {
                    dashTrendEl.innerText = `↓ ${ov.overall_delta} Declined`;
                    dashTrendEl.className = 'text-[10px] bg-rose-500/30 text-rose-100 border border-rose-400/30 px-2 py-0.5 rounded-full font-bold';
                } else if (ov.overall_trend === 'stable') {
                    dashTrendEl.innerText = '→ Stable';
                    dashTrendEl.className = 'text-[10px] bg-white/20 text-indigo-100 px-2 py-0.5 rounded-full font-semibold';
                } else {
                    dashTrendEl.innerText = '● Baseline Set';
                    dashTrendEl.className = 'text-[10px] bg-emerald-500/20 text-emerald-200 border border-emerald-400/20 px-2 py-0.5 rounded-full font-semibold';
                }
            }
        } else {
            dashBandEl.innerText = 'Not yet assessed';
            dashBandEl.className = 'text-2xl font-bold tracking-tight text-amber-200/90 italic';
            if (dashMaxEl) dashMaxEl.classList.add('hidden');
            if (headerBandEl) headerBandEl.innerText = 'Not yet assessed';
            if (mobBandEl) mobBandEl.innerText = 'Not assessed';
            if (dashTrendEl) {
                dashTrendEl.innerText = 'Not yet assessed';
                dashTrendEl.className = 'text-[10px] bg-white/20 px-2 py-0.5 rounded-full font-semibold';
            }
        }

        const streakDays = document.getElementById('dash-streak-days');
        if (streakDays) streakDays.innerText = ov.streak_days;
        const sideStreak = document.getElementById('sidebar-streak-days');
        if (sideStreak) sideStreak.innerText = ov.streak_days;
        const totalSess = document.getElementById('dash-total-sessions');
        if (totalSess) totalSess.innerText = ov.total_sessions;
        const totalMins = document.getElementById('dash-total-mins');
        if (totalMins) totalMins.innerText = ov.total_minutes;

        // Gap calculation
        const gapTextEl = document.getElementById('dash-band-gap-text');
        if (gapTextEl) {
            if (!isOverallAssessed) {
                gapTextEl.innerText = `Target: Band ${ov.target_band} • Complete practice tests to establish your baseline`;
            } else if (ov.target_achieved) {
                gapTextEl.innerText = '🎉 Target band score achieved!';
            } else {
                const gap = ov.band_gap;
                const moduleInfo = ov.assessed_count < 4 ? ` (${ov.assessed_count}/4 modules assessed)` : '';
                gapTextEl.innerText = `${gap > 0 ? '+' + gap : gap} band needed to reach target ${ov.target_band}${moduleInfo}`;
            }
        }

        // Progress bar in sidebar and dashboard
        const pct = isOverallAssessed
            ? Math.min(100, Math.max(10, Math.round((ov.overall_band / ov.target_band) * 100)))
            : 0;
        const sideProg = document.getElementById('sidebar-progress-bar');
        if (sideProg) sideProg.style.width = `${pct}%`;
        const dashProg = document.getElementById('dash-target-progress');
        if (dashProg) dashProg.style.width = `${pct}%`;
        const mobProgEl = document.getElementById('mobile-sidebar-progress-bar');
        if (mobProgEl) mobProgEl.style.width = `${pct}%`;

        // Update module details & badges helper
        const updateModuleUI = (modKey, badgeId, mobBadgeId, diagBandId, diagTrendId, diagWeakId, diagAdviceId, defaultWeakText, adviceText) => {
            const modMeta = ov.module_details ? ov.module_details[modKey] : null;
            const score = ov.module_scores[modKey];
            const isAssessed = modMeta ? modMeta.status === 'assessed' : (score !== null && score !== undefined);

            const badgeEl = document.getElementById(badgeId);
            const mobBadgeEl = document.getElementById(mobBadgeId);
            const diagBandEl = document.getElementById(diagBandId);
            const diagTrendEl = document.getElementById(diagTrendId);
            const diagWeakEl = document.getElementById(diagWeakId);
            const diagAdviceEl = document.getElementById(diagAdviceId);

            if (isAssessed) {
                const trendIcon = modMeta && modMeta.trend === 'improved' ? ' ↑' : (modMeta && modMeta.trend === 'declined' ? ' ↓' : '');
                const scoreText = `Band ${score.toFixed(1)}${trendIcon}`;

                if (badgeEl) {
                    badgeEl.innerText = scoreText;
                    badgeEl.className = 'px-2 py-0.5 text-xs font-semibold rounded-full bg-slate-800 text-brand-300 font-mono border border-slate-700';
                }
                if (mobBadgeEl) {
                    mobBadgeEl.innerText = scoreText;
                    mobBadgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-brand-50 text-brand-700 font-mono border border-brand-200';
                }
                if (diagBandEl) {
                    diagBandEl.innerText = `Band ${score.toFixed(1)}`;
                    diagBandEl.className = 'font-bold text-xs px-2 py-0.5 rounded-full bg-brand-100 text-brand-800';
                }
                if (diagTrendEl && modMeta) {
                    diagTrendEl.classList.remove('hidden');
                    if (modMeta.trend === 'improved') {
                        diagTrendEl.innerText = `↑ +${modMeta.delta} Improved`;
                        diagTrendEl.className = 'text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800';
                    } else if (modMeta.trend === 'declined') {
                        diagTrendEl.innerText = `↓ ${modMeta.delta} Declined`;
                        diagTrendEl.className = 'text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-100 text-rose-800';
                    } else if (modMeta.trend === 'stable') {
                        diagTrendEl.innerText = '→ Stable';
                        diagTrendEl.className = 'text-[10px] font-semibold px-1.5 py-0.5 rounded bg-slate-200 text-slate-700';
                    } else {
                        diagTrendEl.innerText = '● Baseline Set';
                        diagTrendEl.className = 'text-[10px] font-semibold px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-700';
                    }
                }
                if (diagWeakEl) {
                    diagWeakEl.innerText = defaultWeakText;
                    diagWeakEl.className = 'text-xs font-bold text-rose-600 mb-2';
                }
            } else {
                if (badgeEl) {
                    badgeEl.innerText = 'Not assessed';
                    badgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-slate-100 text-slate-500';
                }
                if (mobBadgeEl) {
                    mobBadgeEl.innerText = 'Not assessed';
                    mobBadgeEl.className = 'px-2 py-0.5 text-[10px] font-semibold rounded-full bg-slate-100 text-slate-500';
                }
                if (diagBandEl) {
                    diagBandEl.innerText = 'Not assessed';
                    diagBandEl.className = 'font-bold text-xs bg-slate-200/70 text-slate-600 px-2 py-0.5 rounded-full';
                }
                if (diagTrendEl) diagTrendEl.classList.add('hidden');
                if (diagWeakEl) {
                    diagWeakEl.innerText = 'Not yet assessed';
                    diagWeakEl.className = 'text-xs font-semibold text-slate-500 mb-2';
                }
            }

            if (diagAdviceEl) diagAdviceEl.innerText = adviceText;
        };

        // Update each module
        updateModuleUI('listening', 'badge-listening-band', 'mobile-badge-listening-band', 'dash-diag-l-band', 'dash-diag-l-trend', 'dash-diag-l-weakest', 'dash-diag-l-advice', diag.listening.weakest_question_type || 'Multiple Choice', diag.listening.key_advice || '');
        updateModuleUI('reading', 'badge-reading-band', 'mobile-badge-reading-band', 'dash-diag-r-band', 'dash-diag-r-trend', 'dash-diag-r-weakest', 'dash-diag-r-advice', diag.reading.weakest_question_type || 'True / False / Not Given', diag.reading.key_advice || '');
        updateModuleUI('writing', 'badge-writing-band', 'mobile-badge-writing-band', 'dash-diag-w-band', 'dash-diag-w-trend', 'dash-diag-w-bottleneck', 'dash-diag-w-advice', diag.writing.bottleneck_criterion || 'Grammar Range & Accuracy', diag.writing.key_advice || '');
        updateModuleUI('speaking', 'badge-speaking-band', 'mobile-badge-speaking-band', 'dash-diag-s-band', 'dash-diag-s-trend', 'dash-diag-s-bottleneck', 'dash-diag-s-advice', diag.speaking.bottleneck_criterion || 'Fluency & Coherence', diag.speaking.key_advice || '');

        // Render Action Priorities
        renderPriorities(appDiagnostics.priorities);

        // Render Charts
        renderCharts(ov.module_scores, ov.target_band, appDiagnostics.chart_data);

    } catch (err) {
        console.error('Failed loading diagnostics:', err);
    }
}

function renderPriorities(priorities) {
    const container = document.getElementById('dash-priorities-list');
    if (!container) return;
    if (!priorities || priorities.length === 0) {
        container.innerHTML = '<div class="text-xs text-slate-400">Complete practice tests across modules to generate your custom AI improvement roadmap.</div>';
        return;
    }

    container.innerHTML = priorities.map((p, idx) => `
        <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/70 hover:bg-white hover:border-brand-200 transition-all">
            <div class="flex items-start gap-3">
                <span class="w-6 h-6 rounded-full ${p.urgency === 'High' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'} flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                    ${idx + 1}
                </span>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs font-bold text-slate-800">${p.title}</span>
                        <span class="text-[10px] font-semibold px-2 py-0.5 rounded ${p.status === 'not_assessed' ? 'bg-indigo-50 text-indigo-700 border border-indigo-200' : (p.urgency === 'High' ? 'bg-rose-50 text-rose-600' : 'bg-amber-50 text-amber-600')}">
                            ${p.status === 'not_assessed' ? 'Baseline Pending' : p.urgency + ' Priority'}
                        </span>
                    </div>
                    <p class="text-[11px] text-slate-500 mt-0.5 leading-relaxed">${p.description}</p>
                </div>
            </div>
            <button onclick="switchView('${p.target_route}')" class="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-brand-50 hover:text-brand-700 hover:border-brand-200 text-xs font-semibold shrink-0 transition-colors">
                ${p.action_label} →
            </button>
        </div>
    `).join('');
}

function renderCharts(moduleScores, targetBand, chartData) {
    // 1. Radar Chart: 4-Segment Competency
    const radarEl = document.getElementById('radarChart');
    if (radarEl) {
        const radarCtx = radarEl.getContext('2d');
        if (radarChartInstance) radarChartInstance.destroy();

        const lScore = moduleScores.listening || 0;
        const rScore = moduleScores.reading || 0;
        const wScore = moduleScores.writing || 0;
        const sScore = moduleScores.speaking || 0;
        const anyAssessed = lScore > 0 || rScore > 0 || wScore > 0 || sScore > 0;

        radarChartInstance = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: ['Listening', 'Reading', 'Writing', 'Speaking'],
                datasets: [
                    {
                        label: anyAssessed ? 'Current Assessed Band' : 'Current Band (Not yet assessed)',
                        data: [lScore, rScore, wScore, sScore],
                        backgroundColor: anyAssessed ? 'rgba(99, 102, 241, 0.2)' : 'rgba(148, 163, 184, 0.1)',
                        borderColor: anyAssessed ? '#4f46e5' : '#94a3b8',
                        pointBackgroundColor: anyAssessed ? '#4f46e5' : '#94a3b8',
                        borderDash: anyAssessed ? [] : [4, 4],
                        borderWidth: 2
                    },
                    {
                        label: 'Target Goal',
                        data: [targetBand, targetBand, targetBand, targetBand],
                        backgroundColor: 'rgba(16, 185, 129, 0.05)',
                        borderColor: '#10b981',
                        borderDash: [4, 4],
                        pointBackgroundColor: '#10b981',
                        borderWidth: 1.5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        min: 0.0,
                        max: 9.0,
                        ticks: { stepSize: 1.5, font: { size: 10 } }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                if (context.datasetIndex === 0) {
                                    const val = context.raw;
                                    return val > 0 ? `Current Band: ${val.toFixed(1)}` : 'Current Band: Not yet assessed';
                                }
                                return `Target Goal: Band ${context.raw}`;
                            }
                        }
                    },
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
                }
            }
        });
    }

    // 2. Progression Timeline Line Chart
    const trendEl = document.getElementById('trendChart');
    if (trendEl) {
        const trendCtx = trendEl.getContext('2d');
        if (trendChartInstance) trendChartInstance.destroy();

        const hasAttempts = chartData && chartData.dates && chartData.dates.length > 0;
        const dates = hasAttempts ? chartData.dates : ['Baseline'];
        const listeningData = hasAttempts ? chartData.listening : [null];
        const readingData = hasAttempts ? chartData.reading : [null];
        const writingData = hasAttempts ? chartData.writing : [null];
        const speakingData = hasAttempts ? chartData.speaking : [null];

        trendChartInstance = new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    { label: 'Listening', data: listeningData, borderColor: '#6366f1', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Reading', data: readingData, borderColor: '#0ea5e9', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Writing', data: writingData, borderColor: '#f59e0b', tension: 0.3, fill: false, spanGaps: true },
                    { label: 'Speaking', data: speakingData, borderColor: '#10b981', tension: 0.3, fill: false, spanGaps: true }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { min: 4.0, max: 9.0, ticks: { stepSize: 0.5, font: { size: 10 } } },
                    x: { ticks: { font: { size: 10 } } }
                },
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const val = context.raw;
                                return val !== null && val !== undefined ? `${context.dataset.label}: Band ${val.toFixed(1)}` : `${context.dataset.label}: Not yet assessed`;
                            }
                        }
                    }
                }
            }
        });
    }
}

async function confirmResetAttempts() {
    if (!confirm('Are you sure you want to reset all practice test attempts for this candidate account?\n\nYour scores across all 4 segments will return to "Not yet assessed", allowing you to start fresh.')) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/attempts/reset`, { method: 'POST' });
        const data = await res.json();
        alert('✅ ' + (data.message || 'Practice attempts have been reset to Not yet assessed.'));
        if (typeof refreshData === 'function') await refreshData();
        if (typeof switchView === 'function') switchView('dashboard');
    } catch (err) {
        alert('Error resetting attempts: ' + err.message);
    }
}

async function loadRecentAttempts() {
    try {
        const res = await fetch(`${API_BASE}/api/attempts?limit=10`);
        const attempts = await res.json();
        const tbody = document.getElementById('dash-attempts-tbody');
        if (!tbody) return;

        if (!attempts || attempts.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="p-5 text-center text-slate-400">No practice attempts recorded yet. Choose a module above to get started!</td></tr>`;
            return;
        }

        const moduleColors = {
            listening: 'bg-indigo-50 text-indigo-700',
            reading: 'bg-sky-50 text-sky-700',
            writing: 'bg-amber-50 text-amber-700',
            speaking: 'bg-emerald-50 text-emerald-700'
        };

        tbody.innerHTML = attempts.map(att => {
            const dateStr = att.created_at ? att.created_at.substring(0, 10) : 'Today';
            const mod = att.module.toLowerCase();
            const colorClass = moduleColors[mod] || 'bg-slate-100 text-slate-700';

            // Key metric summary
            let metricText = '';
            if (mod === 'listening' || mod === 'reading') {
                const raw = att.criterion_scores?.raw_score ?? 0;
                const tot = att.criterion_scores?.total ?? 10;
                metricText = `Raw Score: ${raw}/${tot}`;
            } else if (mod === 'writing') {
                const ta = att.criterion_scores?.task_achievement?.band ?? 6.0;
                const gr = att.criterion_scores?.grammatical_range_accuracy?.band ?? 6.0;
                metricText = `TA: ${ta} | GRA: ${gr}`;
            } else if (mod === 'speaking') {
                const fc = att.criterion_scores?.fluency_coherence?.band ?? 6.0;
                metricText = `Fluency: ${fc} | Lex: ${att.criterion_scores?.lexical_resource?.band ?? 6.5}`;
            }

            return `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="p-3.5 pl-5 text-slate-500">${dateStr}</td>
                    <td class="p-3.5">
                        <span class="px-2 py-0.5 rounded-full font-semibold uppercase text-[10px] ${colorClass}">
                            ${att.module}
                        </span>
                    </td>
                    <td class="p-3.5 font-medium text-slate-800 max-w-[200px] truncate">${att.test_title || att.test_id}</td>
                    <td class="p-3.5 font-bold text-slate-900">
                        <span class="px-2 py-0.5 rounded bg-slate-100">Band ${att.band_score.toFixed(1)}</span>
                    </td>
                    <td class="p-3.5 text-slate-500 font-mono text-[11px]">${metricText}</td>
                    <td class="p-3.5 pr-5 text-right">
                        <button onclick='viewAttemptDetails(${JSON.stringify(att).replace(/'/g, "&#39;")})' class="text-brand-600 hover:text-brand-800 font-semibold text-xs">
                            Review AI Critique →
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (err) {
        console.error('Failed loading attempts:', err);
    }
}

function viewAttemptDetails(att) {
    if (att.module === 'writing') {
        if (typeof renderWritingReport === 'function') renderWritingReport(att.ai_feedback);
        if (typeof switchView === 'function') switchView('writing');
        const rEl = document.getElementById('writing-report-container');
        if (rEl) rEl.scrollIntoView({ behavior: 'smooth' });
    } else if (att.module === 'speaking') {
        if (typeof renderSpeakingReport === 'function') renderSpeakingReport(att.ai_feedback);
        if (typeof switchView === 'function') switchView('speaking');
        const rEl = document.getElementById('speaking-report-container');
        if (rEl) rEl.scrollIntoView({ behavior: 'smooth' });
    } else {
        alert(`Attempt Details for ${att.module.toUpperCase()}:\nBand Score: ${att.band_score}\n${JSON.stringify(att.criterion_scores, null, 2)}`);
    }
}
