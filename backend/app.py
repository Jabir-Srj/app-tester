"""
Automated App Tester - Flask Backend
Main application entry point
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import uuid
import threading
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)

# Configuration
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_tester.db'
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'zip', 'tar', 'gz', 'tar.gz'}
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max upload
    JSON_SORT_KEYS = False

app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Create upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Scan(db.Model):
    """Scan record model"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, scanning, completed, failed
    progress = db.Column(db.Integer, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Results
    vulnerabilities = db.relationship('Vulnerability', backref='scan', lazy=True, cascade='all, delete-orphan')
    dependencies = db.relationship('Dependency', backref='scan', lazy=True, cascade='all, delete-orphan')
    secrets = db.relationship('Secret', backref='scan', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'language': self.language,
            'status': self.status,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'vulnerability_count': len(self.vulnerabilities),
            'critical_count': sum(1 for v in self.vulnerabilities if v.severity == 'critical'),
            'high_count': sum(1 for v in self.vulnerabilities if v.severity == 'high'),
        }

class Vulnerability(db.Model):
    """Detected vulnerability"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = db.Column(db.String(36), db.ForeignKey('scan.id'), nullable=False)
    
    # Vulnerability details
    type = db.Column(db.String(100), nullable=False)  # SQL Injection, XSS, etc.
    severity = db.Column(db.String(20), nullable=False)  # critical, high, medium, low, info
    cvss_score = db.Column(db.Float, nullable=True)
    file_path = db.Column(db.String(500), nullable=False)
    line_number = db.Column(db.Integer, nullable=True)
    code_snippet = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False)
    remediation = db.Column(db.Text, nullable=False)
    cve_id = db.Column(db.String(50), nullable=True)  # CVE-2024-XXXXX
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'severity': self.severity,
            'cvss_score': self.cvss_score,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'code_snippet': self.code_snippet,
            'description': self.description,
            'remediation': self.remediation,
            'cve_id': self.cve_id,
            'created_at': self.created_at.isoformat(),
        }

class Dependency(db.Model):
    """Scanned dependency"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = db.Column(db.String(36), db.ForeignKey('scan.id'), nullable=False)
    
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    latest_version = db.Column(db.String(50), nullable=True)
    is_vulnerable = db.Column(db.Boolean, default=False)
    cve_ids = db.Column(db.JSON, default=list)  # List of CVE IDs
    vulnerabilities = db.Column(db.JSON, default=list)  # Detailed vulnerability info
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'latest_version': self.latest_version,
            'is_vulnerable': self.is_vulnerable,
            'cve_ids': self.cve_ids,
            'vulnerabilities': self.vulnerabilities,
        }

