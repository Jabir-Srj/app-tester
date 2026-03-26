# Automated App Tester - Project Summary

**Project Location:** `C:\Users\Jabir\Projects\app-tester\`  
**Status:** v1.0 Foundation Complete  
**Last Updated:** 2026-03-26

## 📋 Project Overview

A comprehensive full-stack web application for automated security testing of source code. Detects vulnerabilities, insecure dependencies, and hardcoded secrets across multiple programming languages.

## 🏗️ Architecture

### Backend (Flask)
- **Location:** `backend/app.py`
- **Database:** SQLite with SQLAlchemy ORM
- **Scanners:**
  - Python security scanner (AST + pattern matching)
  - Dependency vulnerability scanner
  - Secret/credential detector
  - (JS, Java, Go scanners ready to implement)

### Frontend (React)
- **Framework:** React 18 + TypeScript + Tailwind CSS
- **Build:** Vite
- **Pages:**
  - Upload & Scan interface
  - Real-time results dashboard
  - Vulnerability details
  - Report generation

### Containerization
- Docker setup for easy deployment
- docker-compose for local development

## 📁 Project Structure

```
app-tester/
├── README.md                          # Project documentation
├── docker-compose.yml                 # Docker composition
├── Dockerfile                         # Backend Docker image
├── .gitignore                         # Git ignore rules
│
├── backend/
│   ├── app.py                         # ⭐ Flask main app (14.5 KB)
│   ├── config.py                      # Configuration (to create)
│   ├── models.py                      # Database schemas (in app.py)
│   ├── requirements.txt                # Python dependencies ✅
│   │
│   ├── scanners/
│   │   ├── __init__.py
│   │   ├── python_scanner.py          # ⭐ Python security scanner (10.7 KB)
│   │   ├── dependency_scanner.py      # ⭐ Dependency & secret scanner (7 KB)
│   │   ├── js_scanner.py              # (To implement)
│   │   ├── java_scanner.py            # (To implement)
│   │   └── custom_rules.py            # (To implement)
│   │
│   ├── api_integrations/
│   │   ├── snyk_integration.py        # (To implement)
│   │   ├── nvd_integration.py         # (To implement)
│   │   └── github_integration.py      # (To implement)
│   │
│   ├── uploads/                       # Uploaded files (auto-created)
│   └── instance/
│       └── app_tester.db              # SQLite database (auto-created)
│
├── frontend/
│   ├── package.json                   # ✅ NPM dependencies
│   ├── vite.config.ts                 # (To create)
│   ├── tsconfig.json                  # (To create)
│   │
│   ├── src/
│   │   ├── App.tsx                    # ⭐ Main React app (8 KB)
│   │   ├── main.tsx                   # (To create)
│   │   │
│   │   ├── components/
│   │   │   ├── FileUpload.tsx         # (To extract from App)
│   │   │   ├── ScanProgress.tsx       # (To implement)
│   │   │   ├── VulnerabilityList.tsx  # (To implement)
│   │   │   ├── ReportViewer.tsx       # (To implement)
│   │   │   └── Dashboard.tsx          # (To implement)
│   │   │
│   │   ├── pages/
│   │   │   ├── HomePage.tsx           # (To implement)
│   │   │   ├── ScanPage.tsx           # (To implement)
│   │   │   └── HistoryPage.tsx        # (To implement)
│   │   │
│   │   ├── services/
│   │   │   └── api.ts                 # API client (To create)
│   │   │
│   │   └── types.ts                   # TypeScript types (To create)
│   │
│   └── public/                        # Static assets
```

## ✅ Completed Components

### Backend
- ✅ Flask app with CORS support
- ✅ SQLAlchemy database models (Scan, Vulnerability, Dependency, Secret)
- ✅ REST API endpoints:
  - POST /api/scan — Start scan
  - GET /api/scan/{id} — Get scan status
  - GET /api/scan/{id}/results — Get results
  - GET /api/scans — List all scans
  - GET /api/scan/{id}/report — Download report
- ✅ File upload handling
- ✅ Background scanning with threading
- ✅ HTML report generation

### Scanners
- ✅ **PythonScanner:**
  - SQL Injection detection
  - Eval/exec/dangerous function detection
  - Insecure random usage
  - Secret detection (API keys, passwords, tokens, AWS keys, etc.)
  - Weak cryptography detection
  - Hardcoded file paths
  - AST parsing + regex patterns

- ✅ **DependencyScanner:**
  - pip-audit integration (Python)
  - npm audit integration (JavaScript)
  - OWASP Dependency-Check (Java)
  - Secret scanning with 8+ patterns

### Frontend
- ✅ React component with TypeScript
- ✅ File upload interface
- ✅ Real-time scan progress polling
- ✅ Results dashboard with severity breakdown
- ✅ Vulnerability list with filtering
- ✅ Tailwind CSS styling

### Configuration
- ✅ requirements.txt with all dependencies
- ✅ package.json with React/TypeScript setup
- ✅ Dockerfile for backend
- ✅ docker-compose.yml for local development

## 🚀 Getting Started

### Local Development

**1. Install Backend Dependencies**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Install Frontend Dependencies**
```bash
cd frontend
npm install
```

**3. Run Backend**
```bash
cd backend
python app.py
# Runs on http://localhost:5000
```

**4. Run Frontend**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

### Docker

```bash
docker-compose up
# Backend: http://localhost:5000
# Frontend: http://localhost:3000
```

## 🔍 API Usage Examples

### Start a Scan
```bash
curl -X POST http://localhost:5000/api/scan \
  -F "file=@myapp.zip" \
  -F "language=python" \
  -F "include_dependencies=true" \
  -F "include_secrets=true"

