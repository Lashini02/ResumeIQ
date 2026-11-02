import { useState } from "react";
import axios from "axios";
import {
  UploadCloud,
  FileText,
  BrainCircuit,
  CheckCircle,
  AlertCircle,
  Sparkles,
  ArrowRight,
  RefreshCw,
  Target,
  Download,
} from "lucide-react";

import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setResults(null);

    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please select a PDF file.");
      setFile(null);
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("File must be smaller than 5 MB.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleAnalyze = async (event) => {
    event.preventDefault();

    setError("");
    setResults(null);

    if (!file) {
      setError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);

    const formData = new FormData();

    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/analyze",
        formData,
      );

      setResults(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Unable to connect to the server. Please check your backend.",
      );
    } finally {
      setLoading(false);
    }
  };

  const resetAnalyzer = () => {
    setFile(null);
    setJobDescription("");
    setResults(null);
    setError("");

    const input = document.getElementById("resume-upload");

    if (input) input.value = "";
  };

  const downloadReport = () => {
    if (!results) return;

    const report = `
RESUMEIQ - RESUME ANALYSIS REPORT

Resume: ${results.filename}

Resume Match Score: ${results.score}%
Text Similarity: ${results.similarity}%
Resume Word Count: ${results.word_count}

MATCHED SKILLS:
${results.matched_skills.join(", ") || "None"}

MISSING SKILLS:
${results.missing_skills.join(", ") || "None"}

SUGGESTIONS:
${results.suggestions.map((s, i) => `${i + 1}. ${s}`).join("\n")}

Note: This is an experimental keyword and text similarity
indicator, not a hiring decision or official ATS score.
`;

    const blob = new Blob([report], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "ResumeIQ_Report.txt";
    link.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <nav className="navbar">
        <div className="brand">
          <BrainCircuit size={29} />
          <span>ResumeIQ</span>
        </div>

        <span className="nav-label">AI Resume Analyzer</span>
      </nav>

      <main className="main-container">
        <section className="hero">
          <div className="hero-tag">
            <Sparkles size={15} />
            SMART RESUME ANALYSIS
          </div>

          <h1>
            Your Resume.
            <br />
            <span>One Step Closer.</span>
          </h1>

          <p>
            Discover how well your resume matches your dream job. Get useful
            keyword insights and improvement suggestions.
          </p>
        </section>

        {!results && (
          <form className="analyzer-card" onSubmit={handleAnalyze}>
            <div className="section-heading">
              <FileText size={22} />
              <div>
                <h2>Analyze Your Resume</h2>
                <p>Upload your CV and enter the target job description.</p>
              </div>
            </div>

            <label className="field-label">Upload Resume (PDF)</label>

            <label className="upload-box" htmlFor="resume-upload">
              <UploadCloud size={38} />

              {file ? (
                <>
                  <strong>{file.name}</strong>
                  <span>
                    {(file.size / 1024).toFixed(1)} KB · Ready to analyze
                  </span>
                </>
              ) : (
                <>
                  <strong>Click to upload your resume</strong>
                  <span>PDF format · Maximum 5 MB</span>
                </>
              )}
            </label>

            <input
              id="resume-upload"
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              hidden
            />

            <label className="field-label">Job Description</label>

            <textarea
              className="job-input"
              placeholder="Paste the complete job description here..."
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
              rows="8"
            />

            {error && (
              <div className="error-message">
                <AlertCircle size={18} />
                {error}
              </div>
            )}

            <button className="analyze-button" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <RefreshCw className="spin" size={19} />
                  Analyzing Resume...
                </>
              ) : (
                <>
                  Analyze My Resume
                  <ArrowRight size={19} />
                </>
              )}
            </button>

            <p className="privacy-text">
              Your PDF is processed in memory and is not stored by this
              application.
            </p>
          </form>
        )}

        {results && (
          <section className="results-container">
            <div className="result-heading">
              <div>
                <span className="result-tag">
                  <Sparkles size={15} /> ANALYSIS COMPLETE
                </span>

                <h2>Your Resume Report</h2>

                <p>{results.filename}</p>
              </div>

              <button className="secondary-button" onClick={resetAnalyzer}>
                <RefreshCw size={16} />
                New Analysis
              </button>
            </div>

            <div className="score-card">
              <div className="score-icon">
                <Target size={27} />
              </div>

              <div>
                <h3>{results.score}%</h3>
                <p>Resume Match Score</p>
                <span>Based on keyword coverage and text similarity</span>
              </div>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <span>Text Similarity</span>
                <strong>{results.similarity}%</strong>
              </div>

              <div className="stat-card">
                <span>Matched Skills</span>
                <strong>{results.matched_skills.length}</strong>
              </div>

              <div className="stat-card">
                <span>Missing Skills</span>
                <strong>{results.missing_skills.length}</strong>
              </div>

              <div className="stat-card">
                <span>Resume Words</span>
                <strong>{results.word_count}</strong>
              </div>
            </div>

            <div className="result-card">
              <h3>
                <CheckCircle size={20} />
                Matched Skills
              </h3>

              <div className="skill-list">
                {results.matched_skills.length > 0 ? (
                  results.matched_skills.map((skill) => (
                    <span className="skill matched" key={skill}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>No matched skills found.</p>
                )}
              </div>
            </div>

            <div className="result-card">
              <h3>
                <AlertCircle size={20} />
                Missing Keywords
              </h3>

              <div className="skill-list">
                {results.missing_skills.length > 0 ? (
                  results.missing_skills.map((skill) => (
                    <span className="skill missing" key={skill}>
                      {skill}
                    </span>
                  ))
                ) : (
                  <p>No missing keywords from our skill list.</p>
                )}
              </div>
            </div>

            <div className="result-card">
              <h3>
                <Sparkles size={20} />
                Improvement Suggestions
              </h3>

              <ul className="suggestions">
                {results.suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>

            <div className="result-card">
              <h3>All Recognized Resume Skills</h3>

              <div className="skill-list">
                {results.resume_skills.map((skill) => (
                  <span className="skill matched" key={skill}>
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="report-actions">
              <button className="analyze-button" onClick={downloadReport}>
                <Download size={18} />
                Download Report
              </button>

              <button className="secondary-button" onClick={resetAnalyzer}>
                Analyze Another Resume
              </button>
            </div>

            <p className="disclaimer">
              This score is an experimental keyword and text similarity
              indicator. It is not an official ATS score, a complete evaluation
              of candidate suitability, or a hiring decision. Add missing skills
              only when they accurately reflect your abilities.
            </p>
          </section>
        )}
      </main>

      <footer>
        <p>ResumeIQ © 2026 · Built with React & Python</p>
      </footer>
    </div>
  );
}

export default App;
