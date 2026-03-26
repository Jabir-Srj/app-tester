# Quick Start Guide - Automated App Tester

## 🚀 5-Minute Setup

### Option 1: Local Development (Recommended for Testing)

```bash
# 1. Navigate to project
cd C:\Users\Jabir\Projects\app-tester

# 2. Setup Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Backend runs on: http://localhost:5000
```

In a new terminal:
```bash
# 3. Setup Frontend
cd frontend
npm install
npm run dev

# Frontend runs on: http://localhost:5173
```

### Option 2: Docker (One Command)

```bash
cd C:\Users\Jabir\Projects\app-tester
docker-compose up
```

Access at:
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

---

## 📝 First Scan

### 1. Create a Test File

Create a vulnerable Python file (`test.py`):
```python
import os
import hashlib
import random

# Vulnerable 1: SQL Injection
user_id = input("Enter ID: ")
query = "SELECT * FROM users WHERE id = " + user_id

# Vulnerable 2: Hardcoded API Key
api_key = "sk_test_1234567890abcdef"

# Vulnerable 3: Weak Cryptography
password = "mypassword"
hashed = hashlib.md5(password.encode()).hexdigest()

# Vulnerable 4: Insecure Random
token = random.randint(100000, 999999)
```

### 2. Create ZIP File

Windows:
```bash
cd C:\Users\Jabir\Projects\app-tester
# Create folder with test files
mkdir test_code
copy test.py test_code\
# Right-click test_code → Send to → Compressed folder
# Or use: powershell -c "Compress-Archive -Path test_code -DestinationPath test_code.zip"
```

### 3. Upload and Scan

1. Go to http://localhost:5173
2. Click "Drop your file here or click to upload"
3. Select `test_code.zip`
4. Select language: `Python`
5. Click "Start Scan"

### 4. View Results

Results appear in real-time:
- **Critical Issues:** 1 (Hardcoded API key)
- **High Issues:** 2 (SQL Injection, Weak Crypto)
- **Total:** 4 vulnerabilities

---

## 🧪 Testing the API

### Start a Scan via API

```bash
# On Windows, create test.zip first
# Then:
curl -X POST http://localhost:5000/api/scan `
  -F "file=@test_code.zip" `
  -F "language=python" `
  -F "include_dependencies=true" `
  -F "include_secrets=true"

# Response:
# {
#   "scan_id": "abc-123-def",
#   "status": "scanning",
#   "message": "Scan started"
# }
```

### Get Results

```bash
curl http://localhost:5000/api/scan/abc-123-def/results

# Response shows all vulnerabilities, dependencies, secrets
```

### Download Report

```bash
# JSON Report
curl http://localhost:5000/api/scan/abc-123-def/report?format=json > report.json

# HTML Report
curl http://localhost:5000/api/scan/abc-123-def/report?format=html > report.html
```

---

## 📊 What Gets Scanned

### Python ✅
- SQL Injection patterns
- eval/exec/dangerous functions
- Insecure random
- Weak cryptography (MD5, SHA1, ECB)
- **Hardcoded secrets:**
  - API Keys
  - AWS Keys (AKIA...)
  - Private Keys
  - Database URLs
  - Passwords
  - Tokens
- Insecure imports
- File path issues

### Dependencies ✅
- Known CVEs
- Outdated packages
- Vulnerable versions
- (Uses pip-audit for Python)

### Secrets ✅
- API Keys
- AWS Credentials
- GitHub Tokens
- Slack Tokens
- Database URLs
- Private Keys

### Next (To Implement)
- JavaScript/TypeScript
- Java
- C#
- Go
- Ruby

---

## 🔧 Configuration

### Backend Settings
Edit `backend/app.py` Config class:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_tester.db'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'zip', 'tar', 'gz', 'tar.gz'}
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
```

### Environment Variables
Create `.env` in project root (for future API keys):
```
SNYK_API_TOKEN=your_token
GITHUB_TOKEN=your_token
NVD_API_KEY=your_key
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 5000 (backend)
lsof -ti :5000 | xargs kill -9

# Kill process on port 5173 (frontend)
lsof -ti :5173 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### File Upload Fails

- File must be ZIP/TAR format
- Max size: 100MB
- Ensure `uploads/` folder exists

### No Results Appearing

1. Check backend logs (should show scan progress)
2. Ensure frontend is hitting correct API URL (http://localhost:5000)
3. Check browser console for errors

### Python Dependencies Missing

```bash
cd backend
pip install -r requirements.txt

# Also install security tools:
pip install bandit semgrep pip-audit
```

---

## 📈 Next: Expanding the Project

### Add JavaScript Support

1. Create `backend/scanners/js_scanner.py`
2. Implement similar pattern detection
3. Update `app.py` to call JS scanner
4. Update frontend dropdown with JavaScript option

### Add GitHub Integration

1. Get GitHub API token
2. Create `backend/api_integrations/github_integration.py`
3. Add endpoint to scan repos directly
4. Update frontend with GitHub URL input

### Generate PDF Reports

1. Install `pip install reportlab`
2. Create `backend/utils/pdf_generator.py`
3. Update report endpoint to generate PDFs

---

## 💡 Pro Tips

1. **Test with real code:** Upload your own projects for scanning
2. **Check remediation:** Each finding includes fix suggestions
3. **Compare scans:** Keep track of scan history to see improvements
4. **Batch scanning:** Future version will support multiple files
5. **CI/CD integration:** Use API for GitHub Actions, GitLab CI, etc.

---

## 📞 Support

- **Docs:** See README.md and PROJECT_SUMMARY.md
- **Issues:** Create GitHub issue
- **Questions:** Check code comments

---

**Happy Scanning! 🔐**

