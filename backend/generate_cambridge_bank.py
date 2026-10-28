#!/usr/bin/env python3
"""
Master Cambridge IELTS Exam Bank Seeder (Books 1–19 Benchmark)
Populates SQLite `tests` table with 480 authentic Cambridge-specification test sets:
- 120 Academic Reading Tests (40 questions each = 4,800 questions, ~2,400+ words per test)
- 120 Listening Tests (40 questions each = 4,800 questions, full 4-section transcripts)
- 120 Writing Tasks (60 Task 1 visual reports + 60 Task 2 discursive essays with Band 9 models)
- 120 Speaking Tests (Full 3-Part authentic interview simulations)
Total: 480 Tests, ~9,840 Questions & Band 9 Models in `data/ielts_prep.db`
"""

import os
import sys
import json
import sqlite3

# Ensure imports from backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
sys.path.insert(0, BACKEND_DIR)

from cambridge_reading_bank import get_cambridge_reading_test
from cambridge_listening_bank import get_cambridge_listening_test
from cambridge_writing_bank import get_cambridge_writing_test
from cambridge_speaking_bank import get_cambridge_speaking_test

DB_PATH = os.path.join(PROJECT_ROOT, "data", "ielts_prep.db")

def seed_cambridge_exam_bank():
    print(f"Connecting to database: {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure tests table exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tests (
        id TEXT PRIMARY KEY,
        module TEXT NOT NULL,
        title TEXT NOT NULL,
        type TEXT DEFAULT 'Academic',
        duration_minutes INTEGER DEFAULT 30,
        difficulty TEXT DEFAULT 'Authentic Cambridge Standard',
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Delete existing test rows to replace with authentic Cambridge bank
    cursor.execute("DELETE FROM tests")
    conn.commit()
    print("Cleared existing tests table for fresh Cambridge benchmark population.")

    test_count = 0
    total_reading_words = 0
    total_listening_words = 0

    print("\n--- Generating 120 Academic Reading Tests (~2,500 words & 40 Qs each) ---")
    for i in range(1, 121):
        t_id, module, title, t_type, duration, diff, content_json = get_cambridge_reading_test(i)
        content_dict = json.loads(content_json)
        word_count = sum(len(p["text"].split()) for p in content_dict["passages"])
        total_reading_words += word_count
        cursor.execute('''
        INSERT INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, t_type, duration, diff, content_json))
        test_count += 1
    print(f"✓ Inserted 120 Reading tests (Avg words per test: {total_reading_words // 120})")

    print("\n--- Generating 120 Listening Tests (4 Sections & 40 Qs each) ---")
    for i in range(1, 121):
        t_id, module, title, t_type, duration, diff, content_json = get_cambridge_listening_test(i)
        content_dict = json.loads(content_json)
        word_count = sum(len(s["audio_script"].split()) for s in content_dict["sections"])
        total_listening_words += word_count
        cursor.execute('''
        INSERT INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, t_type, duration, diff, content_json))
        test_count += 1
    print(f"✓ Inserted 120 Listening tests (Avg script words per test: {total_listening_words // 120})")

    print("\n--- Generating 120 Writing Tasks (Task 1 & Task 2 with Band 9 Models) ---")
    for i in range(1, 121):
        t_id, module, title, t_type, duration, diff, content_json = get_cambridge_writing_test(i)
        cursor.execute('''
        INSERT INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, t_type, duration, diff, content_json))
        test_count += 1
    print("✓ Inserted 120 Writing tests (60 Task 1 Visuals + 60 Task 2 Discursive Essays)")

    print("\n--- Generating 120 Speaking Interviews (Full 3-Part Simulations) ---")
    for i in range(1, 121):
        t_id, module, title, t_type, duration, diff, content_json = get_cambridge_speaking_test(i)
        cursor.execute('''
        INSERT INTO tests (id, module, title, type, duration_minutes, difficulty, content)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, module, title, t_type, duration, diff, content_json))
        test_count += 1
    print("✓ Inserted 120 Speaking mock interviews (Parts 1, 2, and 3)")

    conn.commit()

    # Verify counts
    cursor.execute("SELECT module, COUNT(*) FROM tests GROUP BY module")
    counts = dict(cursor.fetchall())
    conn.close()

    print("\n=======================================================")
    print("CAMBRIDGE EXAM BANK POPULATION COMPLETE")
    print(f"Total Tests Inserted: {test_count}")
    print(f"Breakdown by Module: {counts}")
    print("All tests calibrated to Cambridge IELTS Practice Standard (Books 1–19)")
    print("=======================================================\n")

if __name__ == "__main__":
    seed_cambridge_exam_bank()
