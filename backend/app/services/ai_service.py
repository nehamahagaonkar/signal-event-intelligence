import os

from google import genai


MODEL_NAME = "gemini-2.5-flash"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=api_key)


def generate_with_gemini(prompt: str) -> str:
    try:
        client = get_client()

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    except RuntimeError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"Gemini API request failed: {error}"
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

    return generate_with_gemini(prompt)


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

    return generate_with_gemini(prompt)
