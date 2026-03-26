import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

interface ScanResult {
  scan_id: string;
  status: string;
  progress: number;
  vulnerabilities: any[];
  dependencies: any[];
  secrets: any[];
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [scanning, setScanning] = useState(false);
  const [results, setResults] = useState<ScanResult | null>(null);
  const [language, setLanguage] = useState('auto');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleScan = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    formData.append('include_dependencies', 'true');
    formData.append('include_secrets', 'true');

    setScanning(true);

    try {
      const response = await axios.post('/api/scan', formData);
      const scanId = response.data.scan_id;

      // Poll for results
      const pollInterval = setInterval(async () => {
        try {
          const resultResponse = await axios.get(`/api/scan/${scanId}/results`);
          setResults(resultResponse.data);

          if (resultResponse.data.scan.status === 'completed') {
            clearInterval(pollInterval);
            setScanning(false);
          }
        } catch (error) {
          console.error('Error fetching results:', error);
        }
      }, 1000);
    } catch (error) {
      console.error('Error starting scan:', error);
      setScanning(false);
      alert('Error starting scan');
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-blue-600 bg-blue-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <div className="container mx-auto p-6">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">
            🔐 Automated App Tester
          </h1>
          <p className="text-gray-400">
            Comprehensive security scanning for your applications
          </p>
        </div>

        {/* Main Content */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Start Scan</h2>

            {/* Language Selection */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="auto">Auto Detect</option>
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="csharp">C#</option>
                <option value="go">Go</option>
              </select>
            </div>

            {/* File Upload */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Code
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition cursor-pointer">
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept=".zip,.tar,.tar.gz"
                  className="hidden"
                  id="file-input"
                />
                <label htmlFor="file-input" className="cursor-pointer">
                  <div className="text-gray-500">
                    <p className="text-lg font-medium mb-2">
                      {file ? file.name : 'Drop your file here or click to upload'}
                    </p>
                    <p className="text-sm text-gray-400">
                      Supported: ZIP, TAR, TAR.GZ (Max 100MB)
                    </p>
                  </div>
                </label>
              </div>
            </div>

            {/* Scan Button */}
            <button
              onClick={handleScan}
              disabled={!file || scanning}
              className={`w-full py-3 px-4 rounded-lg font-bold text-white transition ${
                scanning
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
              }`}
            >
              {scanning ? 'Scanning...' : 'Start Scan'}
            </button>
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">Results</h2>

            {results ? (
              <div>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-red-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Critical Issues</p>
                    <p className="text-3xl font-bold text-red-600">
                      {results.summary.critical}
                    </p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">High Issues</p>
                    <p className="text-3xl font-bold text-orange-600">
                      {results.summary.high}
                    </p>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Total</p>
                    <p className="text-3xl font-bold text-blue-600">
                      {results.summary.total_vulnerabilities}
                    </p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600">Vulnerable Deps</p>
                    <p className="text-3xl font-bold text-purple-600">
                      {results.summary.vulnerable_dependencies}
                    </p>
                  </div>
                </div>

                {/* Vulnerabilities List */}
                {results.vulnerabilities.length > 0 && (
                  <div className="mb-6">
                    <h3 className="font-bold text-lg mb-3 text-gray-800">
                      Vulnerabilities
                    </h3>
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {results.vulnerabilities.slice(0, 5).map((vuln) => (
                        <div
                          key={vuln.id}
                          className={`p-3 rounded-lg border border-gray-200 ${getSeverityColor(
                            vuln.severity
                          )}`}
                        >
                          <p className="font-bold">{vuln.type}</p>
                          <p className="text-sm">{vuln.file_path}:{vuln.line_number}</p>
                          <p className="text-xs mt-1">{vuln.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-12">
                <p className="text-lg">Upload a file to start scanning</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
