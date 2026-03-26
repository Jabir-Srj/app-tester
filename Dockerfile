FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install security tools
RUN pip install --no-cache-dir \
    bandit \
    semgrep \
    pip-audit

# Copy backend code
COPY backend/ ./backend

EXPOSE 5000

CMD ["python", "backend/app.py"]
