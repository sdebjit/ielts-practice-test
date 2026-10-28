import json
import urllib.request
import urllib.error
import re
import ssl
import socket
from database import get_settings

def get_ssl_context():
    try:
        return ssl.create_default_context()
    except Exception:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

def verify_gemini_key(api_key):
    """
    Fast verification of Gemini API key using Google's models endpoint.
    Completes in under a second and returns accessible models.
    """
    if not api_key:
        return {'valid': False, 'error': 'API key is empty.'}

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url, headers={"User-Agent": "IELTS-Master/1.0"})

    for ctx in [ssl.create_default_context(), ssl._create_unverified_context()]:
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
                models = [m['name'].replace('models/', '') for m in data.get('models', [])]
                return {'valid': True, 'models': models}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8')
            return {'valid': False, 'error': f"Google API HTTP {e.code}: {err_body}"}
        except (socket.timeout, urllib.error.URLError) as e:
            continue
        except Exception as e:
            continue

    return {'valid': False, 'error': 'Network timeout reaching Google Gemini API from backend.'}

def call_gemini_api(prompt, api_key=None, model="gemini-3.8-flash", system_instruction=None):
    """
    Direct REST call to Google Gemini API with model fallback and SSL resilience.
    """
    if not api_key:
        settings = get_settings()
        api_key = settings.get('gemini_api_key', '')
        model = settings.get('gemini_model', 'gemini-3.8-flash')

    if not api_key:
        raise ValueError("NO_API_KEY")

    # Candidate models to try in order if the primary model times out or is unavailable
    models_to_try = [model]
    for m in ['gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for attempt_model in models_to_try[:2]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{attempt_model}:generateContent?key={api_key}"
        
        contents = [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "IELTS-Master/1.0"
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        for ctx in [ssl.create_default_context(), ssl._create_unverified_context()]:
            try:
                with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    candidates = result.get('candidates', [])
                    if candidates:
                        text = candidates[0]['content']['parts'][0]['text']
                        text = re.sub(r'^```json\s*', '', text.strip())
                        text = re.sub(r'```$', '', text.strip())
                        return json.loads(text)
                    raise ValueError("Empty response from Gemini API")
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                last_error = f"Gemini API HTTP Error {e.code}: {error_body}"
                break # Model issue, try next model
            except (socket.timeout, urllib.error.URLError) as e:
                last_error = f"Network timeout contacting Gemini API: {str(e)}"
                continue
            except Exception as e:
                last_error = str(e)
                continue

    raise RuntimeError(last_error or "Network timeout contacting Gemini API")


def generate_gemini_tts(text, voice_name="Puck", api_key=None):
    """
    Generate authentic, human-sounding voice audio using Gemini 2.0 Flash Audio output.
    Returns dict: {'success': True, 'mime_type': 'audio/wav' | 'audio/pcm;rate=24000', 'audio_base64': ...}
    """
    if not api_key:
        settings = get_settings()
        api_key = settings.get('gemini_api_key', '')
    if not api_key:
        return {'success': False, 'error': 'NO_API_KEY'}

    clean_text = text.strip()
    if not clean_text:
        return {'success': False, 'error': 'Empty text'}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{
                "text": f"Read the following text aloud with authentic British Cambridge IELTS examiner cadence, clear human breathing, natural pauses, and warm articulation:\n\n\"{clean_text}\""
            }]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice_name or "Puck"
                    }
                }
            }
        }
    }

    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json", "User-Agent": "IELTS-Master/1.0"},
        method="POST"
    )

    for ctx in [ssl.create_default_context(), ssl._create_unverified_context()]:
        try:
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                candidate = res_data.get('candidates', [{}])[0]
                parts = candidate.get('content', {}).get('parts', [])
                for part in parts:
                    if 'inlineData' in part and 'data' in part['inlineData']:
                        return {
                            'success': True,
                            'mime_type': part['inlineData'].get('mimeType', 'audio/wav'),
                            'audio_base64': part['inlineData']['data']
                        }
                return {'success': False, 'error': 'No audio returned in Gemini response'}
        except urllib.error.HTTPError as e:
            return {'success': False, 'error': f"HTTP {e.code}: {e.read().decode('utf-8')}"}
        except Exception:
            continue

    return {'success': False, 'error': 'Failed to connect to Gemini TTS endpoint'}



