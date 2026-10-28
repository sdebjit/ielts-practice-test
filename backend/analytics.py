import json
from datetime import datetime, timedelta
from database import get_connection, get_settings

def calculate_ielts_overall(l, r, w, s):
    """
    Official IELTS Overall Band Score Rounding Formula:
    Calculates average of the four components (or available assessed components).
    If the average ends in .25, it is rounded up to the next half band (e.g., 6.25 -> 6.5).
    If it ends in .75, it is rounded up to the next whole band (e.g., 6.75 -> 7.0).
    If it ends in .125, it rounds down to the whole band.
    """
    scores = [s for s in [l, r, w, s] if s is not None and s > 0]
    if not scores:
        return None
    
    avg = sum(scores) / len(scores)
    # Round to 3 decimal places to prevent float precision quirks
    avg = round(avg, 3)
    whole = int(avg)
    fraction = avg - whole

    if fraction < 0.25:
        return float(whole)
    elif fraction < 0.75:
        return float(whole + 0.5)
    else:
        return float(whole + 1.0)

def get_diagnostics(user_id=1):
    conn = get_connection()
    settings = get_settings(user_id=user_id)
    target_band = settings.get('target_band', 7.5)

    # Fetch all attempts for this specific user
    rows = conn.execute('''
    SELECT a.*, t.title as test_title
    FROM attempts a
    LEFT JOIN tests t ON a.test_id = t.id
    WHERE a.user_id = ?
    ORDER BY a.created_at ASC
    ''', (user_id,)).fetchall()
    
    # Fetch study logs for streaks for this specific user
    logs = conn.execute('SELECT activity_date, SUM(minutes) as total_min FROM study_logs WHERE user_id = ? GROUP BY activity_date ORDER BY activity_date DESC', (user_id,)).fetchall()
    conn.close()

    module_attempts = {
        'listening': [],
        'reading': [],
        'writing': [],
        'speaking': []
    }

    for r in rows:
        d = dict(r)
        try:
            d['criterion_scores'] = json.loads(d['criterion_scores'])
        except Exception:
            d['criterion_scores'] = {}
        try:
            d['ai_feedback'] = json.loads(d['ai_feedback'])
        except Exception:
            d['ai_feedback'] = {}
        
        mod = d['module'].lower()
        if mod in module_attempts:
            module_attempts[mod].append(d)

    # Detailed Module Score & Trend Computation
    def analyze_module_score_and_trend(attempts_list):
        if not attempts_list:
            return {
                'score': None,
                'status': 'not_assessed',
                'trend': 'none',
                'delta': 0.0,
                'attempts_count': 0,
                'display': 'Not yet assessed',
                'latest_score': None
            }
        
        attempts_count = len(attempts_list)
        recent = attempts_list[-3:]
        current_score = round(sum(a['band_score'] for a in recent) / len(recent), 1)
        latest_score = attempts_list[-1]['band_score']

        if attempts_count == 1:
            trend = 'established'
            delta = 0.0
        else:
            prev_score = attempts_list[-2]['band_score']
            delta = round(latest_score - prev_score, 1)
            if delta > 0:
                trend = 'improved'
            elif delta < 0:
                trend = 'declined'
            else:
                trend = 'stable'

        return {
            'score': current_score,
            'status': 'assessed',
            'trend': trend,
            'delta': delta,
            'attempts_count': attempts_count,
            'display': f'Band {current_score:.1f}',
            'latest_score': latest_score
        }

    l_meta = analyze_module_score_and_trend(module_attempts['listening'])
    r_meta = analyze_module_score_and_trend(module_attempts['reading'])
    w_meta = analyze_module_score_and_trend(module_attempts['writing'])
    s_meta = analyze_module_score_and_trend(module_attempts['speaking'])

    l_band = l_meta['score']
    r_band = r_meta['score']
    w_band = w_meta['score']
    s_band = s_meta['score']

    assessed_modules = [m for m, meta in [('listening', l_meta), ('reading', r_meta), ('writing', w_meta), ('speaking', s_meta)] if meta['status'] == 'assessed']
    assessed_count = len(assessed_modules)

    overall_band = calculate_ielts_overall(l_band, r_band, w_band, s_band)
    is_assessed = overall_band is not None

    if is_assessed:
        band_gap = round(target_band - overall_band, 1)
        target_achieved = overall_band >= target_band
        display_overall = f"Band {overall_band:.1f}"
    else:
        band_gap = None
        target_achieved = False
        display_overall = "Not yet assessed"

    # Overall cross-attempt trend
    overall_trend = 'none'
    overall_delta = 0.0
    if len(rows) > 1:
        last_score = rows[-1]['band_score']
        prev_score = rows[-2]['band_score']
        overall_delta = round(last_score - prev_score, 1)
        if overall_delta > 0:
            overall_trend = 'improved'
        elif overall_delta < 0:
            overall_trend = 'declined'
        else:
            overall_trend = 'stable'
    elif len(rows) == 1:
        overall_trend = 'established'

    # Calculate Study Streak
    streak_days = 0
    today = datetime.now().date()
    log_dates = {datetime.strptime(row['activity_date'], '%Y-%m-%d').date() for row in logs if row['activity_date']}
    
    check_day = today
    if check_day not in log_dates:
        check_day = today - timedelta(days=1)
    
    while check_day in log_dates:
        streak_days += 1
        check_day -= timedelta(days=1)

    # Total stats
    total_practice_sessions = len(rows)
    total_minutes_practiced = sum(row['total_min'] for row in logs) if logs else 0

    # 1. Listening Diagnostics
    listening_diag = analyze_listening(module_attempts['listening'])
    # 2. Reading Diagnostics
    reading_diag = analyze_reading(module_attempts['reading'])
    # 3. Writing Diagnostics
    writing_diag = analyze_writing(module_attempts['writing'])
    # 4. Speaking Diagnostics
    speaking_diag = analyze_speaking(module_attempts['speaking'])

    # Synthesize Top 3 Priorities for Improvement
    priorities = generate_priorities(overall_band, target_band, {
        'listening': (l_meta, listening_diag),
        'reading': (r_meta, reading_diag),
        'writing': (w_meta, writing_diag),
        'speaking': (s_meta, speaking_diag)
    })

    # Prepare timeline chart data
    chart_data = {
        'dates': [],
        'overall': [],
        'listening': [],
        'reading': [],
        'writing': [],
        'speaking': []
    }
    
    for att in rows[-15:]:
        created = att['created_at'][:10]
        chart_data['dates'].append(created)
        chart_data[att['module'].lower()].append(att['band_score'])

    return {
        'overview': {
            'overall_band': overall_band,
            'is_assessed': is_assessed,
            'display_overall_band': display_overall,
            'target_band': target_band,
            'band_gap': band_gap,
            'target_achieved': target_achieved,
            'overall_trend': overall_trend,
            'overall_delta': overall_delta,
            'assessed_count': assessed_count,
            'streak_days': streak_days,
            'total_sessions': total_practice_sessions,
            'total_minutes': total_minutes_practiced,
            'module_scores': {
                'listening': l_band,
                'reading': r_band,
                'writing': w_band,
                'speaking': s_band
            },
            'module_details': {
                'listening': l_meta,
                'reading': r_meta,
                'writing': w_meta,
                'speaking': s_meta
            }
        },
        'diagnostics': {
            'listening': listening_diag,
            'reading': reading_diag,
            'writing': writing_diag,
            'speaking': speaking_diag
        },
        'priorities': priorities,
        'chart_data': chart_data
    }

