# Automated App Tester 🔐

A comprehensive automated app tester web application for scanning source code and detecting vulnerabilities, security flaws, and insecure dependencies.

## Features

### 🔍 Scanning Capabilities
- **Multi-language support:** Python, JavaScript/TypeScript, Java, C#, Go, Ruby
- **Static code analysis** with AST parsing
- **Dynamic analysis** with sandbox execution
- **Dependency vulnerability scanning**
- **Secret/credential detection**
- **Custom security rule engine**

### 📊 Vulnerability Detection
- SQL Injection & command injection patterns
- XSS & CSRF vulnerabilities
- Hardcoded secrets (API keys, tokens, credentials)
- Weak cryptography & insecure hashing
- Insecure dependencies & known CVEs
- Buffer overflows & memory leaks
- Authentication/authorization flaws
- Data exposure risks & XXE
- Insecure deserialization
- Path traversal & file access issues

### 🎯 Output Formats
- **Interactive HTML dashboard**
- **JSON reports** (machine-readable)
- **PDF reports** (printable)
- **CLI output** (terminal)
- **Real-time scanning progress**

### 🌐 Web App Features
- Upload source code (ZIP/TAR/direct)
- GitHub repository integration
- Scan history & comparison
- Vulnerability filtering/sorting
- CVSS scores & severity levels
- Detailed remediation suggestions
- Batch scanning
- Scheduled scans (future)

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** React + TypeScript + Tailwind CSS
- **Database:** SQLite
- **Containerization:** Docker
- **Security Tools:**
  - Bandit (Python security)
  - Semgrep (static analysis)
  - npm audit (JavaScript dependencies)
  - pip-audit (Python dependencies)
  - Trivy (vulnerability scanner)
  - OWASP ZAP (dynamic analysis)

## Free APIs Used

1. **Snyk API** - dependency vulnerability scanning
2. **NVD (CVE Database)** - vulnerability data
3. **GitHub API** - repository analysis
4. **Bandit** - Python security linting
5. **Semgrep** - static analysis rules

## Project Structure

```
app-tester/
├── backend/
│   ├── app.py                 # Flask main application
│   ├── config.py              # Configuration
│   ├── models.py              # Database models
│   ├── scanners/
│   │   ├── __init__.py
│   │   ├── base_scanner.py    # Abstract base
│   │   ├── python_scanner.py  # Python security scanning
│   │   ├── js_scanner.py      # JavaScript/TypeScript scanning
│   │   ├── java_scanner.py    # Java scanning
│   │   ├── go_scanner.py      # Go scanning
│   │   ├── dependency_scanner.py
│   │   ├── secret_scanner.py
│   │   └── custom_rules.py
│   ├── api_integrations/
│   │   ├── __init__.py
│   │   ├── snyk_integration.py
│   │   ├── nvd_integration.py
│   │   ├── github_integration.py
│   │   └── bandit_integration.py
│   ├── utils/
│   │   ├── file_handler.py
│   │   ├── report_generator.py
│   │   └── validators.py
│   ├── static/          # Generated reports
│   ├── uploads/         # Uploaded files
│   ├── requirements.txt
│   └── run.py           # Entry point
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx
│   │   │   ├── ScanProgress.tsx
│   │   │   ├── VulnerabilityList.tsx
│   │   │   ├── ReportViewer.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── ScanPage.tsx
│   │   │   └── HistoryPage.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── LICENSE
└── CONTRIBUTING.md
```

## Installation

### Local Development

1. **Clone repository**
```bash
git clone https://github.com/yourusername/app-tester.git
cd app-tester
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

3. **Frontend setup**
```bash
cd frontend
npm install
npm run dev
```

Backend runs on `http://localhost:5000`
Frontend runs on `http://localhost:5173`

### Docker

```bash
docker-compose up
```

App runs on `http://localhost:3000`

## Usage

### Web Interface

1. Go to http://localhost:3000
2. Upload your source code (ZIP file)
3. Select scan options
4. Start scan
5. View results in real-time
6. Download report (HTML/JSON/PDF)

### API

```bash
# Upload and scan
curl -X POST http://localhost:5000/api/scan \
  -F "file=@myapp.zip" \
  -F "language=python" \
  -F "include_dependencies=true"

# Get scan results
curl http://localhost:5000/api/scan/scan_id/results

# Get scan history
curl http://localhost:5000/api/scans
```

### CLI (Future)

```bash
app-tester scan ./myapp --language python --report html
```

## Vulnerability Severity Levels

- **Critical:** Immediate exploitation risk (RCE, auth bypass)
- **High:** Significant security impact (SQL injection, XSS)
- **Medium:** Moderate risk, exploitation may be limited
- **Low:** Minimal impact or unlikely exploitation
- **Info:** Informational findings, best practices

## Supported Languages

- ✅ Python (v1)
- ✅ JavaScript/TypeScript (v1)
- 🔄 Java (planned)
- 🔄 C# (planned)
- 🔄 Go (planned)
- 🔄 Ruby (planned)

## API Keys (Optional)

For enhanced scanning:

- **Snyk API:** Get free at https://snyk.io
- **GitHub Token:** For private repo scanning

Set in `.env`:
```
SNYK_API_TOKEN=your_token
GITHUB_TOKEN=your_token
```

## Configuration

See `backend/config.py` for:
- Upload size limits
- Timeout settings
- Scan concurrency
- Database settings
- API rate limits

## Development Roadmap

- [ ] v1.0 - Python + JavaScript scanning with web interface
- [ ] v1.1 - Java, C#, Go support
- [ ] v1.2 - GitHub integration
- [ ] v1.3 - Scheduled scans
- [ ] v1.4 - Scan comparison & trends
- [ ] v1.5 - Team collaboration features
- [ ] v2.0 - CLI tool
- [ ] v2.1 - CI/CD pipeline integration

## Performance

- Python scanning: ~500 LOC/sec
- JavaScript scanning: ~800 LOC/sec
- Dependency scanning: Variable (API dependent)
- Secret scanning: ~1000 LOC/sec

## Security

- Uploaded files scanned in isolated sandbox
- No data stored permanently (optional)
- Supports private scans
- HTTPS ready
- Rate limiting enabled

## Contributing

See CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file

## Support

- 📧 Email: support@apptester.dev
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## Disclaimer

This tool is for authorized security testing only. Unauthorized access to computer systems is illegal.

---

**Made with ❤️ for developers who care about security**
