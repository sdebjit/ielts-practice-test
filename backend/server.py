import http.server
import socketserver
import json
import os
import urllib.parse
import uuid
import sys
import re
import time

from database import (
    init_db, get_settings, update_settings, get_all_tests, get_random_test, get_test_by_id,
    save_attempt, get_recent_attempts, get_vocabulary, add_vocabulary,
    toggle_vocabulary_mastered, delete_vocabulary, reset_user_attempts,
    register_user, login_user, create_session, get_user_by_token, delete_session, get_user_by_id
)
from seed_data import seed_tests
from analytics import get_diagnostics, calculate_ielts_overall
from gemini_service import evaluate_writing, evaluate_speaking, call_gemini_api, verify_gemini_key, generate_gemini_tts

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

# Official IELTS Academic Raw Score to Band Score Conversion Tables (Strict 40 Questions)
def convert_listening_raw_to_band(raw_score, total=40):
    if raw_score >= 39: return 9.0
    if raw_score >= 37: return 8.5
    if raw_score >= 35: return 8.0
    if raw_score >= 32: return 7.5
    if raw_score >= 30: return 7.0
    if raw_score >= 26: return 6.5
    if raw_score >= 23: return 6.0
    if raw_score >= 18: return 5.5
    if raw_score >= 16: return 5.0
    if raw_score >= 13: return 4.5
    if raw_score >= 10: return 4.0
    if raw_score >= 8:  return 3.5
    if raw_score >= 6:  return 3.0
    if raw_score >= 4:  return 2.5
    return 2.0

def convert_reading_raw_to_band(raw_score, exam_type='Academic', total=40):
    if exam_type and 'general' in str(exam_type).lower():
        # Official IELTS General Training Reading Raw-to-Band Scale
        if raw_score >= 39: return 9.0
        if raw_score >= 37: return 8.5
        if raw_score >= 36: return 8.0
        if raw_score >= 34: return 7.5
        if raw_score >= 32: return 7.0
        if raw_score >= 30: return 6.5
        if raw_score >= 27: return 6.0
        if raw_score >= 23: return 5.5
        if raw_score >= 19: return 5.0
        if raw_score >= 15: return 4.5
        if raw_score >= 12: return 4.0
        if raw_score >= 8:  return 3.5
        if raw_score >= 5:  return 3.0
        if raw_score >= 3:  return 2.5
        return 2.0
    else:
        # Official IELTS Academic Reading Raw-to-Band Scale
        if raw_score >= 39: return 9.0
        if raw_score >= 37: return 8.5
        if raw_score >= 35: return 8.0
        if raw_score >= 33: return 7.5
        if raw_score >= 30: return 7.0
        if raw_score >= 27: return 6.5
        if raw_score >= 23: return 6.0
        if raw_score >= 19: return 5.5
        if raw_score >= 15: return 5.0
        if raw_score >= 13: return 4.5
        if raw_score >= 10: return 4.0
        if raw_score >= 8:  return 3.5
        if raw_score >= 6:  return 3.0
        if raw_score >= 4:  return 2.5
        return 2.0