def analyze_listening(attempts):
    if not attempts:
        return {
            'status': 'Not yet assessed',
            'weakest_question_type': 'Not yet assessed',
            'accuracy_by_type': {},
            'key_advice': 'Complete your first Listening test (4 sections, 40 questions) to assess your initial band and detect distractor traps.',
            'recommendation': 'Take Listening Test 1 to establish baseline.'
        }
    
    # Aggregate question type performance
    type_counts = {}
    type_correct = {}
    for att in attempts:
        c = att.get('criterion_scores', {})
        breakdown = c.get('question_type_breakdown', {})
        for qtype, stats in breakdown.items():
            type_counts[qtype] = type_counts.get(qtype, 0) + stats.get('total', 0)
            type_correct[qtype] = type_correct.get(qtype, 0) + stats.get('correct', 0)
    
    accuracy = {}
    for qtype in type_counts:
        accuracy[qtype] = round((type_correct[qtype] / type_counts[qtype]) * 100) if type_counts[qtype] > 0 else 0
    
    weakest = min(accuracy.items(), key=lambda x: x[1])[0] if accuracy else 'Multiple Choice'
    
    return {
        'status': f'{len(attempts)} test(s) completed',
        'weakest_question_type': weakest,
        'accuracy_by_type': accuracy or {'Multiple Choice': 65, 'Form Completion': 80, 'Matching': 70},
        'key_advice': f'Focus on {weakest}. In IELTS listening, pre-reading question stems and predicting part-of-speech improves accuracy by 25%.',
        'recommendation': f'Drill {weakest} questions with audio script comparison.'
    }

