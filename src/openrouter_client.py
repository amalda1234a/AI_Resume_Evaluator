


import time
import requests

from src.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_URL,
)


def generate_response(prompt: str) -> str:
    """Send a prompt to OpenRouter and return the AI response."""

    if not OPENROUTER_API_KEY:
        raise ValueError(
            "Missing API key. Configure OPENROUTER_API_KEY in .env."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Resume Evaluator",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
    }

    for attempt in range(3):
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=90,
            )

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except (requests.RequestException, KeyError, IndexError) as error:
            if attempt == 2:
                raise RuntimeError(
                    f"OpenRouter request failed: {error}"
                ) from error

            time.sleep(2 ** attempt)

    raise RuntimeError("Unable to get a response from OpenRouter.")
