# GitHub Copilot Code Review Instructions

You are the automated senior code reviewer for **IELTS Master** (`sdebjit/ielts-practice-test`).
When reviewing Pull Requests, evaluate changes against the following strict project standards:

---

## 1. 🛡️ Security & Zero Data Leakage (Highest Priority)
* **No Hardcoded Secrets**: Reject any commit containing API keys (e.g. `AIza...`, `AQ....`, `ghp_...`, `gho_...`), private keys (`BEGIN ... PRIVATE KEY`), passwords, or bearer tokens.
* **SQL Injection Prevention**: All database interactions with SQLite must use parameterized queries with `?` placeholders. **Never** permit string concatenation, f-strings, or raw interpolation inside SQL statements.
* **Password Hashing**: Authentication passwords must be hashed using PBKDF2-HMAC-SHA256 with a unique 16-byte random salt per user and compared using constant-time comparison (`hmac.compare_digest`).
* **Environment Protection**: Ensure database files (`data/*.db`), logs (`*.log`), and credential keys are excluded from git and ignored by `.gitignore`.

---

## 2. 🐍 Backend Standards (Python 3.10+)
* **Zero External Pip Dependencies**: The backend must run strictly using Python's standard library (`http.server`, `socketserver`, `sqlite3`, `json`, `urllib`, `hashlib`, `hmac`, `uuid`, etc.). Reject additions of external packages to maintain lightweight, zero-dependency deployment.
* **Idempotent Data Seeding**: Any schema migrations or bank additions must check for table existence (`CREATE TABLE IF NOT EXISTS`) and existing counts before inserting to avoid duplicate test records or overwriting user progress.
* **Type Safety & Error Handling**: REST endpoints in `backend/server.py` must validate JSON request bodies, return appropriate HTTP status codes (200, 400, 401, 403, 404, 500), and return error responses formatted as `{"error": "description"}`.

---

## 3. 🌐 Frontend Standards (Modular Vanilla JavaScript & Tailwind CSS)
* **Modular Structure**: New JavaScript code must be organized into logical domain modules under `frontend/js/` (e.g. `auth.js`, `reading.js`, `writing.js`, `catalog.js`, `timers.js`, `utils.js`).
* **Browser Compatibility**: Code must run natively in standard modern browsers using ES6+ without requiring a Node.js runtime or build/bundler step.
* **Syntax & Error Prevention**: All files in `frontend/js/` must pass JavaScript syntax checking (`node -c`) with zero errors.

---

## 4. 📝 IELTS Pedagogical & Rubric Accuracy
* **Raw-to-Band Scoring Accuracy**:
  * **Academic Reading**: Follows standard 40-question Cambridge scale (30/40 = Band 7.0, 35/40 = Band 8.0, 39/40 = Band 9.0).
  * **General Training Reading**: Follows stricter Cambridge GT scale (30/40 = Band 6.5, 34/40 = Band 7.5, 36/40 = Band 8.0).
* **Writing Task Separation**:
  * Academic Task 1 requires visual report structure (150 words).
  * General Training Task 1 requires letter structure (Formal, Semi-formal, Informal) addressing all 3 bullet points with appropriate opening and closing (150 words).
  * Task 2 requires discursive essay structure (250 words).
* **Listening & Speaking**: Remain common across both exam tracks.

---

## 5. 🚀 Review Output Format
Please structure your review feedback concisely:
1. **Summary of Changes**: High-level understanding of what the PR accomplishes.
2. **Security & Quality Check**: Confirm no secrets, syntax issues, or dependency violations.
3. **Actionable Suggestions**: Specific code improvements or line-level recommendations.