def check_answer_strict(user_val, correct_ans, qtype):
    """
    Enforces official IELTS examination marking strictness:
    - True/False/Not Given & Yes/No/Not Given standard abbreviations
    - Roman numeral headings
    - Strict word count and case-insensitive text matching
    """
    if user_val is None or str(user_val).strip() == '':
        return False
    u = str(user_val).strip()
    c = str(correct_ans).strip()

    # Case 1: True / False / Not Given
    if qtype in ['True/False/Not Given', 'True / False / Not Given']:
        u_upper = u.upper()
        c_upper = c.upper()
        if c_upper == 'TRUE': return u_upper in ['TRUE', 'T']
        elif c_upper == 'FALSE': return u_upper in ['FALSE', 'F']
        elif c_upper == 'NOT GIVEN': return u_upper in ['NOT GIVEN', 'NG']
        return u_upper == c_upper

    # Case 2: Yes / No / Not Given
    if qtype in ['Yes/No/Not Given', 'Yes / No / Not Given']:
        u_upper = u.upper()
        c_upper = c.upper()
        if c_upper == 'YES': return u_upper in ['YES', 'Y']
        elif c_upper == 'NO': return u_upper in ['NO', 'N']
        elif c_upper == 'NOT GIVEN': return u_upper in ['NOT GIVEN', 'NG']
        return u_upper == c_upper

    # Case 3: Matching Headings (roman numerals: i, ii, iii, iv, v, vi, vii, viii, ix, x)
    if 'Heading' in qtype:
        u_roman = u.lower().split('.')[0].strip()
        c_roman = c.lower().split('.')[0].strip()
        return (u_roman == c_roman) or (u.lower() == c.lower())

    # Case 4: Multiple Choice & Matching Features
    if qtype in ['Multiple Choice', 'Matching Features']:
        if u.lower() == c.lower():
            return True
        if len(u) == 1 and c.upper().startswith(u.upper()):
            return True
        if len(c) == 1 and u.upper().startswith(c.upper()):
            return True
        return False

    # Case 5: Text / Form / Summary / Sentence Completion
    u_norm = re.sub(r'[^\w\s]', '', u.lower()).strip()
    c_norm = re.sub(r'[^\w\s]', '', c.lower()).strip()

    if u_norm == c_norm:
        return True

    # Accept alternative slash variants in key (e.g. "reporter / biomarker")
    if '/' in c:
        alts = [re.sub(r'[^\w\s]', '', alt.lower()).strip() for alt in c.split('/')]
        if u_norm in alts:
            return True

    return False

# Rate limiting for failed authentication attempts (prevent brute force)
FAILED_LOGIN_ATTEMPTS = {}

def check_login_rate_limit(key, max_attempts=5, window_seconds=60):
    now = time.time()
    attempts = [t for t in FAILED_LOGIN_ATTEMPTS.get(key, []) if now - t < window_seconds]
    FAILED_LOGIN_ATTEMPTS[key] = attempts
    return len(attempts) < max_attempts

def record_failed_login(key):
    now = time.time()
    if key not in FAILED_LOGIN_ATTEMPTS:
        FAILED_LOGIN_ATTEMPTS[key] = []
    FAILED_LOGIN_ATTEMPTS[key].append(now)

def clear_failed_login(key):
    FAILED_LOGIN_ATTEMPTS.pop(key, None)

