
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Canonical skill names and common variations.
# Add more skills and variations as the project grows.
SKILL_ALIASES = {
    # --------------------------------------------------------------------------
    # EXISTING BASE SKILLS
    # --------------------------------------------------------------------------
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "flask": ["flask"],
    "django": ["django"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "excel": ["excel", "microsoft excel", "ms excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "communication": ["communication", "communication skills", "verbal communication", "written communication"],
    "teamwork": ["teamwork", "team work", "collaboration", "cross functional collaboration"],
    "problem solving": ["problem solving", "problem-solving", "analytical problem solving", "complex problem solving"],
    "project management": ["project management", "project planning"],
    "business analysis": ["business analysis", "ba"],
    "requirements gathering": [
        "requirements gathering",
        "requirement gathering",
        "requirements elicitation",
        "requirements analysis"
    ],
    "agile": ["agile", "agile methodologies", "agile practices"],
    "scrum": ["scrum", "scrum framework"],
    "jira": ["jira"],
    "manual testing": ["manual testing"],
    "automation testing": ["automation testing", "test automation", "ui automation testing"],
    "selenium": ["selenium", "selenium webdriver"],
    "playwright": ["playwright"],
    "api testing": ["api testing", "api test", "api test automation"],
    "cybersecurity": ["cybersecurity", "cyber security", "information security"],
    "networking": ["networking", "computer networking", "network security"],
    "linux": ["linux", "linux os"],
    "penetration testing": ["penetration testing", "pentesting", "pen testing"],
    "ethical hacking": ["ethical hacking"],
    "risk management": ["risk management", "risk assessment"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "git": ["git"],
    "github": ["github"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp"],
    "postman": ["postman"],
    "figma": ["figma"],
    "rest api": ["rest api", "restful api", "rest apis", "restful apis"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED TECHNICAL & DEVOPS SKILLS
    # --------------------------------------------------------------------------
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": ["ci/cd", "cicd", "continuous integration", "continuous deployment"],
    "terraform": ["terraform"],
    "jenkins": ["jenkins"],
    "microservices": ["microservices", "microservices architecture"],
    "system design": ["system design", "software architecture"],
    "postgresql": ["postgresql", "postgres"],
    "redis": ["redis"],
    "graphql": ["graphql"],
    "golang": ["golang", "go"],
    "rust": ["rust"],
    "ruby": ["ruby", "ruby on rails"],
    "php": ["php"],
    "laravel": ["laravel"],
    "nestjs": ["nestjs", "nest.js"],
    "tailwind css": ["tailwind css", "tailwind"],
    "bash scripting": ["bash scripting", "shell scripting", "bash"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED QA & TESTING SKILLS
    # --------------------------------------------------------------------------
    "cypress": ["cypress"],
    "jmeter": ["jmeter", "apache jmeter"],
    "appium": ["appium"],
    "regression testing": ["regression testing"],
    "integration testing": ["integration testing"],
    "unit testing": ["unit testing"],
    "smoke testing": ["smoke testing", "sanity testing"],
    "user acceptance testing": ["user acceptance testing", "uat"],
    "performance testing": ["performance testing", "load testing"],
    "security testing": ["security testing"],
    "test planning": ["test planning", "test strategy"],
    "test case design": ["test case design", "test execution"],
    "defect management": ["defect management", "bug tracking", "defect triage"],
    "bdd": ["bdd", "behavior driven development", "bdd framework"],
    "tdd": ["tdd", "test driven development"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED MOBILE & UI/UX SKILLS
    # --------------------------------------------------------------------------
    "flutter": ["flutter"],
    "react native": ["react native"],
    "swift": ["swift", "ios development"],
    "kotlin": ["kotlin", "android development"],
    "ui/ux design": ["ui/ux design", "ui ux", "user interface design", "user experience design"],
    "user research": ["user research", "wireframing"],
    "product management": ["product management"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED DATA SCIENCE & AI SKILLS
    # --------------------------------------------------------------------------
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv"],
    "prompt engineering": ["prompt engineering"],
    "etl": ["etl", "etl pipelines", "data warehousing"],
    "snowflake": ["snowflake"],
    "big data": ["big data", "apache spark", "spark"],
    "data visualization": ["data visualization", "dashboard creation"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED HUMAN RESOURCES (HR) SKILLS
    # --------------------------------------------------------------------------
    "talent acquisition": ["talent acquisition", "full cycle recruiting", "recruitment"],
    "technical sourcing": ["technical sourcing", "candidate screening"],
    "applicant tracking systems": ["applicant tracking systems", "ats management", "ats"],
    "employee onboarding": ["employee onboarding", "employee offboarding"],
    "employee engagement": ["employee engagement", "employee retention"],
    "performance management": ["performance management", "performance reviews"],
    "payroll administration": ["payroll administration", "compensation and benefits"],
    "hr compliance": ["hr compliance", "labor laws knowledge"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED DIGITAL MARKETING SKILLS
    # --------------------------------------------------------------------------
    "seo": ["seo", "search engine optimization"],
    "sem": ["sem", "search engine marketing", "google ads", "ppc"],
    "social media marketing": ["social media marketing", "smm"],
    "content marketing": ["content marketing", "copywriting", "content creation"],
    "email marketing": ["email marketing", "mailchimp"],
    "google analytics": ["google analytics", "ga4", "digital analytics"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED BUSINESS & ENTERPRISE TOOLS
    # --------------------------------------------------------------------------
    "sap": ["sap"],
    "salesforce": ["salesforce"],
    "hubspot": ["hubspot"],
    "financial modeling": ["financial modeling", "budgeting", "forecasting"],
    "supply chain management": ["supply chain management"],
    "sdlc": ["sdlc", "software development life cycle"],

    # --------------------------------------------------------------------------
    # NEWLY ADDED UNIVERSAL SOFT SKILLS
    # --------------------------------------------------------------------------
    "critical thinking": ["critical thinking", "logical reasoning"],
    "adaptability": ["adaptability", "flexibility", "adaptability to change"],
    "time management": ["time management", "prioritization", "task prioritization"],
    "conflict resolution": ["conflict resolution", "conflict management"],
    "stakeholder management": ["stakeholder management", "stakeholder interaction"],
    "technical writing": ["technical writing", "technical documentation"],
    "presentation skills": ["presentation skills"],
    "emotional intelligence": ["emotional intelligence", "eq"],
    "attention to detail": ["attention to detail"],
    "decision making": ["decision making"],
    "leadership": ["leadership", "mentorship", "coaching"]

}


def normalize_text(text):
    """Convert text into a consistent lowercase format."""
    return re.sub(r"\s+", " ", text.lower()).strip()


def contains_term(text, term):
    """Check for a term without matching it inside another word."""
    pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
    return re.search(pattern, text, re.IGNORECASE) is not None


def extract_skills(text):
    """Identify recognized skills using canonical names and aliases."""
    normalized = normalize_text(text)
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        terms = [skill] + aliases

        if any(contains_term(normalized, term) for term in terms):
            found_skills.append(skill)

    return sorted(set(found_skills))


def extract_keywords(job_description, limit=15):
    """
    Extract useful single-word and two-word keywords
    from a job description using TF-IDF.
    """
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=100
        )

        matrix = vectorizer.fit_transform([job_description])

        terms = vectorizer.get_feature_names_out()
        scores = matrix.toarray()[0]

        ranked_terms = sorted(
            zip(terms, scores),
            key=lambda item: item[1],
            reverse=True
        )

        keywords = []

        for term, score in ranked_terms:
            if len(term) > 2 and term not in keywords:
                keywords.append(term)

            if len(keywords) >= limit:
                break

        return keywords

    except ValueError:
        return []


def calculate_text_similarity(resume_text, job_description):
    """Calculate TF-IDF cosine similarity as a percentage."""
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        vectors = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        return 0.0


def analyze_job_match(resume_text, job_description):
    """Perform skill matching, keyword analysis and scoring."""

    resume_normalized = normalize_text(resume_text)
    job_normalized = normalize_text(job_description)

    resume_skills = extract_skills(resume_normalized)
    job_skills = extract_skills(job_normalized)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    job_keywords = extract_keywords(job_description)

    matched_keywords = [
        keyword for keyword in job_keywords
        if contains_term(resume_normalized, keyword)
    ]

    missing_keywords = [
        keyword for keyword in job_keywords
        if keyword not in matched_keywords
    ]

    similarity = calculate_text_similarity(
        resume_text,
        job_description
    )

    # Give skill coverage more weight than text similarity.
    if job_skills:
        skill_coverage = (
            len(matched_skills) / len(job_skills)
        ) * 100

        score = (
            skill_coverage * 0.70
            + similarity * 0.30
        )
    else:
        score = similarity

    suggestions = []

    if missing_skills:
        suggestions.append(
            "Review the missing skills and add them only "
            "if you genuinely possess those skills."
        )

    if missing_keywords:
        suggestions.append(
            "Review the missing job-description keywords. "
            "Include relevant terms naturally where they "
            "accurately describe your experience."
        )

    if len(resume_text.split()) < 150:
        suggestions.append(
            "Consider adding more relevant details about "
            "your education, projects and experience."
        )

    if not resume_skills:
        suggestions.append(
            "Add a clearly labelled Skills section to your resume."
        )

    if not suggestions:
        suggestions.append(
            "Your resume contains several relevant skills. "
            "Continue tailoring it to the specific job description."
        )

    return {
        "score": round(score, 2),
        "similarity": similarity,
        "job_skills": job_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "job_keywords": job_keywords,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "word_count": len(resume_text.split())
    }
