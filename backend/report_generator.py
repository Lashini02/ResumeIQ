
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


def generate_analysis_report(filename, analysis):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontSize=25,
        leading=30,
        textColor=colors.HexColor("#4338CA"),
        alignment=TA_CENTER,
        spaceAfter=8
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#312E81"),
        spaceBefore=12,
        spaceAfter=7
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14
    ))

    story = []

    # Title
    story.append(Paragraph("ResumeIQ", styles["ReportTitle"]))

    story.append(Paragraph(
        "Resume Analysis Report",
        styles["Heading2"]
    ))

    story.append(Spacer(1, 8))

    # Report information
    story.append(Paragraph(
        f"<b>Resume:</b> {filename}",
        styles["SmallText"]
    ))

    story.append(Paragraph(
        f"<b>Analysis Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles["SmallText"]
    ))

    story.append(Spacer(1, 15))

    # Match score
    score = analysis.get("score", 0)
    similarity = analysis.get("similarity", 0)

    score_data = [
        ["Resume Match Score", "Text Similarity"],
        [f"{score}%", f"{similarity}%"]
    ]

    score_table = Table(
        score_data,
        colWidths=[80 * mm, 80 * mm]
    )

    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#E0E7FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0),
         colors.HexColor("#312E81")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.lightgrey)
    ]))

    story.append(score_table)

    # Skills
    def add_list_section(title, items):

        story.append(Paragraph(
            title,
            styles["SectionHeading"]
        ))

        if items:
            for item in items:
                story.append(Paragraph(
                    f"&bull; {item}",
                    styles["SmallText"]
                ))
        else:
            story.append(Paragraph(
                "No items identified.",
                styles["SmallText"]
            ))

    add_list_section(
        "Matched Skills",
        analysis.get("matched_skills", [])
    )

    add_list_section(
        "Missing Skills",
        analysis.get("missing_skills", [])
    )

    add_list_section(
        "Matched Job Keywords",
        analysis.get("matched_keywords", [])
    )

    add_list_section(
        "Missing Job Keywords",
        analysis.get("missing_keywords", [])
    )

    # Resume sections
    story.append(Paragraph(
        "Resume Section Analysis",
        styles["SectionHeading"]
    ))

    sections = analysis.get("sections", {})

    section_labels = {
        "professional_summary": "Professional Summary",
        "technical_skills": "Technical Skills",
        "work_experience": "Work Experience",
        "education": "Education",
        "projects": "Projects",
        "certifications": "Certifications",
        "achievements": "Achievements",
        "additional_information": "Additional Information"
    }

    section_data = [["Resume Section", "Status", "Word Count"]]

    for key, label in section_labels.items():

        details = sections.get(key, {})

        found = details.get("found", False)
        word_count = details.get("word_count", 0)

        section_data.append([
            label,
            "Detected" if found else "Not Detected",
            str(word_count)
        ])

    section_table = Table(
        section_data,
        colWidths=[85 * mm, 45 * mm, 30 * mm],
        repeatRows=1
    )

    section_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#E0E7FF")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4,
         colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(section_table)

    # Suggestions
    add_list_section(
        "Improvement Suggestions",
        analysis.get("suggestions", [])
    )

    # Disclaimer
    story.append(Spacer(1, 15))
    story.append(HRFlowable(
        width="100%",
        color=colors.lightgrey
    ))

    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Disclaimer:</b> ResumeIQ provides an experimental "
        "resume-to-job-description matching analysis. The score "
        "is based on keyword matching and text similarity. "
        "It is not an official ATS score or a guarantee of "
        "employment suitability. Missing skills should only "
        "be added when they accurately reflect your abilities.",
        styles["SmallText"]
    ))

    document.build(story)

    buffer.seek(0)

    return buffer
