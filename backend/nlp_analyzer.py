
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Canonical skill names and common variations.
# Add more skills and variations as the project grows.
SKILL_ALIASES = {
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "react.js"],
    "node.js": ["node.js", "nodejs", "node"],
    "flask": ["flask"],
    "django": ["django"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo db"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "communication": ["communication", "communication skills"],
    "teamwork": ["teamwork", "team work"],
    "problem solving": ["problem solving", "problem-solving"],
    "project management": ["project management"],
    "business analysis": ["business analysis"],
    "requirements gathering": [
        "requirements gathering",
        "requirement gathering",
        "requirements elicitation"
    ],
    "agile": ["agile"],
    "scrum": ["scrum"],
    "jira": ["jira"],
    "manual testing": ["manual testing"],
    "automation testing": ["automation testing", "test automation"],
    "selenium": ["selenium"],
    "playwright": ["playwright"],
    "api testing": ["api testing", "api test"],
    "cybersecurity": ["cybersecurity", "cyber security"],
    "networking": ["networking", "computer networking"],
    "linux": ["linux"],
    "penetration testing": ["penetration testing", "pentesting"],
    "ethical hacking": ["ethical hacking"],
    "risk management": ["risk management"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "git": ["git"],
    "github": ["github"],
    "c++": ["c++"],
    "c#": ["c#"],
    "postman": ["postman"],
    "figma": ["figma"],
    "rest api": ["rest api", "restful api"]
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