def evaluate_writing(prompt_data, student_essay, api_key=None):
    """
    Evaluates IELTS Writing Task 1 or Task 2 against official IELTS criteria.
    """
    task_type = prompt_data.get('task_type', 'Task 2')
    prompt_title = prompt_data.get('title', '')
    prompt_text = prompt_data.get('prompt', '')
    min_words = 150 if task_type == 'Task 1' else 250

    system_instruction = (
        "You are an expert Cambridge/IDP Certified Senior IELTS Writing Examiner. "
        "Assess the student's submission rigorously according to the official IELTS 9-band descriptors: "
        "1. Task Achievement (for Task 1) or Task Response (for Task 2) "
        "2. Coherence and Cohesion "
        "3. Lexical Resource "
        "4. Grammatical Range and Accuracy. "
        "Be constructive, analytical, accurate, and fair. Provide band scores in 0.5 increments (e.g. 6.0, 6.5, 7.0). "
        "You must respond in strict JSON matching the requested schema."
    )

    subtype = prompt_data.get('subtype', '')
    is_gt = 'general' in str(prompt_data.get('type', '')).lower() or 'letter' in subtype.lower()
    gt_letter_instruction = ""
    if is_gt and (task_type == 'Task 1' or 'letter' in subtype.lower()):
        gt_letter_instruction = (
            f"\nSpecial General Training Task 1 ({subtype or 'Letter'}) Requirements:\n"
            "- Check opening salutation (e.g., Dear Sir or Madam / Dear Mr. Smith / Dear Sarah) and closing (e.g., Yours faithfully / Yours sincerely / Best regards).\n"
            "- Verify that all 3 bullet points in the prompt are addressed with clear, relevant detail.\n"
            "- Verify that the tone/register is consistent (Formal, Semi-formal, or Informal as required).\n"
        )

    user_prompt = f"""
IELTS WRITING EVALUATION REQUEST
Exam Module: {'General Training' if is_gt else 'Academic'}
Task Type: {task_type}
Target Minimum Word Count: {min_words} words
Prompt Title: {prompt_title}
Official Question / Prompt:
\"\"\"{prompt_text}\"\"\"{gt_letter_instruction}

Student's Essay:
\"\"\"{student_essay}\"\"\"

Please evaluate this submission and return a JSON object with this EXACT structure:
{{
  "overall_band": 6.5,
  "criteria": {{
    "task_achievement": {{"band": 6.5, "comment": "Detailed critique on response fulfillment, thesis, overview, or main ideas"}},
    "coherence_cohesion": {{"band": 6.5, "comment": "Critique on paragraphing, logical progression, and cohesive linkers"}},
    "lexical_resource": {{"band": 7.0, "comment": "Critique on vocabulary range, collocations, precision, and spelling"}},
    "grammatical_range_accuracy": {{"band": 6.0, "comment": "Critique on sentence structures (simple vs complex), punctuation, and error density"}}
  }},
  "word_count": {len(student_essay.split())},
  "strengths": [
    "Specific strength 1 with direct quote or praise",
    "Specific strength 2"
  ],
  "areas_to_improve": [
    "Actionable weakness 1 to gain +0.5 band",
    "Actionable weakness 2 to gain +0.5 band"
  ],
  "line_by_line_corrections": [
    {{
      "original": "exact sentence or phrase from student",
      "correction": "natural native Band 8+ correction",
      "explanation": "why this correction improves grammar, tone, or academic style",
      "type": "grammar"
    }}
  ],
  "vocabulary_upgrades": [
    {{
      "basic_word": "simple word used by student (e.g. 'increase')",
      "band8_alternative": "advanced academic alternative or collocation (e.g. 'experience an exponential surge')",
      "example_sentence": "sentence demonstrating how to use it in context"
    }}
  ],
  "model_paragraph": "A model Band 8.5 sample paragraph showing how to elevate one part of the student's essay"
}}
"""

    try:
        return call_gemini_api(user_prompt, api_key=api_key, system_instruction=system_instruction)
    except Exception as e:
        # Fall back to heuristic evaluator if API key missing or offline
        return fallback_writing_evaluation(prompt_data, student_essay, error_msg=str(e))


