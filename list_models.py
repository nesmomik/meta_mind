from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

models = client.models.list()

print("Available models for this project:\n")
for m in models.data:
    print("-", m.id)
