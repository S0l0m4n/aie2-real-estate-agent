"""
Thin Groq client.
"""

from functools import lru_cache

from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL

# Model temperature (default = 1)
TEMPERATURE = 1


# NOTE: Use the cache to only create the client once
@lru_cache(maxsize=1)
def _get_groq_client():
    return Groq(api_key=GROQ_API_KEY)


def call_llm(user_prompt: str, system_prompt: str) -> str:
    """Call LLM with user prompt and system prompt."""
    client = _get_groq_client()

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        model=GROQ_MODEL,
        temperature=TEMPERATURE,
    )

    return response.choices[0].message.content