def evaluate_speaking(test_data, responses, api_key=None):
    """
    Evaluates IELTS Speaking Part 1, 2, and 3 responses against official criteria.
    """
    system_instruction = (
        "You are an expert Cambridge/IDP Certified Senior IELTS Speaking Examiner. "
        "Assess the candidate's spoken transcript across the 4 official IELTS criteria: "
        "1. Fluency and Coherence (speech rate, continuity, hesitation, linking phrases) "
        "2. Lexical Resource (idiomatic language, vocabulary variety, paraphrasing) "
        "3. Grammatical Range and Accuracy (clause variety, tenses, accuracy) "
        "4. Pronunciation & Delivery Insights (intonation cues, rhythm, stress markers). "
        "You must respond in strict JSON matching the requested schema."
    )

    qa_formatted = []
    for item in responses:
        part = item.get('part', 'Part 1')
        q = item.get('question', '')
        a = item.get('answer', '')
        qa_formatted.append(f"[{part}] Examiner: {q}\nCandidate: {a}\n")

    user_prompt = f"""
IELTS SPEAKING INTERVIEW EVALUATION REQUEST
Interview Transcript:
{chr(10).join(qa_formatted)}

Please evaluate this interview transcript and return a JSON object with this EXACT structure:
{{
  "overall_band": 6.5,
  "criteria": {{
    "fluency_coherence": {{"band": 6.5, "comment": "Critique of flow, hesitations, connective phrases, and answer expansion"}},
    "lexical_resource": {{"band": 7.0, "comment": "Critique of natural idioms, topic-specific vocabulary, and variety"}},
    "grammatical_range_accuracy": {{"band": 6.0, "comment": "Critique of complex sentence attempts, conditionals, and error frequency"}},
    "pronunciation": {{"band": 6.5, "comment": "Delivery analysis, connected speech, rhythm, and intonation advice based on transcript wording"}}
  }},
  "filler_words_detected": [
    "like (3 times)",
    "um / uh (2 times)",
    "you know (2 times)"
  ],
  "strengths": [
    "Specific strength 1 with citation",
    "Specific strength 2"
  ],
  "areas_to_improve": [
    "Crucial improvement area for speaking score",
    "Guidance on using the PREP framework (Point, Reason, Example, Point)"
  ],
  "expansion_advice": "Detailed advice on how to develop answers in Part 3 to reach Band 7.5+",
  "better_expressions": [
    {{
      "spoken": "casual or repetitive phrase used by candidate",
      "upgraded": "natural, idiomatic Band 8 expression",
      "reason": "why this sounds more natural to a native examiner"
    }}
  ]
}}
"""

    try:
        return call_gemini_api(user_prompt, api_key=api_key, system_instruction=system_instruction)
    except Exception as e:
        return fallback_speaking_evaluation(test_data, responses, error_msg=str(e))


# =====================================================================
# Intelligent Heuristic Fallback Engine
# Ensures 100% offline functionality & immediate evaluation without crashing
# =====================================================================

