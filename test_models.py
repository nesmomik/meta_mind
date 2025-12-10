from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

test_models = [
    "gpt-4.1-mini",
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-5-nano",
]

for m in test_models:
    try:
        response = client.responses.create(
            model=m,
            input="Hello"
        )
        print(f"{m} - OK")
    except Exception as e:
        print(f"{m} - NO:", e)
