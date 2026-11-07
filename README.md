
# AI Resume Evaluator

## Project Overview
AI Resume Evaluator is a Python-based application that evaluates candidate resumes against a job description using an AI model through OpenRouter.

It extracts text from PDF and DOCX resumes, preprocesses the content, evaluates candidates across five categories, calculates a weighted score, and generates a JSON report.

## Technologies Used
- Python 3
- OpenRouter API
- Pydantic
- Requests
- PyPDF
- Python-docx
- Python-dotenv

## Evaluation Categories

| Category | Weight |
|---|---:|
| Core Skills | 30% |
| Projects and Assignments | 25% |
| Experience and Internships | 15% |
| Academic Qualification | 15% |
| Resume Quality | 15% |

## Project Structure

```text
AI_Resume_Evaluator/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── parsers.py
│   ├── preprocessor.py
│   ├── openrouter_client.py
│   └── evaluator.py
├── sample_resumes/
│   ├── strong_candidate.docx
│   └── weak_candidate.docx
├── .env.example
├── .gitignore
├── requirements.txt
├── jd.txt
└── main.py
```

## Installation

1. Clone the repository.
2. Create a virtual environment:

   python -m venv .venv

3. Activate it:

   .venv\Scripts\activate

4. Install dependencies:

   pip install -r requirements.txt

5. Create a `.env` file using `.env.example` and add your OpenRouter API key.

## Usage

Run the application:

python main.py sample_resumes/strong_candidate.docx

For another resume:

python main.py sample_resumes/weak_candidate.docx

## Output

The application generates `evaluation_report.json` containing:
- Candidate name
- Overall matching score
- Fit status
- Category scores and justifications
- Key strengths
- Skill gaps
- Hiring manager recommendation

## Sample Testing

Two fictional resumes are included for testing:
- Strong candidate
- Weak candidate

## Security

API keys are stored in environment variables and excluded from Git using `.gitignore`.
