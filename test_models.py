from dotenv import load_dotenv
import os
load_dotenv()

from openai import OpenAI

client = OpenAI()

models = ["gpt-5-nano"]

for m in models:
    try:
        client.responses.create(model=m, input="hi")
        print(m, "- OK")
    except Exception as e:
        print(m, "- NO:", e)
