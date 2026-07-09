"""
reports/report_generator.py
Generates a professional PDF career report combining resume score,
skill gap, salary prediction, recommendations, and trending market skills.
Uses ReportLab for layout-controlled, multi-page PDF output.
"""

import logging
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BRAND_BLUE = colors.HexColor("#185FA5")
LIGHT_BLUE = colors.HexColor("#E6F1FB")
DARK_TEXT = colors.HexColor("#0B0B0B")
MUTED_TEXT = colors.HexColor("#5F5E5A")
SUCCESS = colors.HexColor("#27500A")
DANGER = colors.HexColor("#791F1F")


def _styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle("CPTitle", fontSize=22, leading=26, textColor=BRAND_BLUE, spaceAfter=4))
    base.add(ParagraphStyle("CPSubtitle", fontSize=11, textColor=MUTED_TEXT, spaceAfter=14))
    base.add(ParagraphStyle("CPHeading", fontSize=14, leading=18, textColor=DARK_TEXT, spaceBefore=16, spaceAfter=8))
    base.add(ParagraphStyle("CPBody", fontSize=10, leading=15, textColor=DARK_TEXT))
    base.add(ParagraphStyle("CPScore", fontSize=36, leading=40, textColor=BRAND_BLUE, alignment=1))
    base.add(ParagraphStyle("CPScoreLabel", fontSize=10, textColor=MUTED_TEXT, alignment=1))
    return base


def generate_career_report(
    output_path: str,
    user_name: str,
    target_role: str,
    career_score: float,
    resume_match_pct: float,
    matched_skills: list,
    missing_skills: list,
    predicted_salary: dict,
    recommendations: list,
    trending_skills: list,
):
    """
    Builds the full multi-section PDF career report.

    predicted_salary: dict with keys predicted_salary_lpa, range_low, range_high
    recommendations: list of dicts with keys skill, name, platform, is_free, weeks, priority
    trending_skills: list of (skill_name, demand_pct) tuples
    """
    styles = _styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    )
    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story.append(Paragraph("CareerPulse AI", styles["CPTitle"]))
    story.append(Paragraph(
        f"AI-Generated Career Report for <b>{user_name}</b> &nbsp;|&nbsp; "
        f"Target role: {target_role} &nbsp;|&nbsp; Generated on {date.today().strftime('%d %b %Y')}",
        styles["CPSubtitle"],
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#D3D1C7")))

    # ── Career score block ──────────────────────────────────────────────────
    story.append(Spacer(1, 14))
    score_table = Table(
        [[Paragraph(f"{career_score}", styles["CPScore"]), Paragraph(f"{resume_match_pct}%", styles["CPScore"])],
         [Paragraph("Career score / 100", styles["CPScoreLabel"]), Paragraph("Resume match", styles["CPScoreLabel"])]],
        colWidths=[8 * cm, 8 * cm],
    )
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#B5D4F4")),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(score_table)

    # ── Skill gap section ───────────────────────────────────────────────────
    story.append(Paragraph("Skill gap analysis", styles["CPHeading"]))
    skill_rows = [["Matched skills (found in resume)", "Missing skills (required by market)"]]
    max_len = max(len(matched_skills), len(missing_skills), 1)
    matched_pad = matched_skills + [""] * (max_len - len(matched_skills))
    missing_pad = missing_skills + [""] * (max_len - len(missing_skills))
    for m, g in zip(matched_pad, missing_pad):
        skill_rows.append([m, g])

    skill_table = Table(skill_rows, colWidths=[8 * cm, 8 * cm])
    skill_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1EFE8")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 1), (0, -1), SUCCESS),
        ("TEXTCOLOR", (1, 1), (1, -1), DANGER),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(skill_table)

    # ── Salary prediction ────────────────────────────────────────────────────
    story.append(Paragraph("AI salary prediction", styles["CPHeading"]))
    sal_text = (
        f"Based on your experience, location, and skill set, CareerPulse AI predicts an expected "
        f"salary of <b>₹{predicted_salary['predicted_salary_lpa']} LPA</b>, with a typical market range of "
        f"₹{predicted_salary['range_low']} – ₹{predicted_salary['range_high']} LPA."
    )
    story.append(Paragraph(sal_text, styles["CPBody"]))

    # ── Trending market skills ───────────────────────────────────────────────
    story.append(Paragraph("Trending skills in the market", styles["CPHeading"]))
    trend_rows = [["Skill", "Market demand"]] + [[s, f"{p}%"] for s, p in trending_skills]
    trend_table = Table(trend_rows, colWidths=[8 * cm, 8 * cm])
    trend_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1EFE8")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(trend_table)

    # ── Page break before recommendations ───────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Your personalized learning roadmap", styles["CPHeading"]))
    rec_rows = [["Skill to learn", "Recommended course", "Platform", "Cost", "Duration", "Priority"]]
    for r in recommendations:
        rec_rows.append([
            r["skill"], r["name"], r["platform"],
            "Free" if r["is_free"] else "Paid", f"{r['weeks']} wks", r["priority"],
        ])
    rec_table = Table(rec_rows, colWidths=[2.8 * cm, 5.5 * cm, 3.2 * cm, 1.6 * cm, 1.8 * cm, 2.1 * cm])
    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D3D1C7")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F8F5")]),
    ]))
    story.append(rec_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Generated by CareerPulse AI — Intelligent Job Market Analytics & Skill Gap Analyzer. "
        "This report is based on aggregated market data and should be used as directional guidance.",
        ParagraphStyle("footer", fontSize=8, textColor=MUTED_TEXT),
    ))

    doc.build(story)
    logger.info(f"Career report generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_career_report(
        output_path="sample_career_report.pdf",
        user_name="Aarav Sharma",
        target_role="Data Analyst",
        career_score=72.0,
        resume_match_pct=68.0,
        matched_skills=["Python", "SQL", "Power BI", "Pandas", "Excel", "Machine Learning", "Tableau"],
        missing_skills=["Spark", "Azure", "Airflow"],
        predicted_salary={"predicted_salary_lpa": 11.4, "range_low": 9.3, "range_high": 14.3},
        recommendations=[
            {"skill": "Spark", "name": "Big Data with Spark", "platform": "YouTube", "is_free": True, "weeks": 4, "priority": "High"},
            {"skill": "Azure", "name": "Azure Fundamentals (AZ-900)", "platform": "Microsoft Learn", "is_free": True, "weeks": 3, "priority": "High"},
            {"skill": "Airflow", "name": "Apache Airflow: The Hands-On Guide", "platform": "Udemy", "is_free": False, "weeks": 3, "priority": "Medium"},
        ],
        trending_skills=[("Python", 84), ("SQL", 76), ("Power BI", 62), ("Generative AI", 58)],
    )
