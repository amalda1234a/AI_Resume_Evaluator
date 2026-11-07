

import argparse
import sys
from pathlib import Path

from src.config import JD_PATH, REPORT_PATH, validate_config
from src.evaluator import evaluate_resume, save_report
from src.parsers import extract_resume_text
from src.preprocessor import preprocess_jd, preprocess_resume


def main() -> None:
    """Run the resume evaluation application."""

    parser = argparse.ArgumentParser(
        description="AI-powered resume evaluation system"
    )

    parser.add_argument(
        "resume",
        help="Path to a candidate resume (PDF or DOCX)"
    )

    args = parser.parse_args()

    resume_path = Path(args.resume)

    try:
        validate_config()

        if not resume_path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {resume_path}"
            )

        print("\nAI Resume Evaluator")
        print("-------------------")
        print("Reading job description...")

        jd_text = JD_PATH.read_text(encoding="utf-8")
        jd_text = preprocess_jd(jd_text)

        print("Extracting resume text...")

        resume_text = extract_resume_text(str(resume_path))
        resume_text = preprocess_resume(resume_text)

        print("Evaluating resume using AI...")
        print("Please wait...\n")

        evaluation = evaluate_resume(jd_text, resume_text)

        save_report(evaluation, REPORT_PATH)

        print("Evaluation completed successfully!")
        print(f"Candidate: {evaluation['candidate_name']}")
        print(
            f"Overall Score: "
            f"{evaluation['overall_match_score']}/100"
        )
        print(f"Fit Status: {evaluation['fit_status']}")
        print(f"\nReport saved to: {REPORT_PATH}")

    except (ValueError, FileNotFoundError, RuntimeError) as error:
        print(f"\nError: {error}")
        sys.exit(1)

    except OSError as error:
        print(f"\nFile error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
