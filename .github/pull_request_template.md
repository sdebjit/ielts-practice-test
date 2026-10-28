## 📋 Pull Request Summary

### 🎯 Purpose & Context
<!-- Describe the problem solved or feature added by this PR -->

---

### 🔍 Changes Made
* 

---

### 🛡️ Copilot Review & Quality Checklist
- [ ] No hardcoded secrets, API keys, or private credentials included.
- [ ] Backend runs with zero external pip dependencies (standard library Python only).
- [ ] SQLite queries are strictly parameterized (`?`).
- [ ] Modular frontend scripts in `frontend/js/` pass JavaScript syntax check (`node -c`).
- [ ] IELTS exam scoring scales (Academic vs General Training) preserved.
- [ ] Validated with GitHub Copilot Code Review.

---

### ✅ Verification & Testing
<!-- Describe how these changes were tested and verified -->
- **Syntax Check:** `python3 -m py_compile backend/*.py`
- **JS Syntax:** `for f in frontend/js/*.js frontend/app.js; do node -c "$f"; done`
- **Database / Test Bank:** `python3 -c "import sys; sys.path.append('backend'); from database import init_db; from seed_data import seed_tests; init_db(); seed_tests()"`
