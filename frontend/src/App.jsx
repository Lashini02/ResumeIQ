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
  Mail,
  Phone,
  Contact,
  Code,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

const SECTION_LABELS = {
  professional_summary: "Professional Summary",
  technical_skills: "Technical Skills",
  work_experience: "Work Experience",
  education: "Education",
  projects: "Projects",
  certifications: "Certifications",
  achievements: "Achievements",
  additional_information: "Additional Information",
};

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];
    setError("");
    setResults(null);

    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please select a PDF file.");
      setFile(null);
      event.target.value = "";
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("Your PDF must be smaller than 5 MB.");
      setFile(null);
      event.target.value = "";
      return;
    }

    setFile(selectedFile);
  };

  const handleAnalyze = async (event) => {
    event.preventDefault();
    setError("");
    setResults(null);

    if (!file) {
      setError("Please upload your resume first.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please paste the job description.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await axios.post(`${API_URL}/api/analyze`, formData);
      setResults(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "Could not connect to ResumeIQ. Please check that the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async () => {
    if (!file || !jobDescription.trim()) {
      setError("Please upload a resume and enter a job description.");
      return;
    }

    setError("");
    setDownloading(true);
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await axios.post(`${API_URL}/api/report`, formData, {
        responseType: "blob",
      });

      const pdfBlob = new Blob([response.data], { type: "application/pdf" });
      const downloadUrl = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "ResumeIQ_Analysis_Report.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(() => window.URL.revokeObjectURL(downloadUrl), 1000);
    } catch (err) {
      let message = "Unable to download the report. Please try again.";
      if (err.response?.data instanceof Blob) {
        try {
          const text = await err.response.data.text();
          const data = JSON.parse(text);
          message = data.error || message;
        } catch {
          // Keep the default message.
        }
      } else if (err.response?.data?.error) {
        message = err.response.data.error;
      }
      setError(message);
      console.error("PDF download error:", err);
    } finally {
      setDownloading(false);
    }
  };

  const resetAnalyzer = () => {
    setFile(null);
    setJobDescription("");
    setResults(null);
    setError("");
    const input = document.getElementById("resume-upload");
    if (input) input.value = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const matchedSkills = Array.isArray(results?.matched_skills)
    ? results.matched_skills
    : [];
  const missingSkills = Array.isArray(results?.missing_skills)
    ? results.missing_skills
    : [];
  const resumeSkills = Array.isArray(results?.resume_skills)
    ? results.resume_skills
    : [];
  const matchedKeywords = Array.isArray(results?.matched_keywords)
    ? results.matched_keywords
    : [];
  const missingKeywords = Array.isArray(results?.missing_keywords)
    ? results.missing_keywords
    : [];
  const suggestions = Array.isArray(results?.suggestions)
    ? results.suggestions
    : [];

  const sectionData = results?.sections || {};
  const sectionSummary = sectionData.summary || {};
  const contactInfo = sectionData.contact_information || {};
  const score = Math.max(0, Math.min(100, Number(results?.score) || 0));
  const similarity = Math.max(
    0,
    Math.min(100, Number(results?.similarity) || 0),
  );

  return (
    <div className="app">
      <nav className="navbar">
        <a className="brand" href="/" aria-label="ResumeIQ home">
          <BrainCircuit size={27} />
          <span>ResumeIQ</span>
        </a>
        <span className="nav-label">
          Resume & Job Match Analyzer Developed by Lashini Chamodi
        </span>
      </nav>

      <main className="main-container">
        {!results ? (
          <>
            <section className="hero">
              <div className="hero-tag">
                <Sparkles size={14} />
                SMART RESUME INSIGHTS
              </div>
              <h1>
                Make your next
                <span> career move count.</span>
              </h1>
              <p>
                Upload your CV and add a job description to see matching skills,
                missing keywords and practical ways to improve your application.
              </p>
            </section>

            <form className="analyzer-card" onSubmit={handleAnalyze}>
              <div className="section-heading">
                <FileText size={22} />
                <div>
                  <h2>Start your resume analysis</h2>
                  <p>
                    Two quick steps. Your results will appear in one dashboard.
                  </p>
                </div>
              </div>

              <label className="field-label" htmlFor="resume-upload">
                1. Upload your resume
              </label>
              <label className="upload-box" htmlFor="resume-upload">
                <UploadCloud size={34} />
                {file ? (
                  <>
                    <strong>{file.name}</strong>
                    <span>
                      {(file.size / 1024).toFixed(1)} KB · Ready to analyze
                    </span>
                  </>
                ) : (
                  <>
                    <strong>Choose your PDF resume</strong>
                    <span>Click here to browse · PDF only · Maximum 5 MB</span>
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

              <label className="field-label" htmlFor="job-description">
                2. Paste the job description
              </label>
              <textarea
                id="job-description"
                className="job-input"
                placeholder="Paste the job responsibilities, requirements and skills here..."
                value={jobDescription}
                onChange={(event) => setJobDescription(event.target.value)}
                rows={7}
              />

              {error && (
                <div className="error-message">
                  <AlertCircle size={18} />
                  <span>{error}</span>
                </div>
              )}

              <button
                className="analyze-button"
                type="submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <RefreshCw className="spin" size={18} />
                    Analyzing your resume...
                  </>
                ) : (
                  <>
                    Analyze my resume
                    <ArrowRight size={18} />
                  </>
                )}
              </button>
              <p className="privacy-text">
                The current prototype processes the uploaded PDF in memory.
              </p>
            </form>
          </>
        ) : (
          <section className="results-container">
            <div className="result-heading">
              <div>
                <span className="result-tag">
                  <CheckCircle size={15} />
                  ANALYSIS COMPLETE
                </span>
                <h1>Your match overview</h1>
                <p className="file-name">{results.filename || file?.name}</p>
              </div>
              <button
                className="secondary-button"
                onClick={resetAnalyzer}
                type="button"
              >
                <RefreshCw size={16} />
                New analysis
              </button>
            </div>

            <section className="match-hero-card">
              <div className="match-score-copy">
                <span className="eyebrow">YOUR RESUME MATCH</span>
                <div className="score-number">
                  {score.toFixed(1)}
                  <small>%</small>
                </div>
                <p>
                  This is an experimental indicator of how closely the resume
                  text matches the job description.
                </p>
                <div className="score-track">
                  <span style={{ width: `${score}%` }} />
                </div>
              </div>
              <div className="match-side-stats">
                <div className="mini-stat">
                  <span>Text similarity</span>
                  <strong>{similarity.toFixed(1)}%</strong>
                </div>
                <div className="mini-stat">
                  <span>Skills matched</span>
                  <strong>{matchedSkills.length}</strong>
                </div>
                <div className="mini-stat">
                  <span>Skills to review</span>
                  <strong>{missingSkills.length}</strong>
                </div>
              </div>
            </section>

            <div className="section-intro">
              <div>
                <h2>Skills comparison</h2>
                <p>
                  See what already matches and what the job description asks
                  for.
                </p>
              </div>
            </div>

            <div className="comparison-grid">
              <article className="result-card matched-card">
                <div className="card-title">
                  <CheckCircle size={19} />
                  <h3>
                    Matching skills <span>{matchedSkills.length}</span>
                  </h3>
                </div>
                <p className="card-description">
                  Found in both your resume and the job description.
                </p>
                <div className="skill-list">
                  {matchedSkills.length ? (
                    matchedSkills.map((skill) => (
                      <span className="skill matched" key={skill}>
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="empty-state">No matching skills detected.</p>
                  )}
                </div>
              </article>

              <article className="result-card missing-card">
                <div className="card-title">
                  <AlertCircle size={19} />
                  <h3>
                    Skills to review <span>{missingSkills.length}</span>
                  </h3>
                </div>
                <p className="card-description">
                  Mention these only if you genuinely have the skills.
                </p>
                <div className="skill-list">
                  {missingSkills.length ? (
                    missingSkills.map((skill) => (
                      <span className="skill missing" key={skill}>
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="empty-state">No missing skills detected.</p>
                  )}
                </div>
              </article>
            </div>

            {suggestions.length > 0 && (
              <article className="result-card suggestions-card">
                <div className="card-title">
                  <Sparkles size={19} />
                  <h3>Recommended next steps</h3>
                </div>
                <ul className="suggestions">
                  {suggestions.slice(0, 4).map((suggestion, index) => (
                    <li key={`${index}-${suggestion}`}>{suggestion}</li>
                  ))}
                </ul>
              </article>
            )}

            <div className="dashboard-actions">
              <button
                className="analyze-button download-button"
                type="button"
                onClick={downloadReport}
                disabled={downloading}
              >
                {downloading ? (
                  <>
                    <RefreshCw className="spin" size={17} /> Preparing report...
                  </>
                ) : (
                  <>
                    <Download size={17} /> Download PDF report
                  </>
                )}
              </button>
              <button
                className="secondary-button"
                type="button"
                onClick={resetAnalyzer}
              >
                Analyze another resume
              </button>
            </div>

            {error && (
              <div className="error-message">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}

            <div className="more-details">
              <h2>More resume insights</h2>
              <p className="details-hint">
                Open a section only when you need more detail.
              </p>

              {(matchedKeywords.length > 0 || missingKeywords.length > 0) && (
                <details className="detail-panel">
                  <summary>Job description keywords</summary>
                  <div className="comparison-grid compact-grid">
                    <div>
                      <h4>Matched keywords</h4>
                      <div className="skill-list">
                        {matchedKeywords.length ? (
                          matchedKeywords.map((word) => (
                            <span className="skill matched" key={word}>
                              {word}
                            </span>
                          ))
                        ) : (
                          <p className="empty-state">None detected.</p>
                        )}
                      </div>
                    </div>
                    <div>
                      <h4>Missing keywords</h4>
                      <div className="skill-list">
                        {missingKeywords.length ? (
                          missingKeywords.map((word) => (
                            <span className="skill missing" key={word}>
                              {word}
                            </span>
                          ))
                        ) : (
                          <p className="empty-state">None detected.</p>
                        )}
                      </div>
                    </div>
                  </div>
                </details>
              )}

              {results.sections && (
                <details className="detail-panel">
                  <summary>Resume section check</summary>
                  <div className="section-grid">
                    {Object.entries(SECTION_LABELS).map(([key, label]) => {
                      const found = Boolean(sectionData[key]?.found);
                      return (
                        <div className="section-item" key={key}>
                          <span>{label}</span>
                          <strong className={found ? "found" : "not-found"}>
                            {found ? "Detected" : "Not detected"}
                          </strong>
                        </div>
                      );
                    })}
                  </div>
                  <p className="section-summary">
                    {sectionSummary.detected_sections ?? 0} of{" "}
                    {sectionSummary.total_sections ??
                      Object.keys(SECTION_LABELS).length}{" "}
                    sections detected
                  </p>
                </details>
              )}

              {results.sections && (
                <details className="detail-panel">
                  <summary>Contact information check</summary>
                  <div className="contact-grid">
                    <div className="contact-item">
                      <Mail size={16} />
                      <span>{contactInfo.email || "Email not detected"}</span>
                    </div>
                    <div className="contact-item">
                      <Phone size={16} />
                      <span>{contactInfo.phone || "Phone not detected"}</span>
                    </div>
                    <div className="contact-item">
                      <Contact size={16} />
                      <span>
                        {contactInfo.linkedin || "LinkedIn not detected"}
                      </span>
                    </div>
                    <div className="contact-item">
                      <Code size={16} />
                      <span>{contactInfo.github || "GitHub not detected"}</span>
                    </div>
                  </div>
                </details>
              )}

              <details className="detail-panel">
                <summary>
                  All skills found in your resume ({resumeSkills.length})
                </summary>
                <div className="skill-list detail-skill-list">
                  {resumeSkills.length ? (
                    resumeSkills.map((skill) => (
                      <span className="skill neutral-skill" key={skill}>
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p className="empty-state">No skills detected.</p>
                  )}
                </div>
              </details>
            </div>

            <p className="disclaimer">
              ResumeIQ uses experimental rule-based skill matching and TF-IDF
              text similarity. It does not provide an official ATS score or a
              hiring decision. Add a missing skill to your resume only when it
              accurately reflects your abilities.
            </p>
          </section>
        )}
      </main>

      <footer>
        <p>
          ResumeIQ © 2026 · Built with React & Python · Developed by Lashini
          Chamodi
        </p>
      </footer>
    </div>
  );
}

export default App;
