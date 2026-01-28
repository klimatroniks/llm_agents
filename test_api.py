from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

print("API KEY FOUND:", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI()

resp = client.responses.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    input="Ответь одним словом: работает?"
)

print(resp.output_text)
