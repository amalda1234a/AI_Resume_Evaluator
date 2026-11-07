

import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def clean_extracted_text(text: str) -> str:
    """Remove unnecessary spaces and empty lines from extracted text."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_pdf_text(file_path: Path) -> str:
    """Extract text from a PDF resume."""
    reader = PdfReader(str(file_path))
    pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append(page_text)

    return clean_extracted_text("\n".join(pages))


def extract_docx_text(file_path: Path) -> str:
    """Extract text from a DOCX resume, including tables."""
    document = Document(str(file_path))
    content = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            content.append(paragraph.text)

    for table in document.tables:
        for row in table.rows:
            row_text = [
                cell.text.strip() for cell in row.cells
            ]
            content.append(" | ".join(row_text))

    return clean_extracted_text("\n".join(content))


def extract_resume_text(file_path: str) -> str:
    """Extract text based on the resume file extension."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        text = extract_pdf_text(path)
    elif extension == ".docx":
        text = extract_docx_text(path)
    else:
        raise ValueError(
            "Unsupported file format. Please use PDF or DOCX."
        )

    if not text:
        raise ValueError(
            "No readable text found in the resume."
        )

    return text
