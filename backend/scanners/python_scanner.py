"""
Python Security Scanner
Detects vulnerabilities in Python code using AST analysis and pattern matching
"""

import ast
import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Vulnerability:
    type: str
    severity: str
    line_number: int
    description: str
    remediation: str
    code_snippet: str
    cvss_score: float = 0.0

class PythonScanner:
    """Scanner for Python security vulnerabilities"""
    
    def __init__(self):
        self.vulnerabilities: List[Vulnerability] = []
        self.secrets_patterns = {
            'API_KEY': [
                r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
                r'apikey\s*=\s*["\']([^"\']+)["\']',
            ],
            'AWS_KEY': [
                r'AKIA[0-9A-Z]{16}',
            ],
            'PRIVATE_KEY': [
                r'-----BEGIN RSA PRIVATE KEY-----',
                r'-----BEGIN PRIVATE KEY-----',
            ],
            'PASSWORD': [
                r'password\s*=\s*["\']([^"\']+)["\']',
                r'passwd\s*=\s*["\']([^"\']+)["\']',
            ],
            'DATABASE_URL': [
                r'(postgres|mysql|mongodb)://[^/]+:[^@]+@',
            ],
            'TOKEN': [
                r'token\s*=\s*["\']([a-zA-Z0-9\-_]+)["\']',
                r'authorization\s*=\s*["\']Bearer\s+([a-zA-Z0-9\-_.]+)["\']',
            ],
        }
        
    def scan(self, file_path: str) -> List[Vulnerability]:
        """Scan a Python file for vulnerabilities"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except Exception as e:
            return []
        
        self.vulnerabilities = []
        
        # Parse AST
        try:
            tree = ast.parse(code)
        except SyntaxError:
            # If file can't be parsed, use pattern matching
            self._scan_with_patterns(code, file_path)
            return self.vulnerabilities
        
        # Scan for vulnerabilities
        self._scan_ast(tree, code, file_path)
        self._scan_with_patterns(code, file_path)
        
        return self.vulnerabilities
    
    def _scan_ast(self, tree: ast.AST, code: str, file_path: str):
        """Scan AST for vulnerabilities"""
        for node in ast.walk(tree):
            # Check for SQL Injection
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                self._check_sql_injection(node, code, file_path)
            
            # Check for eval/exec usage
            if isinstance(node, ast.Call):
                self._check_dangerous_functions(node, code, file_path)
            
            # Check for insecure random
            if isinstance(node, ast.Call):
                self._check_insecure_random(node, code, file_path)
    
    def _check_sql_injection(self, node: ast.BinOp, code: str, file_path: str):
        """Check for SQL injection patterns"""
        if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
            sql = node.left.value
            if any(keyword in sql.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                # Check if concatenating with variable
                if isinstance(node.right, (ast.Name, ast.Attribute)):
                    line_num = node.lineno
                    self.vulnerabilities.append(Vulnerability(
                        type='SQL Injection',
                        severity='high',
                        line_number=line_num,
                        description='SQL query is concatenated with user input, making it vulnerable to SQL injection attacks.',
                        remediation='Use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))',
                        code_snippet=f'Line {line_num}: SQL query concatenation detected',
                        cvss_score=7.5
                    ))
    
    def _check_dangerous_functions(self, node: ast.Call, code: str, file_path: str):
        """Check for dangerous function calls"""
        dangerous_funcs = {
            'eval': ('Critical Code Execution', 'critical', 9.8, 'eval() executes arbitrary Python code. Use ast.literal_eval() for safe evaluation or avoid dynamic code execution.'),
            'exec': ('Critical Code Execution', 'critical', 9.8, 'exec() executes arbitrary Python code. Avoid dynamic code execution.'),
            '__import__': ('Dynamic Import', 'high', 8.0, 'Dynamic imports can load arbitrary modules. Use importlib.import_module() with validation.'),
            'pickle.loads': ('Insecure Deserialization', 'high', 8.1, 'pickle.loads() is unsafe. Use json for serialization or set strict object validation.'),
            'os.system': ('Command Injection', 'high', 8.6, 'os.system() is vulnerable to command injection. Use subprocess.run() with a list of arguments.'),
            'subprocess.shell': ('Command Injection', 'high', 8.6, 'shell=True in subprocess is vulnerable. Use shell=False with argument list.'),
        }
        
        func_name = self._get_func_name(node.func)
        
        for danger_func, (vuln_type, severity, cvss, remediation) in dangerous_funcs.items():
            if danger_func in func_name:
                self.vulnerabilities.append(Vulnerability(
                    type=vuln_type,
                    severity=severity,
                    line_number=node.lineno,
                    description=f'{danger_func}() detected. This function is inherently unsafe.',
                    remediation=remediation,
                    code_snippet=f'Line {node.lineno}: {func_name}() call',
                    cvss_score=cvss
                ))
    
    def _check_insecure_random(self, node: ast.Call, code: str, file_path: str):
        """Check for insecure random usage"""
        func_name = self._get_func_name(node.func)
        
        if 'random.random' in func_name or 'random.randint' in func_name:
            # Check if used for security purposes
            if self._is_security_context(node, code):
                self.vulnerabilities.append(Vulnerability(
                    type='Insecure Randomness',
                    severity='high',
                    line_number=node.lineno,
                    description='random module is not cryptographically secure. Use secrets module for security-sensitive operations.',
                    remediation='Replace random.random() with secrets.SystemRandom() or secrets.choice()',
                    code_snippet=f'Line {node.lineno}: Insecure random usage',
                    cvss_score=7.5
                ))
    
    def _scan_with_patterns(self, code: str, file_path: str):
        """Scan code with regex patterns"""
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for secrets
            for secret_type, patterns in self.secrets_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        self.vulnerabilities.append(Vulnerability(
                            type=f'Exposed {secret_type}',
                            severity='critical',
                            line_number=line_num,
                            description=f'{secret_type} appears to be hardcoded in the source code.',
                            remediation=f'Move {secret_type.lower()} to environment variables or secure configuration management.',
                            code_snippet=line,
                            cvss_score=9.8
                        ))
            
            # Check for weak cryptography
            weak_crypto = [
                (r'hashlib\.md5', 'MD5 is cryptographically broken. Use SHA-256 or stronger.'),
                (r'hashlib\.sha1', 'SHA1 is weak. Use SHA-256 or stronger.'),
                (r'Cipher\.AES.*MODE_ECB', 'ECB mode is insecure. Use CBC, GCM, or other authenticated modes.'),
                (r'ssl\._create_unverified_context', 'SSL verification is disabled. Enable certificate verification.'),
            ]
            
            for pattern, message in weak_crypto:
                if re.search(pattern, line, re.IGNORECASE):
                    self.vulnerabilities.append(Vulnerability(
                        type='Weak Cryptography',
                        severity='high',
                        line_number=line_num,
                        description=message,
                        remediation='Use SHA-256+, AES-GCM, or modern cryptographic libraries.',
                        code_snippet=line,
                        cvss_score=7.5
                    ))
            
            # Check for hardcoded file paths
            if re.search(r'(open|file)\(["\']/(etc|root|home|var)/', line):
                self.vulnerabilities.append(Vulnerability(
                    type='Hardcoded File Path',
                    severity='medium',
                    line_number=line_num,
                    description='Absolute file path is hardcoded. This may cause portability issues.',
                    remediation='Use relative paths or configuration files for file locations.',
                    code_snippet=line,
                    cvss_score=5.3
                ))
    
    def _get_func_name(self, func_node) -> str:
        """Extract function name from AST node"""
        if isinstance(func_node, ast.Name):
            return func_node.id
        elif isinstance(func_node, ast.Attribute):
            return func_node.attr
        return ''
    
    def _is_security_context(self, node: ast.Call, code: str) -> bool:
        """Check if random is used in security context"""
        security_keywords = ['token', 'secret', 'key', 'nonce', 'salt', 'csrf']
        line_text = code.split('\n')[node.lineno - 1]
        return any(keyword in line_text.lower() for keyword in security_keywords)

# ============================================================================
# Example Usage
# ============================================================================

if __name__ == '__main__':
    scanner = PythonScanner()
    
    # Example vulnerable code
    test_code = '''
import random
import hashlib

# SQL Injection vulnerability
user_id = input("Enter ID: ")
query = "SELECT * FROM users WHERE id = " + user_id

# Hardcoded API key
api_key = "sk_test_12345678901234567890"

# Weak password hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# Insecure random for token
token = random.randint(100000, 999999)
'''
    
    # This would normally scan a file, but here we scan the string
    print("Python Security Scanner - Test Results")
