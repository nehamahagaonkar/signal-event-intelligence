import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_with_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    request = Request(
        OLLAMA_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        return result.get("response", "").strip()

    except HTTPError as error:
        raise RuntimeError(
            f"Ollama returned HTTP {error.code}"
        )

    except URLError:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        )


def summarize_notes(notes: str) -> str:
    prompt = f"""
You are an assistant for an event lead management system.

Summarize the following interaction notes in 2-3 concise sentences.

Focus on:
- what was discussed
- the lead's interest
- any important next step

Do not invent information.

Interaction notes:
{notes}

Return only the summary.
"""

    return generate_with_ollama(prompt)


def draft_follow_up(
    name: str,
    notes: str,
) -> str:
    prompt = f"""
You are a professional business development assistant.

Write a concise, personalized follow-up email for a lead
after an event.

Lead name:
{name}

Interaction notes:
{notes}

Requirements:
- Professional but natural tone
- Mention the relevant discussion
- Include a clear next step
- Do not invent facts
- Keep it under 150 words
- Do not include a subject line

Return only the email body.
"""

    return generate_with_ollama(prompt)