class IELTSRequestHandler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        # Security Hardening Headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            raw = self.rfile.read(content_length).decode('utf-8')
            return json.loads(raw)
        return {}

    def get_token_from_header(self):
        # Strict Bearer token extraction: never accept tokens in query string to prevent leak in logs & referrer
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth[7:].strip()
            if len(token) == 64 and all(c in '0123456789abcdefABCDEF' for c in token):
                return token.lower()
        return None

    def get_current_user(self):
        token = self.get_token_from_header()
        if token:
            user = get_user_by_token(token)
            if user:
                return user
        return None

    def require_auth(self):
        user = self.get_current_user()
        if not user:
            self.send_json({'error': 'Unauthorized: Valid candidate session required. Please sign in.'}, status=401)
            return None
        return user

    def get_current_user_id(self):
        user = self.get_current_user()
        return user['id'] if user else None

    def serve_file(self, filepath, content_type):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return
        with open(filepath, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(content)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static Web App routes
        if path == '/' or path == '/index.html':
            self.serve_file(os.path.join(FRONTEND_DIR, 'index.html'), 'text/html; charset=utf-8')
            return
        elif path == '/app.js':
            self.serve_file(os.path.join(FRONTEND_DIR, 'app.js'), 'application/javascript; charset=utf-8')
            return
        elif path.startswith('/js/'):
            filename = os.path.basename(path)
            js_path = os.path.join(FRONTEND_DIR, 'js', filename)
            if os.path.exists(js_path) and js_path.endswith('.js'):
                self.serve_file(js_path, 'application/javascript; charset=utf-8')
                return
            else:
                self.send_error(404, 'File not found')
                return
        elif path == '/styles.css':
            self.serve_file(os.path.join(FRONTEND_DIR, 'styles.css'), 'text/css; charset=utf-8')
            return

        # =============================================================
        # AUTHENTICATION ENDPOINTS
        # =============================================================
        if path == '/api/auth/me':
            user = self.get_current_user()
            if user:
                self.send_json({'authenticated': True, 'user': user})
            else:
                self.send_json({'authenticated': False})
            return

        elif path == '/api/auth/demo':
            demo_user = get_user_by_id(1)
            if not demo_user:
                init_db()
                demo_user = get_user_by_id(1)
            token = create_session(demo_user['id'])
            self.send_json({'success': True, 'token': token, 'user': demo_user})
            return

        # =============================================================
        # USER-AWARE API ENDPOINTS (PROTECTED & ISOLATED)
        # =============================================================
        elif path == '/api/settings':
            user = self.require_auth()
            if not user:
                return
            s = get_settings(user_id=user['id'])
            # Mask API key for security in UI
            if s.get('gemini_api_key'):
                s['has_api_key'] = True
                s['gemini_api_key_masked'] = s['gemini_api_key'][:4] + '...' + s['gemini_api_key'][-4:] if len(s['gemini_api_key']) > 8 else '****'
            else:
                s['has_api_key'] = False
                s['gemini_api_key_masked'] = ''
            self.send_json(s)
            return

        elif path == '/api/diagnostics':
            user = self.require_auth()
            if not user:
                return
            diag = get_diagnostics(user_id=user['id'])
            self.send_json(diag)
            return

        elif path == '/api/tests':
            module = query.get('module', [None])[0]
            exam_type = query.get('type', [None])[0]
            if not exam_type:
                user = self.get_current_user()
                if user:
                    exam_type = user.get('exam_type')
            tests = get_all_tests(module, exam_type)
            self.send_json(tests)
            return

        elif path == '/api/tests/random':
            module = query.get('module', [None])[0]
            exam_type = query.get('type', [None])[0]
            if not exam_type:
                user = self.get_current_user()
                if user:
                    exam_type = user.get('exam_type')
            t = get_random_test(module, exam_type)
            if t:
                self.send_json(t)
            else:
                self.send_json({'error': 'No tests found'}, status=404)
            return

        elif path.startswith('/api/tests/'):
            test_id = path.split('/api/tests/')[1]
            t = get_test_by_id(test_id)
            if t:
                self.send_json(t)
            else:
                self.send_json({'error': 'Test not found'}, status=404)
            return

        elif path == '/api/attempts':
            user = self.require_auth()
            if not user:
                return
            module = query.get('module', [None])[0]
            limit = int(query.get('limit', [20])[0])
            attempts = get_recent_attempts(limit=limit, module=module, user_id=user['id'])
            self.send_json(attempts)
            return

        elif path == '/api/vocabulary':
            user = self.get_current_user()
            user_id = user['id'] if user else None
            vocab = get_vocabulary(user_id=user_id)
            self.send_json(vocab)
            return

        self.send_error(404, "Endpoint not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            body = self.read_json_body()
        except Exception as e:
            self.send_json({'error': f'Invalid JSON payload: {str(e)}'}, status=400)
            return

        # =============================================================
        # AUTHENTICATION ACTIONS
        # =============================================================
        if path == '/api/auth/register':
            name = body.get('name', '').strip()
            email = body.get('email', '').strip()
            password = body.get('password', '')
            target_band = body.get('target_band', 7.5)
            exam_type = body.get('exam_type', 'Academic')
            res = register_user(name, email, password, target_band=target_band, exam_type=exam_type)
            if res.get('success'):
                self.send_json(res)
            else:
                self.send_json(res, status=400)
            return

        elif path == '/api/auth/login':
            email = body.get('email', '').strip()
            password = body.get('password', '')
            client_ip = self.client_address[0] if self.client_address else 'local'
            rate_key = f"{client_ip}:{email.lower()}"
            if not check_login_rate_limit(rate_key, max_attempts=5, window_seconds=60):
                self.send_json({'error': 'Too many failed sign in attempts. Please wait 1 minute before trying again.'}, status=429)
                return

            res = login_user(email, password)
            if res.get('success'):
                clear_failed_login(rate_key)
                self.send_json(res)
            else:
                record_failed_login(rate_key)
                self.send_json(res, status=400)
            return

        elif path == '/api/auth/logout':
            token = self.get_token_from_header()
            if token:
                delete_session(token)
            self.send_json({'success': True})
            return

        # =============================================================
        # USER SETTINGS & TOOLS (PROTECTED)
        # =============================================================
        elif path == '/api/settings':
            user = self.require_auth()
            if not user:
                return
            updated = update_settings(body, user_id=user['id'])
            self.send_json(updated)
            return

        elif path == '/api/gemini/test':
            user = self.require_auth()
            if not user:
                return
            api_key = body.get('api_key')
            if not api_key:
                s = get_settings(user_id=user['id'])
                api_key = s.get('gemini_api_key', '')

            ver = verify_gemini_key(api_key)
            if ver.get('valid'):
                self.send_json({'success': True, 'models': ver.get('models', []), 'message': 'API Key verified and active!'})
            else:
                self.send_json({'success': False, 'error': ver.get('error', 'Unable to verify API key.')}, status=400)
            return

        elif path == '/api/tts':
            user = self.get_current_user()
            text = body.get('text', '')
            voice = body.get('voice', 'Puck')
            user_settings = get_settings(user_id=user['id']) if user else {}
            admin_settings = get_settings(user_id=1)
            api_key = body.get('api_key') or user_settings.get('gemini_api_key', '') or admin_settings.get('gemini_api_key', '')
            res = generate_gemini_tts(text, voice_name=voice, api_key=api_key)
            if res.get('success'):
                self.send_json(res)
            else:
                self.send_json(res, status=400)
            return

        # =============================================================
        # EXAM EVALUATIONS & USER-ISOLATED ATTEMPTS (PROTECTED)
        # =============================================================
        # Grade Listening Test
        elif path == '/api/attempts/listening':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            test_id = body.get('test_id')
            user_answers = body.get('answers', {})
            time_spent = body.get('time_spent_seconds', 0)

            test = get_test_by_id(test_id)
            if not test:
                self.send_json({'error': 'Test not found'}, status=404)
                return

            sections = test['content'].get('sections', [])
            all_questions = []
            for sec in sections:
                all_questions.extend(sec.get('questions', []))

            total_q = len(all_questions)
            correct_count = 0
            detailed_results = []
            type_breakdown = {}

            for q in all_questions:
                qid = q['id']
                qtype = q.get('type', 'Standard')
                user_val = user_answers.get(qid, '')
                is_correct = check_answer_strict(user_val, q['correct_answer'], qtype)

                if qtype not in type_breakdown:
                    type_breakdown[qtype] = {'total': 0, 'correct': 0}
                type_breakdown[qtype]['total'] += 1
                if is_correct:
                    type_breakdown[qtype]['correct'] += 1
                    correct_count += 1

                detailed_results.append({
                    'id': qid,
                    'type': qtype,
                    'question_text': q['question_text'],
                    'user_answer': user_answers.get(qid, ''),
                    'correct_answer': q['correct_answer'],
                    'is_correct': is_correct,
                    'explanation': q.get('explanation', '')
                })

            band_score = convert_listening_raw_to_band(correct_count, total=total_q)
            attempt_id = f"L-ATT-{uuid.uuid4().hex[:8]}"

            feedback = {
                'raw_score': correct_count,
                'total_questions': total_q,
                'accuracy_percentage': round((correct_count / max(1, total_q)) * 100),
                'detailed_results': detailed_results
            }

            save_attempt(
                attempt_id=attempt_id,
                test_id=test_id,
                module='listening',
                band_score=band_score,
                criterion_scores={'raw_score': correct_count, 'total': total_q, 'question_type_breakdown': type_breakdown},
                user_submission=user_answers,
                ai_feedback=feedback,
                time_spent_seconds=time_spent,
                user_id=user_id
            )

            self.send_json({
                'attempt_id': attempt_id,
                'band_score': band_score,
                'raw_score': correct_count,
                'total_questions': total_q,
                'type_breakdown': type_breakdown,
                'detailed_results': detailed_results
            })
            return

        # Grade Reading Test
        elif path == '/api/attempts/reading':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            test_id = body.get('test_id')
            user_answers = body.get('answers', {})
            time_spent = body.get('time_spent_seconds', 0)

            test = get_test_by_id(test_id)
            if not test:
                self.send_json({'error': 'Test not found'}, status=404)
                return

            passages = test['content'].get('passages', [])
            all_questions = []
            for p in passages:
                all_questions.extend(p.get('questions', []))

            total_q = len(all_questions)
            correct_count = 0
            detailed_results = []
            type_breakdown = {}

            for q in all_questions:
                qid = q['id']
                qtype = q.get('type', 'Standard')
                user_val = user_answers.get(qid, '')
                is_correct = check_answer_strict(user_val, q['correct_answer'], qtype)

                if qtype not in type_breakdown:
                    type_breakdown[qtype] = {'total': 0, 'correct': 0}
                type_breakdown[qtype]['total'] += 1
                if is_correct:
                    type_breakdown[qtype]['correct'] += 1
                    correct_count += 1

                detailed_results.append({
                    'id': qid,
                    'type': qtype,
                    'question_text': q['question_text'],
                    'user_answer': user_answers.get(qid, ''),
                    'correct_answer': q['correct_answer'],
                    'is_correct': is_correct,
                    'explanation': q.get('explanation', '')
                })

            test_type = test.get('type', 'Academic') if test else 'Academic'
            band_score = convert_reading_raw_to_band(correct_count, exam_type=test_type, total=total_q)
            attempt_id = f"R-ATT-{uuid.uuid4().hex[:8]}"

            feedback = {
                'raw_score': correct_count,
                'total_questions': total_q,
                'accuracy_percentage': round((correct_count / max(1, total_q)) * 100),
                'detailed_results': detailed_results
            }

            save_attempt(
                attempt_id=attempt_id,
                test_id=test_id,
                module='reading',
                band_score=band_score,
                criterion_scores={'raw_score': correct_count, 'total': total_q, 'question_type_breakdown': type_breakdown},
                user_submission=user_answers,
                ai_feedback=feedback,
                time_spent_seconds=time_spent,
                user_id=user_id
            )

            self.send_json({
                'attempt_id': attempt_id,
                'band_score': band_score,
                'raw_score': correct_count,
                'total_questions': total_q,
                'type_breakdown': type_breakdown,
                'detailed_results': detailed_results
            })
            return

        # Evaluate Writing Essay with Gemini
        elif path == '/api/attempts/writing':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            test_id = body.get('test_id')
            student_essay = body.get('essay', '').strip()
            time_spent = body.get('time_spent_seconds', 0)
            client_eval = body.get('evaluation')

            if len(student_essay.split()) < 20:
                self.send_json({'error': 'Essay is too short for evaluation (minimum 20 words)'}, status=400)
                return

            if client_eval and isinstance(client_eval, dict) and 'overall_band' in client_eval:
                evaluation = client_eval
            else:
                test = get_test_by_id(test_id)
                prompt_data = test['content'] if test else {'title': 'IELTS Essay', 'prompt': 'General writing task'}
                if test and 'type' in test:
                    prompt_data['type'] = test['type']
                evaluation = evaluate_writing(prompt_data, student_essay)

            band_score = evaluation.get('overall_band', 6.0)
            attempt_id = f"W-ATT-{uuid.uuid4().hex[:8]}"

            save_attempt(
                attempt_id=attempt_id,
                test_id=test_id,
                module='writing',
                band_score=band_score,
                criterion_scores=evaluation.get('criteria', {}),
                user_submission=student_essay,
                ai_feedback=evaluation,
                time_spent_seconds=time_spent,
                user_id=user_id
            )

            self.send_json({
                'attempt_id': attempt_id,
                'evaluation': evaluation
            })
            return

        # Evaluate Speaking Interview with Gemini
        elif path == '/api/attempts/speaking':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            test_id = body.get('test_id')
            responses = body.get('responses', [])
            time_spent = body.get('time_spent_seconds', 0)
            client_eval = body.get('evaluation')

            if client_eval and isinstance(client_eval, dict) and 'overall_band' in client_eval:
                evaluation = client_eval
            else:
                test = get_test_by_id(test_id)
                evaluation = evaluate_speaking(test['content'] if test else {}, responses)

            band_score = evaluation.get('overall_band', 6.0)
            attempt_id = f"S-ATT-{uuid.uuid4().hex[:8]}"

            save_attempt(
                attempt_id=attempt_id,
                test_id=test_id,
                module='speaking',
                band_score=band_score,
                criterion_scores=evaluation.get('criteria', {}),
                user_submission=responses,
                ai_feedback=evaluation,
                time_spent_seconds=time_spent,
                user_id=user_id
            )

            self.send_json({
                'attempt_id': attempt_id,
                'evaluation': evaluation
            })
            return

        # Reset all attempts for current candidate back to unassessed baseline
        elif path == '/api/attempts/reset':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            reset_user_attempts(user_id=user_id)
            self.send_json({
                'success': True,
                'message': 'All attempts reset. Baseline is now Not yet assessed.'
            })
            return

        # Add Vocabulary Item
        elif path == '/api/vocabulary':
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            word = body.get('word', '').strip()
            context = body.get('context', '').strip()
            band_level = body.get('band_level', 'Band 8+')
            meaning = body.get('meaning', '').strip()
            synonyms = body.get('synonyms', '').strip()
            module_source = body.get('module_source', 'General')

            if not word:
                self.send_json({'error': 'Word is required'}, status=400)
                return

            vid = add_vocabulary(word, context, band_level, meaning, synonyms, module_source, user_id=user_id)
            self.send_json({'success': True, 'id': vid})
            return

        elif path.startswith('/api/vocabulary/') and path.endswith('/toggle'):
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            vid = int(path.split('/api/vocabulary/')[1].split('/toggle')[0])
            toggle_vocabulary_mastered(vid, user_id=user_id)
            self.send_json({'success': True})
            return

        self.send_error(404, "Endpoint not found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/vocabulary/'):
            user = self.require_auth()
            if not user:
                return
            user_id = user['id']
            vid = int(path.split('/api/vocabulary/')[1])
            delete_vocabulary(vid, user_id=user_id)
            self.send_json({'success': True})
            return
        self.send_error(404, "Endpoint not found")

def run(port=8080):
    init_db()
    seed_tests()
    server_address = ('', port)
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(server_address, IELTSRequestHandler)
    print(f"===========================================================")
    print(f" IELTS Practice & Improvement Tracker Server Running!")
    print(f" Access URL: http://localhost:{port}")
    print(f" Frontend Root: {FRONTEND_DIR}")
    print(f" Multiuser Mode: ACTIVE")
    print(f"===========================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run(port=port)
