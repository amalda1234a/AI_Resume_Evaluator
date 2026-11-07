

import re


def clean_text(text: str) -> str:
    """Clean unnecessary spaces, symbols and blank lines."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]

    return "\n".join(cleaned_lines)


def limit_text(text: str, max_chars: int = 15000) -> str:
    """Limit text length to reduce unnecessary API token usage."""
    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n[Text truncated due to length limit]"


def preprocess_resume(text: str) -> str:
    """Clean and prepare resume text."""
    cleaned = clean_text(text)
    return limit_text(cleaned)


def preprocess_jd(text: str) -> str:
    """Clean and prepare job description text."""
    cleaned = clean_text(text)
    return limit_text(cleaned, max_chars=10000)
