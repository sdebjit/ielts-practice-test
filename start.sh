#!/usr/bin/env bash
# Quick launch script for IELTS Gemini Prep
PORT="${1:-8080}"
echo "=========================================================="
echo " Starting IELTS Master - Powered by Gemini AI"
echo " Access URL: http://localhost:${PORT}"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if command -v python3 >/dev/null 2>&1; then
    python3 backend/server.py "$PORT"
elif command -v python >/dev/null 2>&1; then
    python backend/server.py "$PORT"
else
    echo "Error: Python 3 was not found on your system."
    exit 1
fi