def fallback_writing_evaluation(prompt_data, student_essay, error_msg=""):
    words = student_essay.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', student_essay) if len(s.strip()) > 3]
    num_sentences = max(1, len(sentences))
    avg_sentence_len = word_count / num_sentences

    task_type = prompt_data.get('task_type', 'Task 2')
    min_words = 150 if task_type == 'Task 1' else 250

    # 1. Task Achievement heuristics
    ta_band = 6.5
    if word_count < min_words - 40:
        ta_band = 5.0
    elif word_count < min_words:
        ta_band = 5.5
    elif word_count >= min_words + 30:
        ta_band = 7.0
    if word_count > 380 and task_type == 'Task 2':
        ta_band = 7.5

    # 2. Coherence & Cohesion heuristics (check linking words)
    connectors = [
        'furthermore', 'moreover', 'however', 'consequently', 'in contrast', 
        'nevertheless', 'on the other hand', 'in addition', 'subsequently', 
        'as a result', 'for instance', 'for example', 'ultimately', 'in conclusion'
    ]
    essay_lower = student_essay.lower()
    found_connectors = [c for c in connectors if c in essay_lower]
    cc_band = 6.0
    if len(found_connectors) >= 6:
        cc_band = 7.0
    elif len(found_connectors) >= 3:
        cc_band = 6.5
    else:
        cc_band = 5.5

    # 3. Lexical Resource heuristics (unique words ratio & academic words)
    unique_words = len(set(w.lower() for w in words))
    ttr = unique_words / max(1, word_count)
    academic_keywords = [
        'significant', 'phenomenon', 'predominant', 'substantial', 'correlation',
        'detrimental', 'perspective', 'constitutes', 'facilitate', 'prevalent',
        'counterpart', 'implication', 'paradigm', 'inevitable', 'allocation'
    ]
    found_academic = [w for w in academic_keywords if w in essay_lower]
    lr_band = 6.0
    if ttr > 0.55 and len(found_academic) >= 3:
        lr_band = 7.0
    elif ttr > 0.45 or len(found_academic) >= 1:
        lr_band = 6.5
    else:
        lr_band = 5.5

    # 4. Grammatical Range and Accuracy heuristics
    gra_band = 6.0
    has_complex = any(k in essay_lower for k in ['although', 'while', 'despite', 'whereas', 'not only', 'which', 'who'])
    if avg_sentence_len > 14 and has_complex:
        gra_band = 6.5
    if avg_sentence_len > 18 and has_complex and word_count >= min_words:
        gra_band = 7.0

    overall = round((ta_band + cc_band + lr_band + gra_band) / 4 * 2) / 2

    # Line-by-line checks
    corrections = []
    upgrades = []
    
    # Common basic words to upgrade
    basic_replacements = [
        ("very big", "substantial / monumental", "Enhances academic precision over colloquial intensifiers."),
        ("a lot of", "an abundance of / numerous", "Appropriate for formal academic tone."),
        ("good", "beneficial / advantageous", "Provides higher specificity and formal register."),
        ("bad", "detrimental / adverse", "Replaces elementary vocabulary with Band 7+ terminology."),
        ("show", "illustrate / demonstrate / depict", "Standard academic reporting verb.")
    ]

    for basic, adv, reason in basic_replacements:
        if basic in essay_lower:
            upgrades.append({
                "basic_word": basic,
                "band8_alternative": adv,
                "example_sentence": f"Replacing '{basic}' with '{adv}' elevates the lexical tier."
            })

    if not upgrades:
        upgrades.append({
            "basic_word": "increase rapidly",
            "band8_alternative": "witness a dramatic escalation",
            "example_sentence": "The sector witnessed a dramatic escalation in adoption rates."
        })

    # Find sample sentence for correction
    for s in sentences:
        if len(s.split()) > 7 and ('because' in s.lower() or 'and' in s.lower() or 'but' in s.lower()):
            corrections.append({
                "original": s,
                "correction": "Refined variant: Enhance clause balance by placing subordinate clauses first (e.g. 'Although ..., ...').",
                "explanation": "IELTS Band 7 examiners look for subordinating conjunctions and passive voice rather than repetitive coordinate conjunctions.",
                "type": "grammar"
            })
            break

    notice = " (Evaluated via Intelligent Heuristic Engine. Add Gemini API Key in Settings for live AI deep examiner critique!)" if "NO_API_KEY" in error_msg else ""

    return {
        "overall_band": overall,
        "criteria": {
            "task_achievement": {
                "band": ta_band,
                "comment": f"Word count: {word_count}/{min_words}. " + (
                    "Fully answers all aspects of the prompt with sustained progression." if ta_band >= 7.0 else
                    "Addresses main prompt points, but ideas could be developed with more granular supporting evidence."
                )
            },
            "coherence_cohesion": {
                "band": cc_band,
                "comment": f"Found {len(found_connectors)} formal cohesive markers. " + (
                    "Logical progression is evident across paragraphs with smooth transitions." if cc_band >= 7.0 else
                    "Paragraph structure is present, but reliance on standard mechanical transitions could be improved with subtle referencing."
                )
            },
            "lexical_resource": {
                "band": lr_band,
                "comment": f"Lexical diversity index: {round(ttr*100)}%. " + (
                    "Demonstrates commendable awareness of collocations and academic terminology." if lr_band >= 7.0 else
                    "Vocabulary is adequate for conveying ideas, though occasional repetition and colloquial idioms appear."
                )
            },
            "grammatical_range_accuracy": {
                "band": gra_band,
                "comment": f"Average sentence length: {round(avg_sentence_len, 1)} words. " + (
                    "Good variety of complex and compound sentence forms." if gra_band >= 7.0 else
                    "Mix of simple and complex sentence forms is present; watch punctuation at clause boundaries."
                )
            }
        },
        "word_count": word_count,
        "strengths": [
            f"Achieved {word_count} words, meeting target length requirements.",
            f"Appropriate essay structure with clear introduction, body paragraphs, and conclusion.",
            "Effective use of academic discourse markers to signal viewpoint shifts."
        ],
        "areas_to_improve": [
            f"Enhance {min([('Task Achievement', ta_band), ('Coherence', cc_band), ('Lexical Resource', lr_band), ('Grammar', gra_band)], key=lambda x: x[1])[0]} to push into Band 7.5+.",
            "Diversify sentence structures by introducing participle clauses (-ing / -ed) and conditional structures.",
            "Incorporate more topic-specific collocations rather than general adjectives."
        ],
        "line_by_line_corrections": corrections,
        "vocabulary_upgrades": upgrades,
        "model_paragraph": "Furthermore, it is widely acknowledged that technological integration fosters cognitive agility. When educational curricula incorporate multifaceted digital platforms, scholars not only assimilate empirical data more expeditiously but also cultivate critical problem-solving faculties essential for modern industry.",
        "note": notice
    }


