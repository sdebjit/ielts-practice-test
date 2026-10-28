// =====================================================================
// IELTS MASTER: HIGH-DEFINITION AUDIO ENGINE (GEMINI NEURAL AI + SYSTEM NATURAL VOICES)
// =====================================================================

function initAudioEngine() {
    const savedEngine = localStorage.getItem('ielts_audio_engine');
    if (savedEngine) currentAudioEngine = savedEngine;

    const savedPersona = localStorage.getItem('ielts_gemini_persona');
    if (savedPersona) currentGeminiPersona = savedPersona;

    const savedBrowserVoice = localStorage.getItem('ielts_browser_voice');
    if (savedBrowserVoice) selectedBrowserVoiceURI = savedBrowserVoice;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => {
            loadAndRankVoices();
        };
        loadAndRankVoices();
        setTimeout(loadAndRankVoices, 100);
        setTimeout(loadAndRankVoices, 300);
        setTimeout(loadAndRankVoices, 800);
        setTimeout(loadAndRankVoices, 1500);
    }
    syncVoiceUI();
}

function pcm16ToWavBlob(base64Pcm, sampleRate = 24000) {
    const binary = atob(base64Pcm);
    const pcmLen = binary.length;
    const buffer = new ArrayBuffer(44 + pcmLen);
    const view = new DataView(buffer);

    const writeStr = (offset, str) => {
        for (let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
    };

    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + pcmLen, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // Mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // Byte rate (sampleRate * 1 channel * 2 bytes/sample)
    view.setUint16(32, 2, true);  // Block align
    view.setUint16(34, 16, true); // 16 bits
    writeStr(36, 'data');
    view.setUint32(40, pcmLen, true);

    const pcmView = new Uint8Array(buffer, 44);
    for (let i = 0; i < pcmLen; i++) {
        pcmView[i] = binary.charCodeAt(i);
    }
    return new Blob([buffer], { type: 'audio/wav' });
}

function loadAndRankVoices() {
    if (!('speechSynthesis' in window)) return;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return;

    const scored = voices.map(v => {
        let score = 0;
        const name = v.name.toLowerCase();
        const lang = v.lang.toLowerCase();

        // Demote known robotic/metallic synthesizers heavily
        const robotic = [
            'bad news', 'bahh', 'bells', 'boing', 'bubbles', 'cellos',
            'good news', 'jester', 'junior', 'organ', 'superstar',
            'trinoids', 'whisper', 'zarvox', 'compact', 'wobble', 'deranged', 'hysterical'
        ];
        if (robotic.some(r => name.includes(r))) score -= 2000;

        // Neural, Online, Enhanced, Siri, Google (ultra-realistic natural voices)
        if (name.includes('natural') || name.includes('online')) score += 800;
        if (name.includes('google')) score += 700;
        if (name.includes('enhanced') || name.includes('premium')) score += 600;
        if (name.includes('siri') || name.includes('oliver') || name.includes('stephanie') || name.includes('martha') || name.includes('arthur') || name.includes('serena') || name.includes('kate') || name.includes('daniel')) score += 500;

        // Preferred IELTS accents
        if (lang.includes('en-gb') || lang.includes('en_gb')) score += 350;
        else if (lang.includes('en-au') || lang.includes('en_au')) score += 250;
        else if (lang.includes('en-ca') || lang.includes('en-nz') || lang.includes('en-ie')) score += 200;
        else if (lang.includes('en-us') || lang.includes('en_us')) score += 150;
        else if (lang.startsWith('en')) score += 50;
        else score -= 1000;

        return { voice: v, score, name: v.name, lang: v.lang, voiceURI: v.voiceURI };
    });

    scored.sort((a, b) => b.score - a.score);
    availableBrowserVoices = scored.filter(s => s.score > -500);
    bestNaturalVoice = availableBrowserVoices.length > 0 ? availableBrowserVoices[0].voice : null;

    populateAllVoiceSelectors();
}

function populateAllVoiceSelectors(force = false) {
    if (!('speechSynthesis' in window)) return;
    const listeningSel = document.getElementById('select-listening-voice');
    const speakingSel = document.getElementById('select-speaking-persona');
    const settingsBrowserSel = document.getElementById('set-browser-voice');

    if (!force && voicesPopulatedAlready && availableBrowserVoices.length > 0) {
        return;
    }

    // 1. Gemini AI Studio Personas
    const geminiGroup = `
    <optgroup label="🌟 Gemini AI Studio Neural Personas">
        <option value="gemini:Puck">👨‍🏫 Puck (Natural British - Cambridge Standard)</option>
        <option value="gemini:Aoede">👩‍🏫 Aoede (Expressive British / Academic)</option>
        <option value="gemini:Charon">👨‍💼 Charon (Senior Cambridge Examiner - Deep)</option>
        <option value="gemini:Kore">👩‍💼 Kore (Calm & Clear Professional)</option>
        <option value="gemini:Fenrir">🎙️ Fenrir (Authoritative Deep Male)</option>
    </optgroup>
    `;

    // 2. High-Def System / Browser Voices (Grouped by Region/Accent)
    const gbOptions = [];
    const auOptions = [];
    const usOptions = [];
    const otherOptions = [];

    availableBrowserVoices.forEach(item => {
        const lang = (item.lang || '').toLowerCase();
        const label = `${item.name} (${item.lang})`;
        const val = `browser:${item.voiceURI || item.name}`;

        if (lang.includes('en-gb') || lang.includes('en_gb')) {
            gbOptions.push(`<option value="${val}">🇬🇧 ${label}</option>`);
        } else if (lang.includes('en-au') || lang.includes('en_au') || lang.includes('en-nz')) {
            auOptions.push(`<option value="${val}">🇦🇺 ${label}</option>`);
        } else if (lang.includes('en-us') || lang.includes('en_us') || lang.includes('en-ca')) {
            usOptions.push(`<option value="${val}">🇺🇸 ${label}</option>`);
        } else {
            otherOptions.push(`<option value="${val}">🎙️ ${label}</option>`);
        }
    });

    let systemGroup = '';
    if (gbOptions.length > 0) {
        systemGroup += `<optgroup label="🇬🇧 British System Voices (Cambridge Standard)">${gbOptions.join('')}</optgroup>`;
    }
    if (auOptions.length > 0) {
        systemGroup += `<optgroup label="🇦🇺 Australian / Kiwi Voices">${auOptions.join('')}</optgroup>`;
    }
    if (usOptions.length > 0) {
        systemGroup += `<optgroup label="🇺🇸 North American Voices">${usOptions.join('')}</optgroup>`;
    }
    if (otherOptions.length > 0) {
        systemGroup += `<optgroup label="🎙️ Other Natural System Voices">${otherOptions.join('')}</optgroup>`;
    }

    const defaultAuto = `<optgroup label="⚡ Quick Preset"><option value="browser:auto">⚡ Auto-Select Best Cambridge Voice</option></optgroup>`;
    const fullHtml = defaultAuto + geminiGroup + systemGroup;

    if (listeningSel) listeningSel.innerHTML = fullHtml;
    if (speakingSel) speakingSel.innerHTML = fullHtml;

    if (settingsBrowserSel) {
        let bHtml = '<option value="">Auto-Detect Best Natural Voice (Recommended)</option>';
        availableBrowserVoices.forEach(item => {
            bHtml += `<option value="${item.voiceURI || item.name}">${item.name} (${item.lang}) - ${item.score >= 500 ? '🌟 Ultra-Realistic' : 'Natural'}</option>`;
        });
        settingsBrowserSel.innerHTML = bHtml;
        if (selectedBrowserVoiceURI) settingsBrowserSel.value = selectedBrowserVoiceURI;
    }

    if (availableBrowserVoices.length > 0) {
        voicesPopulatedAlready = true;
    }
    syncVoiceUI();
}

function populateBrowserVoiceDropdown() {
    populateAllVoiceSelectors(true);
}

function resolveSpeechParameters(engine, persona, browserVoiceURI) {
    // 1. If explicit browser voice is chosen
    if (engine === 'browser' && browserVoiceURI && browserVoiceURI !== 'auto') {
        const found = availableBrowserVoices.find(v => v.voiceURI === browserVoiceURI || v.name === browserVoiceURI);
        if (found) {
            return {
                voice: found.voice,
                pitch: 1.0,
                rate: 1.0,
                name: found.name,
                accent: found.lang
            };
        }
    }

    // 2. Persona mapping to distinct acoustic profiles & voices
    const femaleKeywords = ['female', 'serena', 'stephanie', 'karen', 'samantha', 'martha', 'victoria', 'moira', 'fiona', 'kate', 'susan', 'zira', 'flo', 'sandy', 'shelley', 'grandma', 'tara', 'tessa', 'kathy', 'alice'];
    const maleKeywords = ['male', 'daniel', 'oliver', 'arthur', 'george', 'alex', 'david', 'russell', 'lee', 'rishi', 'eddy', 'reed', 'rocko', 'grandpa', 'fred', 'albert', 'ralph', 'tom'];

    const femaleVoices = availableBrowserVoices.filter(v => femaleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
    const maleVoices = availableBrowserVoices.filter(v => maleKeywords.some(kw => v.name.toLowerCase().includes(kw)));
    const pool = availableBrowserVoices.length > 0 ? availableBrowserVoices : [];

    const getVoice = (preferredList, fallbackIdx = 0) => {
        if (preferredList && preferredList.length > 0) return preferredList[0].voice;
        if (pool.length > fallbackIdx) return pool[fallbackIdx].voice;
        return bestNaturalVoice;
    };

    const getVoice2 = (preferredList, fallbackIdx = 1) => {
        if (preferredList && preferredList.length > 1) return preferredList[1].voice;
        if (preferredList && preferredList.length > 0) return preferredList[0].voice;
        if (pool.length > fallbackIdx) return pool[fallbackIdx].voice;
        return bestNaturalVoice;
    };

    if (persona === 'Aoede') {
        // Expressive British Female Academic
        const voice = getVoice(femaleVoices, 1);
        return {
            voice,
            pitch: 1.25, // Noticeably brighter, expressive female academic pitch
            rate: 1.02,
            name: voice ? `${voice.name} (Aoede Academic Female)` : 'Aoede Academic Female'
        };
    } else if (persona === 'Charon') {
        // Senior Cambridge Examiner (Deep, authoritative, deliberate cadence)
        const voice = getVoice(maleVoices, 0);
        return {
            voice,
            pitch: 0.75, // Noticeably deeper, authoritative pitch
            rate: 0.88,  // Deliberate examiner pacing
            name: voice ? `${voice.name} (Charon Senior Examiner)` : 'Charon Senior Examiner'
        };
    } else if (persona === 'Kore') {
        // Calm & Professional Female
        const voice = getVoice2(femaleVoices, 2);
        return {
            voice,
            pitch: 1.08,
            rate: 0.95,
            name: voice ? `${voice.name} (Kore Calm Professional)` : 'Kore Calm Professional'
        };
    } else if (persona === 'Fenrir') {
        // Deep Resonant Male
        const voice = getVoice2(maleVoices, 1);
        return {
            voice,
            pitch: 0.65, // Deep resonant pitch
            rate: 0.90,
            name: voice ? `${voice.name} (Fenrir Resonant Male)` : 'Fenrir Resonant Male'
        };
    } else {
        // Puck: Natural British Cambridge Male Standard
        const voice = getVoice(maleVoices, 0);
        return {
            voice,
            pitch: 0.98, // Natural British male pitch
            rate: 1.00,
            name: voice ? `${voice.name} (Puck British Examiner)` : 'Puck British Examiner'
        };
    }
}

async function synthesizeGeminiAudio(text, persona = null) {
    persona = persona || currentGeminiPersona || 'Puck';
    const cleanText = text.trim();
    if (!cleanText) return null;

    const cacheKey = `gemini_${persona}_${cleanText}`;
    if (audioBlobCache.has(cacheKey)) {
        return audioBlobCache.get(cacheKey);
    }

    const clientKey = document.getElementById('set-gemini-key')?.value.trim() || appSettings.gemini_api_key || localStorage.getItem('gemini_api_key');

    // 1. Direct Browser Fetch (Fastest, zero Python proxy latency) if client has entered an API key
    if (clientKey) {
        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${clientKey}`;
            const payload = {
                contents: [{
                    role: 'user',
                    parts: [{
                        text: `Read the following IELTS text aloud with authentic British Cambridge IELTS examiner cadence, clear human breathing, natural pauses, and warm articulation:\n\n"${cleanText}"`
                    }]
                }],
                generationConfig: {
                    responseModalities: ["AUDIO"],
                    speechConfig: {
                        voiceConfig: {
                            prebuiltVoiceConfig: {
                                voiceName: persona
                            }
                        }
                    }
                }
            };

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000);
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (res.ok) {
                const data = await res.json();
                const part = data.candidates?.[0]?.content?.parts?.find(p => p.inlineData && p.inlineData.data);
                if (part) {
                    const mimeType = part.inlineData.mimeType || 'audio/pcm;rate=24000';
                    const base64Data = part.inlineData.data;

                    let blobUrl;
                    if (mimeType.startsWith('audio/pcm') || mimeType.includes('rate=')) {
                        let rate = 24000;
                        const m = mimeType.match(/rate=(\d+)/);
                        if (m) rate = parseInt(m[1]);
                        const blob = pcm16ToWavBlob(base64Data, rate);
                        blobUrl = URL.createObjectURL(blob);
                    } else {
                        const binary = atob(base64Data);
                        const bytes = new Uint8Array(binary.length);
                        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                        const blob = new Blob([bytes], { type: mimeType });
                        blobUrl = URL.createObjectURL(blob);
                    }

                    audioBlobCache.set(cacheKey, blobUrl);
                    return blobUrl;
                }
            }
        } catch (err) {
            console.warn('Direct browser Gemini audio synthesis skipped:', err.message);
        }
    }

    // 2. Fallback: Backend TTS endpoint (uses admin / system key)
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        const backendRes = await fetch(`${API_BASE}/api/tts`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ text: cleanText, voice: persona, api_key: clientKey || '' })
        });
        if (backendRes.ok) {
            const ttsData = await backendRes.json();
            if (ttsData.success && ttsData.audio_base64) {
                const mime = ttsData.mime_type || 'audio/wav';
                let blobUrl;
                if (mime.startsWith('audio/pcm') || mime.includes('rate=')) {
                    let rate = 24000;
                    const m = mime.match(/rate=(\d+)/);
                    if (m) rate = parseInt(m[1]);
                    const blob = pcm16ToWavBlob(ttsData.audio_base64, rate);
                    blobUrl = URL.createObjectURL(blob);
                } else {
                    const binary = atob(ttsData.audio_base64);
                    const bytes = new Uint8Array(binary.length);
                    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                    const blob = new Blob([bytes], { type: mime });
                    blobUrl = URL.createObjectURL(blob);
                }
                audioBlobCache.set(cacheKey, blobUrl);
                return blobUrl;
            }
        }
    } catch (bErr) {
        console.warn('Backend TTS endpoint skipped:', bErr.message);
    }

    return null;
}

function stopAnyActiveAudio() {
    if (currentAudioElement) {
        try {
            currentAudioElement.pause();
            currentAudioElement.currentTime = 0;
        } catch (e) {}
        currentAudioElement = null;
    }
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    if (listeningTimeoutId) {
        clearTimeout(listeningTimeoutId);
        listeningTimeoutId = null;
    }
    listeningPassagePlaying = false;
    isAudioPlaying = false;
    updateAudioPlayerUI();
}

async function playExaminerVoice(text, btnElement = null) {
    if (!text) return;
    stopAnyActiveAudio();

    let origHtml = null;
    if (btnElement) {
        origHtml = btnElement.innerHTML;
        btnElement.innerHTML = '<span>🔊 Speaking...</span>';
    }

    const resetButton = () => {
        if (btnElement && origHtml) {
            btnElement.innerHTML = origHtml;
        }
    };

    if (currentAudioEngine === 'gemini') {
        const audioUrl = await synthesizeGeminiAudio(text, currentGeminiPersona);
        if (audioUrl) {
            const audio = new Audio(audioUrl);
            currentAudioElement = audio;
            audio.onended = () => {
                currentAudioElement = null;
                resetButton();
            };
            audio.onerror = () => {
                currentAudioElement = null;
                playBrowserExaminerVoice(text, resetButton);
            };
            try {
                await audio.play();
                return;
            } catch (err) {
                console.warn('Audio play error, falling back to browser voice:', err);
            }
        }
    }

    playBrowserExaminerVoice(text, resetButton);
}

function playBrowserExaminerVoice(text, onComplete = null) {
    if (!('speechSynthesis' in window)) {
        if (onComplete) onComplete();
        return;
    }

    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);

    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);
    if (params.voice) utt.voice = params.voice;
    utt.pitch = params.pitch;
    utt.rate = (audioSpeechRate || 1.0) * params.rate;

    utt.onend = () => {
        if (onComplete) onComplete();
    };
    utt.onerror = () => {
        if (onComplete) onComplete();
    };

    window.speechSynthesis.speak(utt);
}

function toggleAudioPlayback() {
    if (listeningPassagePlaying || isAudioPlaying) {
        stopAnyActiveAudio();
        return;
    }

    const scriptBox = document.getElementById('listening-script-box');
    const script = scriptBox ? scriptBox.innerText.trim() : '';
    if (!script) {
        alert('Audio transcript is empty for this test.');
        return;
    }

    isAudioPlaying = true;
    listeningPassagePlaying = true;
    updateAudioPlayerUI();

    // Split text into natural spoken sentences
    const sentences = script
        .replace(/Section \d+:?/gi, '')
        .split(/(?<=[.!?])\s+/)
        .map(s => s.trim())
        .filter(s => s.length > 2);

    listeningSentencesQueue = sentences;
    listeningSentenceIndex = 0;
    playNextListeningSentence();
}

async function playNextListeningSentence() {
    if (!listeningPassagePlaying || listeningSentenceIndex >= listeningSentencesQueue.length) {
        stopAnyActiveAudio();
        return;
    }

    const sentence = listeningSentencesQueue[listeningSentenceIndex];
    listeningSentenceIndex++;

    const statusText = document.getElementById('audio-status-text');
    if (statusText) {
        statusText.innerText = `Examiner Audio Playing (${listeningSentenceIndex}/${listeningSentencesQueue.length})...`;
    }

    if (currentAudioEngine === 'gemini') {
        try {
            const audioUrl = await synthesizeGeminiAudio(sentence, currentGeminiPersona);
            if (audioUrl && listeningPassagePlaying) {
                const audio = new Audio(audioUrl);
                currentAudioElement = audio;
                audio.playbackRate = audioSpeechRate || 1.0;
                audio.onended = () => {
                    currentAudioElement = null;
                    if (listeningPassagePlaying) {
                        listeningTimeoutId = setTimeout(playNextListeningSentence, 200);
                    }
                };
                audio.onerror = () => {
                    currentAudioElement = null;
                    speakSentenceWithBrowser(sentence);
                };
                await audio.play();
                return;
            }
        } catch (err) {
            console.warn('Gemini listening audio error, falling back to calibrated browser voice:', err);
        }
    }

    // High-definition browser synthesis with calibrated persona voice & pitch
    speakSentenceWithBrowser(sentence);
}

function speakSentenceWithBrowser(sentence) {
    if (!('speechSynthesis' in window)) {
        stopAnyActiveAudio();
        return;
    }

    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(sentence);
    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);

    if (params.voice) utt.voice = params.voice;
    utt.pitch = params.pitch;
    utt.rate = (audioSpeechRate || 1.0) * params.rate;

    utt.onend = () => {
        if (listeningPassagePlaying) {
            // Natural human inter-sentence breath pause (220ms)
            listeningTimeoutId = setTimeout(playNextListeningSentence, 220);
        }
    };

    utt.onerror = () => {
        if (listeningPassagePlaying) {
            listeningTimeoutId = setTimeout(playNextListeningSentence, 150);
        }
    };

    window.speechSynthesis.speak(utt);
}

function setAudioSpeed(rate) {
    audioSpeechRate = rate;
    document.querySelectorAll('.audio-speed-btn').forEach(btn => {
        btn.className = btn.innerText.includes(rate) 
            ? 'audio-speed-btn px-2 py-1 text-xs font-medium rounded bg-brand-600 text-white'
            : 'audio-speed-btn px-2 py-1 text-xs font-medium rounded bg-slate-800 text-slate-300 hover:bg-slate-700';
    });
}

function updateAudioPlayerUI() {
    const playIcon = document.getElementById('audio-icon-play');
    const pauseIcon = document.getElementById('audio-icon-pause');
    const statusText = document.getElementById('audio-status-text');
    const waveforms = document.getElementById('audio-waveforms');

    if (isAudioPlaying || listeningPassagePlaying) {
        if (playIcon) playIcon.classList.add('hidden');
        if (pauseIcon) pauseIcon.classList.remove('hidden');
        if (statusText) statusText.innerText = 'Examiner Audio Playing...';
        if (waveforms) waveforms.classList.remove('opacity-20');
    } else {
        if (playIcon) playIcon.classList.remove('hidden');
        if (pauseIcon) pauseIcon.classList.add('hidden');
        if (statusText) statusText.innerText = 'Audio Paused / Ready';
        if (waveforms) waveforms.classList.add('opacity-20');
    }
}

function toggleAudioScript() {
    const box = document.getElementById('listening-script-box');
    const btn = document.getElementById('btn-toggle-script');
    if (!box) return;
    box.classList.toggle('hidden');
    if (btn) btn.innerText = box.classList.contains('hidden') ? '📜 Audio Transcript' : '✕ Hide Audio Transcript';
}

async function previewExaminerVoice() {
    const params = resolveSpeechParameters(currentAudioEngine, currentGeminiPersona, selectedBrowserVoiceURI);
    const personaLabel = currentAudioEngine === 'gemini' 
        ? `${currentGeminiPersona || 'Puck'} (Gemini AI Studio)` 
        : (params.voice ? `${params.name}` : 'System Cambridge Voice');

    const sample = `Good afternoon. This is the official IELTS examiner audio test using ${personaLabel}.`;
    const testBtns = [
        document.getElementById('btn-listening-test-voice'),
        document.getElementById('btn-preview-voice'),
        document.getElementById('btn-settings-preview-voice')
    ];
    testBtns.forEach(btn => {
        if (btn) btn.innerHTML = `<span>🔊 Testing...</span>`;
    });

    await playExaminerVoice(sample);
    setTimeout(() => {
        testBtns.forEach(btn => {
            if (btn) btn.innerHTML = '<span>🔊 Test</span>';
        });
    }, 2500);
}

function applyVoiceSelection(val) {
    if (!val) return;

    if (val.startsWith('gemini:')) {
        currentAudioEngine = 'gemini';
        currentGeminiPersona = val.replace('gemini:', '');
    } else if (val.startsWith('browser:')) {
        currentAudioEngine = 'browser';
        const uri = val.replace('browser:', '');
        selectedBrowserVoiceURI = (uri === 'auto' || uri === '') ? null : uri;
        if (selectedBrowserVoiceURI) {
            localStorage.setItem('ielts_browser_voice', selectedBrowserVoiceURI);
        } else {
            localStorage.removeItem('ielts_browser_voice');
        }
    } else if (['Puck', 'Aoede', 'Charon', 'Kore', 'Fenrir'].includes(val)) {
        currentAudioEngine = 'gemini';
        currentGeminiPersona = val;
    } else if (val === 'browser') {
        currentAudioEngine = 'browser';
        selectedBrowserVoiceURI = null;
    } else {
        currentAudioEngine = 'browser';
        selectedBrowserVoiceURI = val;
        localStorage.setItem('ielts_browser_voice', val);
    }

    syncVoiceUI();
}

function updateListeningVoiceSelection(val) {
    applyVoiceSelection(val);

    // If listening audio is playing, immediately switch voice and re-speak current sentence!
    if (listeningPassagePlaying) {
        if (currentAudioElement) {
            try { currentAudioElement.pause(); } catch(e){}
            currentAudioElement = null;
        }
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        if (listeningTimeoutId) {
            clearTimeout(listeningTimeoutId);
            listeningTimeoutId = null;
        }
        if (listeningSentenceIndex > 0) {
            listeningSentenceIndex--;
        }
        playNextListeningSentence();
    } else {
        const testBtn = document.getElementById('btn-listening-test-voice');
        if (testBtn) {
            const orig = testBtn.innerHTML;
            testBtn.innerHTML = '<span>✓ Voice Set!</span>';
            setTimeout(() => { testBtn.innerHTML = orig; }, 1400);
        }
    }
}

function updateSpeakingPersonaSelection(val) {
    applyVoiceSelection(val);
}

function updateAudioEnginePreference(val) {
    currentAudioEngine = val;
    syncVoiceUI();
}

function updateGeminiPersonaPreference(val) {
    currentGeminiPersona = val;
    syncVoiceUI();
}

function updateBrowserVoicePreference(val) {
    selectedBrowserVoiceURI = val;
    if (val) localStorage.setItem('ielts_browser_voice', val);
    else localStorage.removeItem('ielts_browser_voice');
    syncVoiceUI();
}

function syncVoiceUI() {
    localStorage.setItem('ielts_audio_engine', currentAudioEngine);
    localStorage.setItem('ielts_gemini_persona', currentGeminiPersona);
    if (selectedBrowserVoiceURI) {
        localStorage.setItem('ielts_browser_voice', selectedBrowserVoiceURI);
    }

    const currentSelectVal = currentAudioEngine === 'gemini' 
        ? `gemini:${currentGeminiPersona || 'Puck'}` 
        : (selectedBrowserVoiceURI ? `browser:${selectedBrowserVoiceURI}` : 'browser:auto');

    const listenVoice = document.getElementById('select-listening-voice');
    if (listenVoice) {
        if ([...listenVoice.options].some(o => o.value === currentSelectVal)) {
            listenVoice.value = currentSelectVal;
        } else if (currentAudioEngine === 'gemini' && [...listenVoice.options].some(o => o.value === `gemini:${currentGeminiPersona}`)) {
            listenVoice.value = `gemini:${currentGeminiPersona}`;
        } else if ([...listenVoice.options].some(o => o.value === currentGeminiPersona)) {
            listenVoice.value = currentGeminiPersona;
        } else {
            listenVoice.value = 'browser:auto';
        }
    }

    const speakPersona = document.getElementById('select-speaking-persona');
    if (speakPersona) {
        if ([...speakPersona.options].some(o => o.value === currentSelectVal)) {
            speakPersona.value = currentSelectVal;
        } else if (currentAudioEngine === 'gemini' && [...speakPersona.options].some(o => o.value === `gemini:${currentGeminiPersona}`)) {
            speakPersona.value = `gemini:${currentGeminiPersona}`;
        } else {
            speakPersona.value = 'browser:auto';
        }
    }

    const setEngine = document.getElementById('set-audio-engine');
    if (setEngine) setEngine.value = currentAudioEngine;

    const setPersona = document.getElementById('set-gemini-persona');
    if (setPersona) setPersona.value = currentGeminiPersona || 'Puck';

    const setBrowser = document.getElementById('set-browser-voice');
    if (setBrowser && selectedBrowserVoiceURI) setBrowser.value = selectedBrowserVoiceURI;
}
