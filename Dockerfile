# Dockerfile for IELTS Master Full-Stack Platform
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# Copy application files
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
COPY data/ /app/data/
COPY start.sh /app/start.sh

# Ensure execute permission
RUN chmod +x /app/start.sh

# Expose server port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

# Start server
CMD ["python3", "backend/server.py", "8080"]
