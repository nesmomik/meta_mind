from openai import OpenAI
from dotenv import load_dotenv

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
    """
    Very short, fast AI host line.
    One short sentence, max ~15 words.
    """

    winner_title = winner or ""

    prompt = f"""
You are a fast, witty game show host in a Wikipedia metadata quiz called meta_mind.

TASK:
- Reply with EXACTLY ONE very short sentence (max 15 words).
- No emojis, no questions, no mention of AI.
- Tone: clever, playful, a bit British, but concise.
- If player was correct: praise them briskly.
- If player was wrong: light, friendly tease.
- Prefer to mention one of the article titles or the category briefly.

DATA:
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
            input=prompt,
            max_output_tokens=40,  # keep it tiny = faster
        )
        text = res.output_text
        if text:
            return text.strip()
        return ""
    except Exception as e:
        print("[AI HOST ERROR]", e)
        return ""
