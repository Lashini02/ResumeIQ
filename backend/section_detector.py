
import re


# Different heading names that may appear in resumes
SECTION_ALIASES = {
    "professional_summary": [
        "professional summary",
        "career summary",
        "profile summary",
        "summary",
        "profile",
        "career objective",
        "objective",
        "about me"
    ],
    "technical_skills": [
        "technical skills",
        "technical expertise",
        "skills",
        "key skills",
        "core competencies",
        "technical knowledge",
        "areas of expertise"
    ],
    "work_experience": [
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "experience",
        "internship experience"
    ],
    "education": [
        "education",
        "educational qualifications",
        "academic qualifications",
        "academic background",
        "education background"
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "project experience"
    ],
    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "courses",
        "licenses and certifications"
    ],
    "achievements": [
        "achievements",
        "awards",
        "honors and awards",
        "accomplishments"
    ],
    "additional_information": [
        "additional information",
        "additional details",
        "interests",
        "hobbies",
        "languages",
        "references"
    ]
}


def normalize_heading(line):
    """Normalize a possible resume heading."""
    line = line.strip().lower()

    # Remove common heading punctuation
    line = re.sub(r"[:\-–—]+$", "", line)

    # Remove numbering such as 1. Skills or 02. Education
    line = re.sub(r"^\d+[\.\)]\s*", "", line)

    return line.strip()


def detect_contact_information(text):
    """Find basic contact details in extracted resume text."""

    email = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    phone = re.findall(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
        text
    )

    linkedin = re.findall(
        r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+",
        text,
        re.IGNORECASE
    )

    github = re.findall(
        r"(?:https?://)?(?:www\.)?github\.com/[^\s]+",
        text,
        re.IGNORECASE
    )

    return {
        "found": bool(email or phone or linkedin or github),
        "email_found": bool(email),
        "phone_found": bool(phone),
        "linkedin_found": bool(linkedin),
        "github_found": bool(github)
    }


def detect_resume_sections(text):
    """
    Detect common resume sections using their headings.

    Returns section presence, word counts and short previews.
    """

    lines = text.splitlines()

    # Prepare all recognized headings
    heading_lookup = {}

    for section_name, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            heading_lookup[alias] = section_name

    detected_content = {}
    current_section = None

    for line in lines:
        cleaned_line = normalize_heading(line)

        # Check whether this line is a recognized heading
        matched_section = heading_lookup.get(cleaned_line)

        if matched_section:
            current_section = matched_section

            if current_section not in detected_content:
                detected_content[current_section] = []

            continue

        # Add text to the currently active section
        if current_section and line.strip():
            detected_content[current_section].append(line.strip())

    # Build a consistent result, including missing sections
    results = {}

    for section_name in SECTION_ALIASES:
        content_lines = detected_content.get(section_name, [])
        content = " ".join(content_lines).strip()

        words = content.split()

        results[section_name] = {
            "found": section_name in detected_content,
            "word_count": len(words),
            "preview": content[:250]
        }

    # Contact details are detected separately because
    # they often appear without a "Contact Information" heading.
    results["contact_information"] = detect_contact_information(text)

    detected_count = sum(
        1 for name in SECTION_ALIASES
        if results[name]["found"]
    )

    results["summary"] = {
        "detected_sections": detected_count,
        "total_sections": len(SECTION_ALIASES),
        "contact_information_found": results["contact_information"]["found"]
    }

    return results