/**
 * IELTS Master - Vocabulary Module
 * Handles Band 8+ academic collocation notebook, search/filtering, modal CRUD,
 * mastery toggling, and standards modal display.
 */

async function loadVocabulary() {
    try {
        const res = await fetch(`${API_BASE}/api/vocabulary`);
        vocabularyList = await res.json();
        renderVocabularyGrid(vocabularyList);
    } catch (err) {
        console.error('Failed loading vocabulary:', err);
    }
}

function renderVocabularyGrid(list) {
    const grid = document.getElementById('vocab-cards-grid');
    if (!grid) return;
    if (!list || list.length === 0) {
        grid.innerHTML = '<div class="col-span-full p-8 text-center text-xs text-slate-400">No vocabulary items added yet. Click "+ Add Collocation" or save suggestions from your Writing & Speaking reports!</div>';
        return;
    }

    grid.innerHTML = list.map(item => `
        <div class="p-4 rounded-xl bg-white border border-slate-200 shadow-sm flex flex-col justify-between hover:border-purple-300 transition-colors">
            <div>
                <div class="flex items-center justify-between mb-1.5">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700">${item.module_source || 'General'}</span>
                    <button onclick="toggleMastered(${item.id})" class="text-xs ${item.mastered ? 'text-emerald-600 font-bold' : 'text-slate-400 hover:text-slate-600'}">
                        ${item.mastered ? '✓ Mastered' : '○ Review'}
                    </button>
                </div>
                <h4 class="font-bold text-slate-900 text-sm mb-1">${item.word_or_phrase}</h4>
                <p class="text-xs text-slate-600 mb-2">${item.meaning || ''}</p>
                ${item.context ? `<p class="text-[11px] text-slate-500 italic bg-slate-50 p-2 rounded-lg border border-slate-100">"${item.context}"</p>` : ''}
            </div>
            <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                <span>${item.band_level || 'Band 8+'}</span>
                <button onclick="deleteVocab(${item.id})" class="text-rose-500 hover:text-rose-700">Delete</button>
            </div>
        </div>
    `).join('');
}

function filterVocabulary() {
    const query = document.getElementById('vocab-search').value.toLowerCase();
    const mod = document.getElementById('vocab-filter-module').value;

    const filtered = vocabularyList.filter(item => {
        const matchesQuery = item.word_or_phrase.toLowerCase().includes(query) ||
                             (item.meaning && item.meaning.toLowerCase().includes(query)) ||
                             (item.context && item.context.toLowerCase().includes(query));
        const matchesMod = mod === 'all' || (item.module_source && item.module_source.toLowerCase().includes(mod.toLowerCase()));
        return matchesQuery && matchesMod;
    });

    renderVocabularyGrid(filtered);
}

async function quickSaveVocab(word, context, module_source) {
    try {
        await fetch(`${API_BASE}/api/vocabulary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                word: word,
                context: context,
                band_level: 'Band 8+',
                module_source: module_source
            })
        });
        alert(`Saved "${word}" to your Band 8+ Vocabulary Notebook!`);
        await loadVocabulary();
    } catch (err) {
        alert('Failed saving word: ' + err.message);
    }
}

function openAddVocabModal() {
    document.getElementById('modal-add-vocab').classList.remove('hidden');
}

function closeAddVocabModal() {
    document.getElementById('modal-add-vocab').classList.add('hidden');
}

async function saveNewVocabulary() {
    const word = document.getElementById('add-vocab-word').value.trim();
    const meaning = document.getElementById('add-vocab-meaning').value.trim();
    const context = document.getElementById('add-vocab-context').value.trim();
    const module_source = document.getElementById('add-vocab-module').value;

    if (!word) {
        alert('Please enter a word or collocation phrase.');
        return;
    }

    try {
        await fetch(`${API_BASE}/api/vocabulary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word, meaning, context, module_source, band_level: 'Band 8+' })
        });
        closeAddVocabModal();
        await loadVocabulary();
    } catch (err) {
        alert('Error saving word: ' + err.message);
    }
}

async function toggleMastered(id) {
    try {
        await fetch(`${API_BASE}/api/vocabulary/${id}/toggle`, { method: 'POST' });
        await loadVocabulary();
    } catch (err) {
        console.error('Failed toggling word:', err);
    }
}

async function deleteVocab(id) {
    if (!confirm('Are you sure you want to delete this word from your notebook?')) return;
    try {
        await fetch(`${API_BASE}/api/vocabulary/${id}`, { method: 'DELETE' });
        await loadVocabulary();
    } catch (err) {
        console.error('Failed deleting word:', err);
    }
}

function toggleIeltsStandardsModal(isOpen) {
    const modal = document.getElementById('modal-ielts-standards');
    if (!modal) return;
    if (isOpen) {
        modal.classList.remove('hidden');
    } else {
        modal.classList.add('hidden');
    }
}