def analyze_reading(attempts):
    if not attempts:
        return {
            'status': 'Not yet assessed',
            'weakest_question_type': 'Not yet assessed',
            'accuracy_by_type': {},
            'key_advice': 'Complete your first Reading test (3 passages, 40 questions) to establish your baseline and diagnose True/False/Not Given accuracy.',
            'recommendation': 'Practice differentiating between "FALSE" (contradiction) and "NOT GIVEN" (absence of proof).'
        }
    
    type_counts = {}
    type_correct = {}
    for att in attempts:
        c = att.get('criterion_scores', {})
        breakdown = c.get('question_type_breakdown', {})
        for qtype, stats in breakdown.items():
            type_counts[qtype] = type_counts.get(qtype, 0) + stats.get('total', 0)
            type_correct[qtype] = type_correct.get(qtype, 0) + stats.get('correct', 0)
    
    accuracy = {}
    for qtype in type_counts:
        accuracy[qtype] = round((type_correct[qtype] / type_counts[qtype]) * 100) if type_counts[qtype] > 0 else 0
    
    weakest = min(accuracy.items(), key=lambda x: x[1])[0] if accuracy else 'True/False/Not Given'

    return {
        'status': f'{len(attempts)} test(s) completed',
        'weakest_question_type': weakest,
        'accuracy_by_type': accuracy or {'True/False/Not Given': 60, 'Matching Headings': 68, 'Summary Completion': 78},
        'key_advice': f'Your main bottleneck is {weakest}. Practice skimming for keywords vs scanning for nuanced relationships.',
        'recommendation': f'Do 1 timed passage focusing purely on {weakest}.'
    }

def analyze_writing(attempts):
    if not attempts:
        return {
            'status': 'Not yet assessed',
            'criteria_averages': {},
            'bottleneck_criterion': 'Not yet assessed',
            'common_weaknesses': [
                'No writing submissions evaluated yet'
            ],
            'key_advice': 'Submit a Task 1 report or Task 2 essay to receive official examiner criterion breakdown and Band 8 lexical suggestions.',
            'recommendation': 'Submit an essay to receive line-by-line Gemini examiner critique.'
        }
    
    crit_totals = {'task_achievement': 0, 'coherence_cohesion': 0, 'lexical_resource': 0, 'grammatical_range_accuracy': 0}
    crit_counts = {'task_achievement': 0, 'coherence_cohesion': 0, 'lexical_resource': 0, 'grammatical_range_accuracy': 0}
    weaknesses = []

    for att in attempts:
        c = att.get('criterion_scores', {})
        fb = att.get('ai_feedback', {})
        if isinstance(fb, dict) and 'areas_to_improve' in fb:
            weaknesses.extend(fb['areas_to_improve'][:2])
        
        for k in crit_totals:
            if k in c and isinstance(c[k], (int, float)):
                crit_totals[k] += c[k]
                crit_counts[k] += 1
            elif k in c and isinstance(c[k], dict) and 'band' in c[k]:
                crit_totals[k] += float(c[k]['band'])
                crit_counts[k] += 1

    averages = {}
    display_names = {
        'task_achievement': 'Task Achievement',
        'coherence_cohesion': 'Coherence & Cohesion',
        'lexical_resource': 'Lexical Resource',
        'grammatical_range_accuracy': 'Grammar Range & Accuracy'
    }
    for k in crit_totals:
        averages[display_names[k]] = round(crit_totals[k] / crit_counts[k], 1) if crit_counts[k] > 0 else 6.0
    
    bottleneck = min(averages.items(), key=lambda x: x[1])[0]

    return {
        'status': f'{len(attempts)} essay(s) evaluated',
        'criteria_averages': averages,
        'bottleneck_criterion': bottleneck,
        'common_weaknesses': list(dict.fromkeys(weaknesses))[:3] or [
            'Need more varied cohesive linkers beyond "Moreover" and "Furthermore"',
            'Occasional repetitive word choice in body paragraphs',
            'Punctuation and clause boundary precision'
        ],
        'key_advice': f'To jump +0.5 band, target {bottleneck}. Band 7+ examiners look specifically for deliberate sentence variety and precise academic collocations.',
        'recommendation': 'Write a 250-word Task 2 essay applying Band 8 collocations.'
    }

