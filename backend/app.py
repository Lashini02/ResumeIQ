from section_detector import detect_resume_sections
from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp_analyzer import analyze_job_match
from flask import send_file
from report_generator import generate_analysis_report
import fitz
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "ResumeIQ Backend is running!"
    })
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

SKILLS = [
    "python", "java", "javascript", "typescript",
    "react", "node.js", "flask", "django",
    "html", "css", "sql", "mysql", "mongodb",
    "excel", "power bi", "tableau",
    "machine learning", "data analysis",
    "communication", "teamwork", "problem solving",
    "project management", "business analysis",
    "requirements gathering", "agile", "scrum",
    "jira", "manual testing", "automation testing",
    "selenium", "playwright", "api testing",
    "cybersecurity", "networking", "linux",
    "penetration testing", "ethical hacking",
    "risk management", "aws", "docker",
    "git", "github", "c++", "c#",
    "postman", "figma", "rest api"
]


def extract_resume_text(file_bytes):
    """Extract text from an uploaded PDF in memory."""

    pdf = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    try:
        if pdf.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        text = ""

        for page in pdf:
            text += page.get_text() + "\n"

        return text.strip()

    finally:
        pdf.close()


def extract_skills(text):
    """Identify skills from the supplied text."""

    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = (
            r"(?<!\w)" +
            re.escape(skill.lower()) +
            r"(?!\w)"
        )

        if re.search(pattern, text):
            found.append(skill)

    return found


def get_similarity(resume_text, job_description):
    """Calculate TF-IDF cosine similarity."""

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        vectors = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        score = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(float(score) * 100, 2)

    except ValueError:
        return 0


def analyze_resume(resume_text, job_description):

    # Run improved NLP analysis
    analysis = analyze_job_match(
        resume_text,
        job_description
    )

    # Detect resume sections
    analysis["sections"] = detect_resume_sections(
        resume_text
    )

    return analysis



@app.route("/api/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return jsonify({
            "error": "Please upload a resume."
        }), 400

    resume = request.files["resume"]

    job_description = request.form.get(
        "job_description", ""
    ).strip()

    if not resume.filename:
        return jsonify({
            "error": "Please select a PDF file."
        }), 400

    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported."
        }), 400

    if not job_description:
        return jsonify({
            "error": "Please enter a job description."
        }), 400

    if len(job_description.split()) < 5:
        return jsonify({
            "error": "Please enter a more detailed job description."
        }), 400

    try:
        file_bytes = resume.read()

        if not file_bytes.startswith(b"%PDF-"):
            return jsonify({
                "error": "Invalid PDF file."
            }), 400

        resume_text = extract_resume_text(file_bytes)

        if len(resume_text) < 30:
            return jsonify({
                "error": "Could not extract text. "
                         "This may be a scanned PDF."
            }), 400

        results = analyze_resume(
            resume_text,
            job_description
        )

        results["filename"] = resume.filename

        return jsonify(results)

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "PDF must be smaller than 5 MB."
    }), 413


@app.route("/api/report", methods=["POST"])
def download_report():

    try:
        # Get uploaded resume and job description
        resume_file = request.files.get("resume")
        job_description = request.form.get("job_description", "")

        if not resume_file:
            return jsonify({
                "error": "Please upload a resume."
            }), 400

        if not resume_file.filename.lower().endswith(".pdf"):
            return jsonify({
                "error": "Only PDF files are supported."
            }), 400

        if not job_description.strip():
            return jsonify({
                "error": "Please enter a job description."
            }), 400

        # Read PDF and extract text
        file_bytes = resume_file.read()

        if not file_bytes.startswith(b"%PDF-"):
            return jsonify({
                "error": "Invalid PDF file."
            }), 400

        resume_text = extract_resume_text(file_bytes)

        if len(resume_text.strip()) < 30:
            return jsonify({
                "error": "Could not extract enough text from this PDF."
            }), 400

        # Run the same analysis used by the application
        analysis = analyze_resume(
            resume_text,
            job_description
        )

        # Generate PDF report
        pdf_buffer = generate_analysis_report(
            resume_file.filename,
            analysis
        )

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="ResumeIQ_Analysis_Report.pdf"
        )

    except Exception as error:
        print("PDF report error:", error)

        return jsonify({
            "error": "Unable to generate the PDF report."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
