import sqlite3
import json
import os
import time
import hashlib
import hmac
import secrets
import re
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ielts_prep.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =====================================================================
# PASSWORD HASHING & AUTHENTICATION UTILITIES (SECURE PBKDF2-HMAC-SHA256)
# =====================================================================

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return pwd_hash, salt

def verify_password(password, salt, stored_hash):
    if not password or not salt or not stored_hash:
        return False
    pwd_hash, _ = hash_password(password, salt)
    # Constant-time comparison to protect against timing side-channel attacks
    return hmac.compare_digest(pwd_hash, stored_hash)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def register_user(name, email, password, target_band=7.5, exam_type='Academic'):
    email = (email or '').strip().lower()
    name = (name or '').strip()
    if not email or not name or not password:
        return {'error': 'Name, email, and password are required'}
    if not EMAIL_REGEX.match(email) or len(email) > 254:
        return {'error': 'Please enter a valid email address'}
    if len(name) > 100:
        return {'error': 'Name must be 100 characters or fewer'}
    if len(password) < 6:
        return {'error': 'Password must be at least 6 characters'}
    if len(password) > 128:
        return {'error': 'Password must not exceed 128 characters'}

    conn = get_connection()
    cursor = conn.cursor()
    existing = cursor.execute('SELECT id FROM users WHERE lower(email) = ?', (email,)).fetchone()
    if existing:
        conn.close()
        return {'error': 'An account with this email already exists. Please sign in instead.'}

    pwd_hash, salt = hash_password(password)
    try:
        target_band_val = float(target_band)
        if target_band_val < 1.0 or target_band_val > 9.0:
            target_band_val = 7.5
    except (ValueError, TypeError):
        target_band_val = 7.5

    clean_exam_type = 'General Training' if exam_type == 'General Training' else 'Academic'

    cursor.execute('''
    INSERT INTO users (name, email, password_hash, salt, target_band, exam_type, gemini_model)
    VALUES (?, ?, ?, ?, ?, ?, 'gemini-3.8-flash')
    ''', (name, email, pwd_hash, salt, target_band_val, clean_exam_type))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    token = create_session(user_id)
    user_data = get_user_by_id(user_id)
    return {'success': True, 'token': token, 'user': user_data}

def login_user(email, password):
    email = (email or '').strip().lower()
    if not email or not password:
        return {'error': 'Email and password are required'}

    conn = get_connection()
    row = conn.execute('SELECT * FROM users WHERE lower(email) = ?', (email,)).fetchone()
    conn.close()
    if not row:
        return {'error': 'Invalid email or password'}

    user = dict(row)
    if not verify_password(password, user['salt'], user['password_hash']):
        return {'error': 'Invalid email or password'}

    token = create_session(user['id'])
    clean_user = get_user_by_id(user['id'])
    return {'success': True, 'token': token, 'user': clean_user}

def create_session(user_id):
    token = secrets.token_hex(32)
    conn = get_connection()
    # Clean up expired sessions periodically
    conn.execute('DELETE FROM user_sessions WHERE expires_at IS NOT NULL AND expires_at < CURRENT_TIMESTAMP')
    conn.execute('INSERT INTO user_sessions (token, user_id, expires_at) VALUES (?, ?, datetime("now", "+30 days"))', (token, user_id))
    conn.commit()
    conn.close()
    return token