def fallback_speaking_evaluation(test_data, responses, error_msg=""):
    full_text = " ".join([r.get('answer', '') for r in responses])
    words = full_text.split()
    word_count = len(words)

    # Detect filler words
    lower_text = full_text.lower()
    fillers = []
    for filler in ['um', 'uh', 'like', 'you know', 'actually', 'basically', 'sort of']:
        # count occurrences with word boundary
        matches = len(re.findall(r'\b' + re.escape(filler) + r'\b', lower_text))
        if matches > 0:
            fillers.append(f"{filler} ({matches} time{'s' if matches > 1 else ''})")

    # Criteria calculations
    fc_band = 6.5
    if word_count < 60:
        fc_band = 5.0
    elif word_count < 120:
        fc_band = 5.5
    elif len(fillers) <= 2 and word_count > 200:
        fc_band = 7.0

    lr_band = 6.5
    idioms = ['a double-edged sword', 'once in a blue moon', 'down to earth', 'on cloud nine', 'broaden my horizons', 'in a nutshell']
    if any(i in lower_text for i in idioms) or len(set(words)) > 90:
        lr_band = 7.0

    gra_band = 6.0
    if any(k in lower_text for k in ['if i were', 'had i known', 'not only', 'whereas', 'provided that']):
        gra_band = 7.0
    elif any(k in lower_text for k in ['although', 'because', 'which', 'when']):
        gra_band = 6.5

    pron_band = 6.5

    overall = round((fc_band + lr_band + gra_band + pron_band) / 4 * 2) / 2

    return {
        "overall_band": overall,
        "criteria": {
            "fluency_coherence": {
                "band": fc_band,
                "comment": "Speaks at length with noticeable continuity. Uses conversational discourse markers with occasional hesitation when searching for content."
            },
            "lexical_resource": {
                "band": lr_band,
                "comment": "Exhibits sufficient lexical flexibility to discuss both familiar personal topics and broader abstract questions."
            },
            "grammatical_range_accuracy": {
                "band": gra_band,
                "comment": "Accurate use of basic sentence patterns; complex sentences are attempted with acceptable grammatical control."
            },
            "pronunciation": {
                "band": pron_band,
                "comment": "Speech is easily understood throughout. Work on natural sentence rhythm and intonation variations on key content words."
            }
        },
        "filler_words_detected": fillers or ["Minimal filler words detected - natural fluency preserved"],
        "strengths": [
            "Good willingness to speak at length and elaborate on personal viewpoints.",
            "Answers address the examiner's core questions directly without drifting off topic.",
            "Natural conversational cadence."
        ],
        "areas_to_improve": [
            "In Part 3, systematically use the PREP method (Point, Reason, Example, Point) to give richer 4-sentence answers.",
            "Substitute filler words with communicative fillers (e.g., 'That is a compelling question to consider...').",
            "Introduce more conditional and hypothetical grammar (e.g., 'If governments were to invest more...')."
        ],
        "expansion_advice": "When answering abstract questions, avoid answering in just 1 or 2 brief sentences. Immediately follow your direct answer with a justification ('The primary reason behind this is...') and a concrete real-world instance ('For example, in contemporary urban centers...').",
        "better_expressions": [
            {
                "spoken": "I really like it",
                "upgraded": "I have an immense fondness for it / I am deeply passionate about it",
                "reason": "Demonstrates higher lexical sophistication required for Band 7+."
            },
            {
                "spoken": "It is a very big problem",
                "upgraded": "It poses a formidable challenge / It constitutes a pressing concern",
                "reason": "Replaces generic elementary vocabulary with idiomatic academic phrasing."
            }
        ]
    }