class Secret(db.Model):
    """Detected secret/credential"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = db.Column(db.String(36), db.ForeignKey('scan.id'), nullable=False)
    
    type = db.Column(db.String(100), nullable=False)  # API_KEY, PASSWORD, TOKEN, etc.
    file_path = db.Column(db.String(500), nullable=False)
    line_number = db.Column(db.Integer, nullable=True)
    severity = db.Column(db.String(20), default='critical')  # Usually critical
    description = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'severity': self.severity,
            'description': self.description,
        }

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/scan', methods=['POST'])
def create_scan():
    """Create a new scan"""
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Get options
    language = request.form.get('language', 'auto')
    include_dependencies = request.form.get('include_dependencies', 'true').lower() == 'true'
    include_secrets = request.form.get('include_secrets', 'true').lower() == 'true'
    
    # Save file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Create scan record
        scan = Scan(
            filename=filename,
            language=language,
            status='pending'
        )
        db.session.add(scan)
        db.session.commit()
        
        # Start scanning in background
        thread = threading.Thread(
            target=run_scan,
            args=(scan.id, file_path, language, include_dependencies, include_secrets)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'scan_id': scan.id,
            'status': 'scanning',
            'message': 'Scan started'
        }), 202
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    """Get scan details"""
    scan = Scan.query.get(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify(scan.to_dict())

@app.route('/api/scan/<scan_id>/results', methods=['GET'])
def get_scan_results(scan_id):
    """Get scan results"""
    scan = Scan.query.get(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    return jsonify({
        'scan': scan.to_dict(),
        'vulnerabilities': [v.to_dict() for v in scan.vulnerabilities],
        'dependencies': [d.to_dict() for d in scan.dependencies],
        'secrets': [s.to_dict() for s in scan.secrets],
        'summary': {
            'total_vulnerabilities': len(scan.vulnerabilities),
            'critical': sum(1 for v in scan.vulnerabilities if v.severity == 'critical'),
            'high': sum(1 for v in scan.vulnerabilities if v.severity == 'high'),
            'medium': sum(1 for v in scan.vulnerabilities if v.severity == 'medium'),
            'low': sum(1 for v in scan.vulnerabilities if v.severity == 'low'),
            'info': sum(1 for v in scan.vulnerabilities if v.severity == 'info'),
            'total_dependencies': len(scan.dependencies),
            'vulnerable_dependencies': sum(1 for d in scan.dependencies if d.is_vulnerable),
            'total_secrets': len(scan.secrets),
        }
    })

@app.route('/api/scans', methods=['GET'])
def list_scans():
    """List all scans"""
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    scans = Scan.query.order_by(Scan.created_at.desc()).limit(limit).offset(offset).all()
    total = Scan.query.count()
    
    return jsonify({
        'scans': [s.to_dict() for s in scans],
        'total': total,
        'limit': limit,
        'offset': offset
    })

@app.route('/api/scan/<scan_id>/report', methods=['GET'])
def download_report(scan_id):
    """Download scan report"""
    scan = Scan.query.get(scan_id)
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    format_type = request.args.get('format', 'json')  # json, html, pdf
    
    if format_type == 'json':
        # Generate JSON report
        report = {
            'scan': scan.to_dict(),
            'vulnerabilities': [v.to_dict() for v in scan.vulnerabilities],
            'dependencies': [d.to_dict() for d in scan.dependencies],
            'secrets': [s.to_dict() for s in scan.secrets],
        }
        return jsonify(report)
    
    elif format_type == 'html':
        # Generate HTML report (simplified)
        html = generate_html_report(scan)
        return html, 200, {'Content-Type': 'text/html'}
    
    return jsonify({'error': 'Unsupported format'}), 400

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def run_scan(scan_id, file_path, language, include_dependencies, include_secrets):
    """Run security scan (background task)"""
    try:
        scan = Scan.query.get(scan_id)
        scan.status = 'scanning'
        db.session.commit()
        
        # TODO: Extract and scan files
        # For now, just update status
        scan.status = 'completed'
        scan.progress = 100
        scan.completed_at = datetime.utcnow()
        db.session.commit()
        
    except Exception as e:
        scan = Scan.query.get(scan_id)
        scan.status = 'failed'
        scan.error_message = str(e)
        db.session.commit()

def generate_html_report(scan):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>App Tester Report - {scan.filename}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; }}
            .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
            .card {{ background: #f9f9f9; padding: 15px; border-radius: 4px; border-left: 4px solid #007bff; }}
            .critical {{ border-left-color: #dc3545; }}
            .high {{ border-left-color: #fd7e14; }}
            .vulnerability {{ margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 4px; }}
            .severity {{ display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }}
            .severity.critical {{ background: #dc3545; color: white; }}
            .severity.high {{ background: #fd7e14; color: white; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Security Scan Report</h1>
            <p><strong>File:</strong> {scan.filename}</p>
            <p><strong>Language:</strong> {scan.language}</p>
            <p><strong>Scanned:</strong> {scan.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary">
                <div class="card critical">
                    <strong>Critical:</strong> {sum(1 for v in scan.vulnerabilities if v.severity == 'critical')}
                </div>
                <div class="card high">
                    <strong>High:</strong> {sum(1 for v in scan.vulnerabilities if v.severity == 'high')}
                </div>
                <div class="card">
                    <strong>Medium:</strong> {sum(1 for v in scan.vulnerabilities if v.severity == 'medium')}
                </div>
                <div class="card">
                    <strong>Total:</strong> {len(scan.vulnerabilities)}
                </div>
            </div>
            
            <h2>Vulnerabilities</h2>
            {''.join(f'''
            <div class="vulnerability">
                <span class="severity {v.severity}">{v.severity.upper()}</span>
                <h3>{v.type}</h3>
                <p><strong>File:</strong> {v.file_path}</p>
                <p><strong>Description:</strong> {v.description}</p>
                <p><strong>Remediation:</strong> {v.remediation}</p>
            </div>
            ''' for v in scan.vulnerabilities)}
        </div>
    </body>
    </html>
    """
    return html

# ============================================================================
# INITIALIZATION
# ============================================================================

@app.before_request
def create_tables():
    """Create database tables on first request"""
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