def get_user_by_token(token):
    if not token or not isinstance(token, str) or len(token) != 64:
        return None
    conn = get_connection()
    row = conn.execute('''
    SELECT u.id, u.name, u.email, u.target_band, u.current_level, u.exam_date, u.exam_type, 
           u.gemini_model, u.daily_goal_minutes, u.created_at,
           (CASE WHEN u.gemini_api_key IS NOT NULL AND length(trim(u.gemini_api_key)) > 0 THEN 1 ELSE 0 END) as has_gemini_key
    FROM user_sessions s
    JOIN users u ON s.user_id = u.id
    WHERE s.token = ? AND (s.expires_at IS NULL OR s.expires_at > CURRENT_TIMESTAMP)
    ''', (token,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def delete_session(token):
    if not token:
        return
    conn = get_connection()
    conn.execute('DELETE FROM user_sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    if not user_id:
        return None
    conn = get_connection()
    row = conn.execute('''
    SELECT id, name, email, target_band, current_level, exam_date, exam_type, 
           gemini_model, daily_goal_minutes, created_at,
           (CASE WHEN gemini_api_key IS NOT NULL AND length(trim(gemini_api_key)) > 0 THEN 1 ELSE 0 END) as has_gemini_key
    FROM users WHERE id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# =====================================================================
# DATABASE SCHEMA INITIALIZATION & MIGRATIONS
# =====================================================================

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Multiuser Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        target_band REAL DEFAULT 7.5,
        current_level REAL DEFAULT 6.0,
        exam_date TEXT DEFAULT '',
        exam_type TEXT DEFAULT 'Academic',
        gemini_api_key TEXT DEFAULT '',
        gemini_model TEXT DEFAULT 'gemini-3.8-flash',
        daily_goal_minutes INTEGER DEFAULT 45,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. User Sessions Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_sessions (
        token TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )
    ''')

    # 3. Legacy settings table (kept for backward-compatibility)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        target_band REAL DEFAULT 7.5,
        current_level REAL DEFAULT 6.0,
        exam_date TEXT DEFAULT '',
        exam_type TEXT DEFAULT 'Academic',
        gemini_api_key TEXT DEFAULT '',
        gemini_model TEXT DEFAULT 'gemini-3.8-flash',
        daily_goal_minutes INTEGER DEFAULT 45,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Seed default user if users table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        legacy_key = ''
        legacy_model = 'gemini-3.8-flash'
        cursor.execute('SELECT gemini_api_key, gemini_model FROM settings WHERE id = 1')
        legacy_row = cursor.fetchone()
        if legacy_row:
            legacy_key = legacy_row[0] or ''
            legacy_model = legacy_row[1] or 'gemini-3.8-flash'

        pwd_hash, salt = hash_password('ielts123')
        cursor.execute('''
        INSERT INTO users (id, name, email, password_hash, salt, target_band, current_level, exam_type, gemini_api_key, gemini_model, daily_goal_minutes)
        VALUES (1, 'Alex Morgan', 'demo@ieltsmaster.com', ?, ?, 7.5, 6.0, 'Academic', ?, ?, 45)
        ''', (pwd_hash, salt, legacy_key, legacy_model))

    # 4. Tests catalog
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tests (
        id TEXT PRIMARY KEY,
        module TEXT NOT NULL,
        title TEXT NOT NULL,
        type TEXT DEFAULT 'Academic',
        duration_minutes INTEGER DEFAULT 30,
        difficulty TEXT DEFAULT 'Standard',
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 5. Attempts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attempts (
        id TEXT PRIMARY KEY,
        user_id INTEGER DEFAULT 1,
        test_id TEXT NOT NULL,
        module TEXT NOT NULL,
        band_score REAL NOT NULL,
        criterion_scores TEXT NOT NULL,
        user_submission TEXT NOT NULL,
        ai_feedback TEXT NOT NULL,
        time_spent_seconds INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute("PRAGMA table_info(attempts)")
    att_cols = [col[1] for col in cursor.fetchall()]
    if 'user_id' not in att_cols:
        cursor.execute("ALTER TABLE attempts ADD COLUMN user_id INTEGER DEFAULT 1")

    # 6. Vocabulary Notebook
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vocabulary_notebook (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        word_or_phrase TEXT NOT NULL,
        context TEXT DEFAULT '',
        band_level TEXT DEFAULT 'Band 8+',
        meaning TEXT DEFAULT '',
        synonyms TEXT DEFAULT '',
        module_source TEXT DEFAULT 'General',
        mastered INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute("PRAGMA table_info(vocabulary_notebook)")
    voc_cols = [col[1] for col in cursor.fetchall()]
    if 'user_id' not in voc_cols:
        cursor.execute("ALTER TABLE vocabulary_notebook ADD COLUMN user_id INTEGER DEFAULT 1")

    # 7. Study Activity Log
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        activity_date TEXT NOT NULL,
        module TEXT NOT NULL,
        minutes INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute("PRAGMA table_info(study_logs)")
    log_cols = [col[1] for col in cursor.fetchall()]
    if 'user_id' not in log_cols:
        cursor.execute("ALTER TABLE study_logs ADD COLUMN user_id INTEGER DEFAULT 1")

    conn.commit()
    conn.close()

# =====================================================================
# USER SETTINGS & PROFILE CRUD
# =====================================================================

def get_settings(user_id=1):
    conn = get_connection()
    row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not row:
        row = conn.execute('SELECT * FROM users WHERE id = 1').fetchone()
    if not row:
        row = conn.execute('SELECT * FROM settings WHERE id = 1').fetchone()
    conn.close()
    if row:
        d = dict(row)
        d.pop('password_hash', None)
        d.pop('salt', None)
        return d
    return {'target_band': 7.5, 'exam_type': 'Academic', 'gemini_model': 'gemini-3.8-flash'}

def update_settings(data, user_id=1):
    conn = get_connection()
    fields = []
    values = []
    allowed = ['name', 'target_band', 'current_level', 'exam_date', 'exam_type', 'gemini_api_key', 'gemini_model', 'daily_goal_minutes']
    for k in allowed:
        if k in data:
            fields.append(f"{k} = ?")
            values.append(data[k])

    if fields:
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        conn.execute(query, values)
        conn.commit()
    conn.close()
    return get_settings(user_id=user_id)

# =====================================================================
# TESTS CATALOG
# =====================================================================

def get_all_tests(module=None, exam_type=None):
    conn = get_connection()
    if module:
        if exam_type and module.lower() in ('reading', 'writing'):
            rows = conn.execute(
                'SELECT id, module, title, type, duration_minutes, difficulty FROM tests WHERE lower(module) = lower(?) AND lower(type) = lower(?) ORDER BY length(id), id ASC',
                (module, exam_type)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT id, module, title, type, duration_minutes, difficulty FROM tests WHERE lower(module) = lower(?) ORDER BY length(id), id ASC',
                (module,)
            ).fetchall()
    else:
        if exam_type:
            rows = conn.execute(
                'SELECT id, module, title, type, duration_minutes, difficulty FROM tests WHERE (lower(type) = lower(?) AND lower(module) IN ("reading", "writing")) OR lower(module) IN ("listening", "speaking") ORDER BY module, length(id), id ASC',
                (exam_type,)
            ).fetchall()
        else:
            rows = conn.execute('SELECT id, module, title, type, duration_minutes, difficulty FROM tests ORDER BY module, length(id), id ASC').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_random_test(module=None, exam_type=None, exclude_id=None):
    conn = get_connection()
    clauses = []
    params = []
    if module:
        clauses.append("lower(module) = lower(?)")
        params.append(module)
        if exam_type and module.lower() in ('reading', 'writing'):
            clauses.append("lower(type) = lower(?)")
            params.append(exam_type)
    else:
        if exam_type:
            clauses.append("((lower(type) = lower(?) AND lower(module) IN ('reading', 'writing')) OR lower(module) IN ('listening', 'speaking'))")
            params.append(exam_type)

    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""

    row = None
    if exclude_id:
        ex_where = (where_sql + " AND id != ?" if where_sql else " WHERE id != ?")
        row = conn.execute(f"SELECT * FROM tests {ex_where} ORDER BY RANDOM() LIMIT 1", params + [exclude_id]).fetchone()

    if not row:
        row = conn.execute(f"SELECT * FROM tests {where_sql} ORDER BY RANDOM() LIMIT 1", params).fetchone()

    conn.close()
    if row:
        d = dict(row)
        try:
            d['content'] = json.loads(d['content'])
        except Exception:
            pass
        return d
    return None

def get_test_by_id(test_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM tests WHERE id = ?', (test_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d['content'] = json.loads(d['content'])
        except Exception:
            pass
        return d
    return None

# =====================================================================
# ATTEMPTS & PRACTICE HISTORY (USER-ISOLATED)
# =====================================================================

def save_attempt(attempt_id, test_id, module, band_score, criterion_scores, user_submission, ai_feedback, time_spent_seconds=0, user_id=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO attempts (id, user_id, test_id, module, band_score, criterion_scores, user_submission, ai_feedback, time_spent_seconds, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (
        attempt_id,
        user_id,
        test_id,
        module,
        float(band_score),
        json.dumps(criterion_scores) if isinstance(criterion_scores, dict) else criterion_scores,
        json.dumps(user_submission) if isinstance(user_submission, (dict, list)) else user_submission,
        json.dumps(ai_feedback) if isinstance(ai_feedback, dict) else ai_feedback,
        int(time_spent_seconds)
    ))

    # Log study time for this specific user
    minutes = max(1, round(time_spent_seconds / 60))
    today_str = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
    INSERT INTO study_logs (user_id, activity_date, module, minutes)
    VALUES (?, ?, ?, ?)
    ''', (user_id, today_str, module, minutes))

    conn.commit()
    conn.close()

def get_recent_attempts(limit=20, module=None, user_id=1):
    conn = get_connection()
    if module:
        rows = conn.execute('''
        SELECT a.*, t.title as test_title
        FROM attempts a
        LEFT JOIN tests t ON a.test_id = t.id
        WHERE a.user_id = ? AND a.module = ?
        ORDER BY a.created_at DESC
        LIMIT ?
        ''', (user_id, module, limit)).fetchall()
    else:
        rows = conn.execute('''
        SELECT a.*, t.title as test_title
        FROM attempts a
        LEFT JOIN tests t ON a.test_id = t.id
        WHERE a.user_id = ?
        ORDER BY a.created_at DESC
        LIMIT ?
        ''', (user_id, limit)).fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        try:
            d['criterion_scores'] = json.loads(d['criterion_scores'])
        except Exception:
            pass
        try:
            d['ai_feedback'] = json.loads(d['ai_feedback'])
        except Exception:
            pass
        results.append(d)
    return results

def reset_user_attempts(user_id=1):
    conn = get_connection()
    conn.execute('DELETE FROM attempts WHERE user_id = ?', (user_id,))
    conn.execute('DELETE FROM study_logs WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True

# =====================================================================
# VOCABULARY NOTEBOOK (USER-ISOLATED)
# =====================================================================

def get_vocabulary(user_id=1):
    conn = get_connection()
    rows = conn.execute('SELECT * FROM vocabulary_notebook WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_vocabulary(word, context, band_level='Band 8+', meaning='', synonyms='', module_source='General', user_id=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO vocabulary_notebook (user_id, word_or_phrase, context, band_level, meaning, synonyms, module_source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, word, context, band_level, meaning, synonyms, module_source))
    conn.commit()
    vocab_id = cursor.lastrowid
    conn.close()
    return vocab_id

def toggle_vocabulary_mastered(vocab_id, user_id=1):
    conn = get_connection()
    conn.execute('UPDATE vocabulary_notebook SET mastered = CASE WHEN mastered = 1 THEN 0 ELSE 1 END WHERE id = ? AND user_id = ?', (vocab_id, user_id))
    conn.commit()
    conn.close()

def delete_vocabulary(vocab_id, user_id=1):
    conn = get_connection()
    conn.execute('DELETE FROM vocabulary_notebook WHERE id = ? AND user_id = ?', (vocab_id, user_id))
    conn.commit()
    conn.close()
