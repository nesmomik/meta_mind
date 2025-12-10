from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

def host_comment(
    mode: str = "",
    category_label: str = "",
    title_a: str = "",
    title_b: str = "",
    winner: str = "",
    was_correct: bool = True,
    score: int = 0,
    remaining_time: int = None,
):
    winner_title = winner or ""

    prompt = f"""
You are the energetic meta_mind game host.
One sentence only. Short, punchy, a bit cheeky, *British humour*,
playful, but clever.

Purpose: Say something fun about the round AND the titles AND the category.
Never mention you're AI.

Rules:
- ALWAYS mention at least one of the titles or a comparison between them.
- When correct: be curious or impressed.
- When wrong: humorous, gentle roast, but supportive.
- Add a tiny nerd fact or "insight" about the category or the topic when possible.
- Never ask questions back.
- No emojis.
- ONE sentence only.

Player data:
Mode: {mode}
Category: {category_label}
Title A: {title_a}
Title B: {title_b}
Winner title: {winner_title}
Correct: {was_correct}
Score: {score}
Time left: {remaining_time}
"""

    try:
        res = client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )
        text = res.output_text
        if text:
            return text.strip()
        return ""
    except Exception:
        return ""
