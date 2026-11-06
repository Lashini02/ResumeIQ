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
    "postman", "figma", "rest api", 
    # Cloud & DevOps
    "azure", "gcp", "kubernetes", "ci/cd", "terraform", "jenkins", "microservices", "system design",
    # Data & AI
    "postgresql", "redis", "deep learning", "nlp", "prompt engineering", "etl", "snowflake", "big data",
    # QA & Security
    "cypress", "jmeter", "appium", "splunk", "bash scripting", "cloud security",
    # UI/UX & Product
    "ui/ux design", "user research", "product management", "sdlc",
    # Universal Soft Skills
    "critical thinking", "emotional intelligence", "adaptability", "time management",
    "conflict resolution", "stakeholder management", "technical writing", "presentation skills", "negotiation",# Mobile Dev
    "flutter", "react native", "swift", "kotlin", "ionic",
    # Digital Marketing
    "seo", "sem", "social media marketing", "content marketing", "google analytics",
    # Business & Enterprise
    "sap", "salesforce", "hubspot", "financial modeling", "budgeting", "supply chain management",
    # Languages & Tech
    "golang", "rust", "ruby", "php", "laravel", "nestjs", "tailwind css", "serverless", "websockets",
    # Additional Soft Skills
    "attention to detail", "decision making", "stress management", "work ethic",
    "remote collaboration", "cultural awareness","functional testing",
    "regression testing",
    "integration testing",
    "unit testing",
    "smoke testing",
    "user acceptance testing",
    "performance testing",
    "load testing",
    "security testing",
    "penetration testing",
    "cross browser testing",
    "mobile testing",
    "exploratory testing",
    "bug tracking",
    "test planning",
    "test strategy",
    "test execution",
    "test case design",
    "test data management",
    "defect management",
    "root cause analysis",
    "continuous integration",
    "continuous deployment",
    "version control",
    "object oriented programming",
    "data structures",
    "algorithms",
    "code review",
    "software architecture",
    "cloud computing",
    "database management",
    "data modeling",
    "business logic analysis",
    "analytical thinking",
    "strategic planning",
    "resource management",
    "time management",
    "crisis management",
    "client communication",
    "stakeholder interaction",
    # Domain Knowledge & Fundamentals
    "domain knowledge",
    "business domain understanding",
    "software development life cycle knowledge",
    "testing lifecycle knowledge",
    "relational database knowledge",
    "nosql database knowledge",
    "system architecture understanding",
    "technical documentation knowledge",

    # Testing & Automation Techniques
    "api test automation",
    "ui automation testing",
    "backend testing",
    "frontend testing",
    "end to end testing",
    "smoke and sanity testing",
    "black box testing",
    "white box testing",
    "gray box testing",
    "bdd framework",
    "tdd methodology",
    "test automation framework design",

    # Problem Solving & Soft Skills
    "analytical problem solving",
    "complex problem solving",
    "troubleshooting skills",
    "debugging capabilities",
    "effective communication",
    "interpersonal skills",
    "cross functional collaboration",
    "adaptability to change",

    # Methodologies & Management
    "scrum framework understanding",
    "kanban methodology",
    "agile practices",
    "sprint planning",
    "defect triage management"

  
        "object oriented programming", "oop concepts", "data structures", "algorithms",
        "system design", "microservices architecture", "restful apis", "graphql",
        "design patterns", "clean code", "code review", "refactoring",
        "unit testing", "integration testing", "test driven development", "tdd",
        "behavior driven development", "bdd", "front end development", "back end development",
        "full stack development", "responsive design", "web performance optimization",
        "ci/cd pipelines", "continuous integration", "continuous deployment",
        "containerization", "infrastructure as code", "serverless architecture",
        "cloud native development", "version control management", "git workflow",
        "semantic versioning", "technical documentation", "api documentation"
    ,

    # --------------------------------------------------------------------------
    # 2. QA & AUTOMATION TESTING
    # --------------------------------------------------------------------------
    
        "manual testing", "automation testing", "api testing", "ui testing",
        "backend testing", "performance testing", "load testing", "stress testing",
        "security testing", "regression testing", "smoke testing", "sanity testing",
        "exploratory testing", "user acceptance testing", "uat", "cross browser testing",
        "mobile automation testing", "framework development", "page object model",
        "test strategy design", "test plan creation", "test case design",
        "test execution", "test data management", "defect management",
        "bug tracking", "root cause analysis", "test automation maintenance"
    ,

    # --------------------------------------------------------------------------
    # 3. DATA SCIENCE, AI & ANALYTICS
    # --------------------------------------------------------------------------
   
        "data analysis", "data visualization", "data modeling", "data warehousing",
        "etl pipeline development", "big data processing", "predictive analytics",
        "statistical analysis", "machine learning algorithms", "deep learning models",
        "natural language processing", "nlp", "computer vision", "prompt engineering",
        "feature engineering", "model training", "model deployment", "model evaluation",
        "business intelligence", "dashboard creation", "exploratory data analysis",
        "data cleaning", "data normalization", "a/b testing analysis"
    ,

    # --------------------------------------------------------------------------
    # 4. CYBERSECURITY & NETWORKING
    # --------------------------------------------------------------------------
    
        "vulnerability assessment", "penetration testing", "ethical hacking",
        "network security", "cloud security", "application security",
        "threat intelligence", "incident response", "security auditing",
        "identity and access management", "iam", "risk assessment",
        "siem monitoring", "firewall configuration", "cryptography fundamentals",
        "zero trust architecture", "compliance standards", "network troubleshooting"
    ,

    # --------------------------------------------------------------------------
    # 5. HUMAN RESOURCES (HR) & RECRUITMENT
    # --------------------------------------------------------------------------
    
        "talent acquisition", "full cycle recruiting", "technical sourcing",
        "candidate screening", "interview scheduling", "applicant tracking systems",
        "ats management", "employer branding", "employee onboarding",
        "employee offboarding", "employee engagement", "employee retention",
        "performance management", "performance reviews", "compensation and benefits",
        "payroll administration", "hr compliance", "labor laws knowledge",
        "conflict resolution", "hris management", "organizational development",
        "succession planning", "training and development", "exit interviews"
    ,

    # --------------------------------------------------------------------------
    # 6. MARKETING & DIGITAL STRATEGY
    # --------------------------------------------------------------------------
    
        "search engine optimization", "seo", "search engine marketing", "sem",
        "pay per click", "ppc advertising", "social media marketing", "smm",
        "content marketing strategy", "copywriting", "content creation",
        "email marketing campaigns", "marketing automation", "growth hacking",
        "brand strategy", "brand positioning", "conversion rate optimization", "cro",
        "lead generation", "customer acquisition", "funnel optimization",
        "market research", "competitor analysis", "digital analytics",
        "campaign management", "influencer marketing", "public relations", "pr strategy"
    ,

    # --------------------------------------------------------------------------
    # 7. BUSINESS ANALYSIS & PROJECT MANAGEMENT
    # --------------------------------------------------------------------------
   
        "requirements gathering", "requirements analysis", "business process modeling",
        "gap analysis", "feasibility study", "functional specification creation",
        "user story creation", "backlog grooming", "sprint planning",
        "agile methodologies", "scrum framework", "kanban framework",
        "project planning", "scope management", "resource allocation",
        "risk management", "stakeholder management", "change management",
        "budget planning", "cost estimation", "vendor management","excel","jira","confluence","trello","MS word","MS powerpoint","MS excel","api"
        "sql","nosql","postgresql","mongodb","redis","data analysis","data visualization","data modeling","data warehousing","etl pipeline development","big data processing","predictive analytics","statistical analysis","machine learning algorithms","deep learning models"
    ,

    # --------------------------------------------------------------------------
    # 8. UNIVERSAL SOFT SKILLS (ඕනෑම Field එකකට ගැළපෙන)
    # --------------------------------------------------------------------------
   
        "analytical thinking", "critical thinking", "logical reasoning",
        "complex problem solving", "decision making", "troubleshooting",
        "effective communication", "verbal communication", "written communication",
        "technical writing", "active listening", "presentation skills",
        "interpersonal skills", "cross functional collaboration", "teamwork",
        "conflict management", "negotiation skills", "stakeholder alignment",
        "time management", "task prioritization", "adaptability",
        "flexibility", "emotional intelligence", "eq", "leadership",
        "mentorship", "coaching", "ownership mindset", "attention to detail",
        "work ethic", "stress management", "remote work collaboration","support","customer service","customer support","customer success","client communication","client relationship management"
        "good communication skills","problem solving","team player","adaptability","time management","critical thinking","leadership skills","interpersonal skills","conflict resolution","decision making","emotional intelligence","negotiation skills","presentation skills","collaboration skills"
        "AI driven tools","AI tools","AI applications","AI technologies","AI platforms","AI frameworks","AI libraries","AI algorithms","AI models","AI solutions","AI systems","AI research","AI development","AI implementation","AI integration"
        "english","spanish","french","german","mandarin","japanese","korean","italian","portuguese","russian","arabic","hindi","bengali","urdu","tamil","telugu","marathi","gujarati","punjabi"
        "digital marketing","social media marketing","content marketing","email marketing","search engine optimization","pay per click","affiliate marketing","inbound marketing","outbound marketing","marketing automation","crm","salesforce","hubspot","zoho","microsoft dynamics","pipedrive","marketo","pardot","mailchimp","constant contact","activecampaign","drip","getresponse","aweber","campaign monitor","sendinblue","convertkit"
        "SEO","SEM","PPC","CRO","content strategy","content creation","content distribution","content optimization","keyword research","link building","on page SEO","off page SEO","technical SEO","local SEO","mobile SEO","voice search optimization","video marketing","influencer marketing","brand management","brand strategy","brand identity"
        "sales","sales strategy","sales process","sales pipeline","lead generation","lead nurturing","lead scoring","customer relationship management","crm software","salesforce automation","sales analytics","sales forecasting","sales enablement","sales training","sales coaching"
        "coordination","organization","planning","prioritization","problem solving","decision making","critical thinking","creativity","innovation","adaptability","flexibility","resilience","emotional intelligence","communication skills","interpersonal skills","teamwork","collaboration","leadership skills"
        "introvert","extrovert","ambivert","analytical","creative","strategic","tactical","detail oriented","big picture thinker","problem solver","decision maker","innovative","adaptable","flexible","resilient","empathetic","assertive"
        "requirements gathering","requirements analysis","business process modeling","gap analysis","feasibility study","functional specification creation","user story creation","backlog grooming","sprint planning","agile methodologies","scrum framework","kanban framework"
    
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
