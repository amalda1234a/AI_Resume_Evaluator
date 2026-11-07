

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from src.openrouter_client import generate_response


WEIGHTS = {
    "core_skills": 30,
    "projects_and_assignments": 25,
    "experience_internships": 15,
    "academic_qualification": 15,
    "resume_quality": 15,
}


class CategoryScore(BaseModel):
    """Score and justification for one evaluation category."""

    score: int = Field(ge=0, le=100)
    justification: str


class EvaluationReport(BaseModel):
    """Validated resume evaluation report."""

    candidate_name: str
    category_scores: dict[str, CategoryScore]
    key_strengths: list[str]
    skill_gaps: list[str]
    hiring_manager_recommendation: str


def build_prompt(jd_text: str, resume_text: str) -> str:
    """Create the prompt for AI-based resume evaluation."""

    schema = {
        "candidate_name": "Candidate name",
        "category_scores": {
            "core_skills": {
                "score": 80,
                "justification": "Explanation"
            },
            "projects_and_assignments": {
                "score": 80,
                "justification": "Explanation"
            },
            "experience_internships": {
                "score": 80,
                "justification": "Explanation"
            },
            "academic_qualification": {
                "score": 80,
                "justification": "Explanation"
            },
            "resume_quality": {
                "score": 80,
                "justification": "Explanation"
            }
        },
        "key_strengths": [
            "Strength 1",
            "Strength 2"
        ],
        "skill_gaps": [
            "Gap 1",
            "Gap 2"
        ],
        "hiring_manager_recommendation": "Recommendation"
    }

    return (
        "You are an experienced technical recruiter.\n"
        "Evaluate the candidate's resume against the job description.\n\n"
        f"JOB DESCRIPTION:\n{jd_text}\n\n"
        f"CANDIDATE RESUME:\n{resume_text}\n\n"
        "Evaluate these five categories using the specified weights:\n"
        "- Core skills: 30%\n"
        "- Projects and assignments: 25%\n"
        "- Experience and internships: 15%\n"
        "- Academic qualification: 15%\n"
        "- Resume quality: 15%\n\n"
        "Give each category a score between 0 and 100.\n"
        "Base scores only on evidence in the resume.\n"
        "Do not invent experience, qualifications or skills.\n"
        "Explain every category score clearly.\n"
        "Identify strengths and skill gaps.\n"
        "Provide a hiring manager recommendation.\n"
        "Return ONLY valid JSON without Markdown code fences.\n"
        "Follow this JSON structure:\n"
        + json.dumps(schema, indent=2)
    )


def parse_ai_response(response: str) -> dict[str, Any]:
    """Convert AI response into a Python dictionary."""

    cleaned = response.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as error:
        raise ValueError(
            "AI returned invalid JSON. Please try again."
        ) from error


def calculate_overall_score(
    category_scores: dict[str, CategoryScore]
) -> int:
    """Calculate the weighted overall matching score."""

    total = sum(
        category_scores[name].score * weight / 100
        for name, weight in WEIGHTS.items()
    )

    return round(total)


def determine_fit_status(score: int) -> str:
    """Determine the candidate's overall fit status."""

    if score >= 75:
        return "Strong Match"

    if score >= 50:
        return "Moderate Match"

    return "Weak Match"


def evaluate_resume(
    jd_text: str,
    resume_text: str
) -> dict[str, Any]:
    """Evaluate a resume using OpenRouter AI."""

    prompt = build_prompt(jd_text, resume_text)

    ai_response = generate_response(prompt)

    response_data = parse_ai_response(ai_response)

    report = EvaluationReport.model_validate(response_data)

    expected_categories = set(WEIGHTS.keys())

    if set(report.category_scores.keys()) != expected_categories:
        raise ValueError(
            "AI response does not contain all five evaluation categories."
        )

    overall_score = calculate_overall_score(
        report.category_scores
    )

    result = report.model_dump()

    result["overall_match_score"] = overall_score

    result["fit_status"] = determine_fit_status(
        overall_score
    )

    for category, weight in WEIGHTS.items():
        result["category_scores"][category]["weight"] = (
            f"{weight}%"
        )

    return result


def save_report(
    evaluation: dict[str, Any],
    output_path: Path
) -> None:
    """Save the evaluation report as a JSON file."""

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            evaluation,
            file,
            indent=4,
            ensure_ascii=False
        )
