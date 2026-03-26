"""
Dependency Vulnerability Scanner
Checks for known vulnerabilities in project dependencies
"""

import subprocess
import json
import re
from typing import List, Dict, Any

class DependencyScanner:
    """Scan dependencies for known vulnerabilities"""
    
    def scan_python_dependencies(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan Python dependencies using pip-audit"""
        vulnerabilities = []
        
        try:
            # Run pip-audit
            result = subprocess.run(
                ['pip-audit', '--desc', '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                for vuln in data.get('vulnerabilities', []):
                    vulnerabilities.append({
                        'name': vuln['name'],
                        'version': vuln['version'],
                        'vulnerability_id': vuln['id'],
                        'description': vuln['description'],
                        'fixed_version': vuln.get('fix_versions', ['N/A'])[0],
                        'cve_ids': vuln.get('cve_ids', []),
                        'severity': self._determine_severity(vuln),
                    })
        except Exception as e:
            print(f"Error scanning Python dependencies: {e}")
        
        return vulnerabilities
    
    def scan_javascript_dependencies(self, directory: str) -> List[Dict[str, Any]]:
        """Scan JavaScript dependencies using npm audit"""
        vulnerabilities = []
        
        try:
            # Run npm audit
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                for pkg_name, vuln_info in data.get('vulnerabilities', {}).items():
                    for severity, count in vuln_info.get('via', {}).items():
                        vulnerabilities.append({
                            'name': pkg_name,
                            'version': vuln_info.get('version', 'unknown'),
                            'severity': severity,
                            'description': str(count),
                        })
        except Exception as e:
            print(f"Error scanning JavaScript dependencies: {e}")
        
        return vulnerabilities
    
    def scan_java_dependencies(self, pom_file: str) -> List[Dict[str, Any]]:
        """Scan Java dependencies using OWASP Dependency-Check"""
        vulnerabilities = []
        
        try:
            result = subprocess.run(
                ['dependency-check', '--scan', pom_file, '--format', 'JSON', '--out', '/tmp/dc-report.json'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode in [0, 1]:  # 0 or 1 are success
                with open('/tmp/dc-report.json', 'r') as f:
                    data = json.load(f)
                    for dep in data.get('reportSchema', {}).get('dependencies', []):
                        for vuln in dep.get('vulnerabilities', []):
                            vulnerabilities.append({
                                'name': dep.get('name'),
                                'version': dep.get('version'),
                                'cve_id': vuln.get('cve'),
                                'description': vuln.get('description'),
                                'severity': vuln.get('severity'),
                                'cvss_score': vuln.get('cvssV3Score'),
                            })
        except Exception as e:
            print(f"Error scanning Java dependencies: {e}")
        
        return vulnerabilities
    
    def _determine_severity(self, vuln: Dict) -> str:
        """Determine vulnerability severity"""
        description = vuln.get('description', '').lower()
        
        if any(keyword in description for keyword in ['rce', 'remote code execution', 'critical']):
            return 'critical'
        elif any(keyword in description for keyword in ['injection', 'xss', 'xxe']):
            return 'high'
        elif any(keyword in description for keyword in ['dos', 'denial']):
            return 'high'
        elif any(keyword in description for keyword in ['auth', 'bypass']):
            return 'high'
        else:
            return 'medium'

class SecretScanner:
    """Scan for hardcoded secrets and credentials"""
    
    PATTERNS = {
        'AWS_KEY': r'AKIA[0-9A-Z]{16}',
        'PRIVATE_KEY': r'-----BEGIN RSA PRIVATE KEY-----',
        'API_KEY': r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
        'PASSWORD': r'password\s*=\s*["\']([^"\']{6,})["\']',
        'DATABASE_URL': r'(postgres|mysql)://[^/]+:[^@]+@',
        'GITHUB_TOKEN': r'ghp_[0-9a-zA-Z]{36}',
        'SLACK_TOKEN': r'xox[baprs]-[0-9a-zA-Z]{10,48}',
    }
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[Dict[str, Any]]:
        """Scan directory for secrets"""
        if extensions is None:
            extensions = ['.py', '.js', '.java', '.cs', '.go', '.rb', '.env', '.properties']
        
        secrets = []
        
        try:
            import os
            for root, dirs, files in os.walk(directory):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.env']]
                
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        file_secrets = self._scan_file(file_path)
                        secrets.extend(file_secrets)
        except Exception as e:
            print(f"Error scanning for secrets: {e}")
        
        return secrets
    
    def _scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan individual file for secrets"""
        secrets = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for secret_type, pattern in self.PATTERNS.items():
                        if re.search(pattern, line, re.IGNORECASE):
                            secrets.append({
                                'type': secret_type,
                                'file': file_path,
                                'line': line_num,
                                'severity': 'critical',
                                'description': f'{secret_type} detected in source code'
                            })
        except Exception:
            pass
        
        return secrets

if __name__ == '__main__':
    print("Dependency Scanner initialized")