Response:
{
  "scan_id": "abc123...",
  "status": "scanning",
  "message": "Scan started"
}
```

### Get Scan Results
```bash
curl http://localhost:5000/api/scan/abc123/results

Response:
{
  "scan": { ... },
  "vulnerabilities": [ ... ],
  "dependencies": [ ... ],
  "secrets": [ ... ],
  "summary": { ... }
}
```

### Download Report
```bash
# JSON
curl http://localhost:5000/api/scan/abc123/report?format=json

# HTML
curl http://localhost:5000/api/scan/abc123/report?format=html

# PDF (not yet implemented)
curl http://localhost:5000/api/scan/abc123/report?format=pdf
```

## 🔐 Vulnerability Types Detected

### Python (Fully Implemented)
- ✅ SQL Injection
- ✅ Code Execution (eval/exec)
- ✅ Insecure Random
- ✅ Weak Cryptography (MD5, SHA1, ECB)
- ✅ Hardcoded Secrets (API keys, passwords, tokens)
- ✅ Hardcoded File Paths

### Dependencies (Fully Implemented)
- ✅ Known CVEs in packages
- ✅ Outdated dependencies
- ✅ Deprecated packages
- ✅ Vulnerable versions

### Secrets (Fully Implemented)
- ✅ API Keys (generic, AWS, GitHub, Slack)
- ✅ Private Keys
- ✅ Database URLs
- ✅ Passwords
- ✅ Tokens

## 📊 Severity Levels

- **Critical:** Immediate exploitation risk (RCE, auth bypass, secrets)
- **High:** Significant security impact (SQL injection, XSS, weak crypto)
- **Medium:** Moderate risk (outdated deps, CSRF, data exposure)
- **Low:** Minimal impact (best practices, info disclosure)
- **Info:** Informational findings only

## 🎯 Next Steps (TODO)

### Immediate (High Priority)
- [ ] Implement JavaScript/TypeScript scanner
- [ ] Implement Java scanner
- [ ] Implement Go scanner
- [ ] Add PDF report generation
- [ ] Add GitHub repository integration
- [ ] Add Snyk API integration
- [ ] Add NVD (CVE database) API integration

### Medium Priority
- [ ] Implement scan comparison
- [ ] Add scan history/trends
- [ ] Implement scheduled scans
- [ ] Add email notifications
- [ ] Add CI/CD pipeline integration
- [ ] Implement user authentication

### Future (v2.0)
- [ ] Build CLI tool
- [ ] Add team collaboration
- [ ] Build mobile app
- [ ] Add SAST/DAST hybrid analysis
- [ ] Build browser extension

## 📚 Technology Stack

### Backend
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- Bandit 1.7.5
- Semgrep 1.45.0
- pip-audit 2.6.1

### Frontend
- React 18.2.0
- TypeScript 5.2.2
- Tailwind CSS 3.3.6
- Vite 5.0.0
- Axios 1.6.0

### DevOps
- Docker
- Docker Compose
- SQLite 3

## 📋 Database Schema

### Scan
- id (UUID)
- filename (string)
- language (string)
- status (enum: pending, scanning, completed, failed)
- progress (0-100)
- created_at (timestamp)
- completed_at (timestamp)
- error_message (text)

### Vulnerability
- id (UUID)
- scan_id (FK)
- type (string)
- severity (enum)
- cvss_score (float)
- file_path (string)
- line_number (int)
- code_snippet (text)
- description (text)
- remediation (text)
- cve_id (string)

### Dependency
- id (UUID)
- scan_id (FK)
- name (string)
- version (string)
- latest_version (string)
- is_vulnerable (boolean)
- cve_ids (JSON array)
- vulnerabilities (JSON)

### Secret
- id (UUID)
- scan_id (FK)
- type (string)
- file_path (string)
- line_number (int)
- severity (enum)
- description (text)

## 🔧 Configuration

Backend config (in `backend/config.py`):
- UPLOAD_FOLDER: 'uploads'
- MAX_CONTENT_LENGTH: 100MB
- ALLOWED_EXTENSIONS: {zip, tar, gz, tar.gz}
- SQLALCHEMY_DATABASE_URI: sqlite:///app_tester.db
- CORS_ORIGINS: ['http://localhost:3000']

## 🤝 Contributing

1. Create a new branch
2. Implement your feature
3. Add tests
4. Submit pull request

## 📝 License

MIT License

## 🆘 Support

- GitHub Issues: Report bugs
- Discussions: Ask questions
- Email: support@apptester.dev

---

**Build Status:** ✅ v1.0 Foundation Complete  
**Lines of Code:** ~2000+ lines of core functionality  
**Test Coverage:** Basic coverage (to be expanded)  
**Documentation:** Complete (README + inline comments)

**Ready for:** Local testing, Docker deployment, feature expansion