def analyze_speaking(attempts):
    if not attempts:
        return {
            'status': 'Not yet assessed',
            'criteria_averages': {},
            'bottleneck_criterion': 'Not yet assessed',
            'filler_word_frequency': 'Not yet assessed',
            'key_advice': 'Record a simulated 3-part examiner interview to measure speech fluency, lexical resource, and filler word frequency.',
            'recommendation': 'Start a simulated 3-part examiner interview with voice synthesis.'
        }
    
    crit_totals = {'fluency_coherence': 0, 'lexical_resource': 0, 'grammatical_range_accuracy': 0, 'pronunciation': 0}
    crit_counts = {'fluency_coherence': 0, 'lexical_resource': 0, 'grammatical_range_accuracy': 0, 'pronunciation': 0}
    fillers = []

    for att in attempts:
        c = att.get('criterion_scores', {})
        fb = att.get('ai_feedback', {})
        if isinstance(fb, dict) and 'filler_words_detected' in fb:
            fillers.extend(fb['filler_words_detected'])
        
        for k in crit_totals:
            if k in c and isinstance(c[k], (int, float)):
                crit_totals[k] += c[k]
                crit_counts[k] += 1
            elif k in c and isinstance(c[k], dict) and 'band' in c[k]:
                crit_totals[k] += float(c[k]['band'])
                crit_counts[k] += 1

    averages = {}
    display_names = {
        'fluency_coherence': 'Fluency & Coherence',
        'lexical_resource': 'Lexical Resource',
        'grammatical_range_accuracy': 'Grammar Range & Accuracy',
        'pronunciation': 'Pronunciation'
    }
    for k in crit_totals:
        averages[display_names[k]] = round(crit_totals[k] / crit_counts[k], 1) if crit_counts[k] > 0 else 6.0
    
    bottleneck = min(averages.items(), key=lambda x: x[1])[0]

    return {
        'status': f'{len(attempts)} speaking session(s) completed',
        'criteria_averages': averages,
        'bottleneck_criterion': bottleneck,
        'filler_word_frequency': ', '.join(fillers[:4]) if fillers else 'Low (clean fluency)',
        'key_advice': f'To improve {bottleneck}, practice speaking continuously for 2 minutes without checking grammar in your head while talking.',
        'recommendation': 'Practice Part 2 Cue Card with a 1-minute structured prep note.'
    }

def generate_priorities(overall, target, module_data):
    priorities = []
    
    unassessed_modules = []
    assessed_gaps = []

    for mod, (meta, diag) in module_data.items():
        if meta.get('status') == 'not_assessed':
            unassessed_modules.append((mod, meta, diag))
        else:
            gap = target - meta['score']
            assessed_gaps.append((mod, gap, meta, diag))
    
    # If modules are unassessed, guide candidate to establish their baseline
    for mod, meta, diag in unassessed_modules:
        mod_name = mod.capitalize()
        priorities.append({
            'module': mod,
            'title': f'Establish {mod_name} Baseline (Not yet assessed)',
            'urgency': 'High',
            'description': f'Complete your first {mod_name} practice session to establish your baseline and uncover specific question-type weaknesses.',
            'action_label': f'Start {mod_name} Test',
            'target_route': mod,
            'status': 'not_assessed'
        })

    # For assessed modules, sort by largest gap to target
    assessed_gaps.sort(key=lambda x: x[1], reverse=True)
    for mod, gap, meta, diag in assessed_gaps:
        mod_name = mod.capitalize()
        score = meta['score']
        trend_note = ""
        if meta['trend'] == 'improved':
            trend_note = f" (↑ +{meta['delta']} recent improvement)"
        elif meta['trend'] == 'declined':
            trend_note = f" (↓ {meta['delta']} recent dip - needs focus)"
        
        if mod in ['writing', 'speaking']:
            bottleneck = diag.get('bottleneck_criterion', 'Grammar and Cohesion')
            priorities.append({
                'module': mod,
                'title': f'Elevate {mod_name} from Band {score} to {target}{trend_note}',
                'urgency': 'High' if gap >= 1.0 else 'Medium',
                'description': f'Your bottleneck is {bottleneck}. {diag.get("key_advice", "")}',
                'action_label': f'Practice {mod_name}',
                'target_route': mod,
                'status': 'assessed'
            })
        else:
            weakest_q = diag.get('weakest_question_type', 'Core Questions')
            priorities.append({
                'module': mod,
                'title': f'Master {mod_name} {weakest_q} (Band {score} → {target}){trend_note}',
                'urgency': 'High' if gap >= 1.0 else 'Medium',
                'description': f'Your accuracy is lowest in {weakest_q}. {diag.get("key_advice", "")}',
                'action_label': f'Start {mod_name} Drill',
                'target_route': mod,
                'status': 'assessed'
            })
            
    return priorities[:3]
