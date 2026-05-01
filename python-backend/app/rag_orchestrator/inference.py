from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv('app/.env')

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def generate_response(question: str, context: str) -> str:
    prompt = f"""
You are an AI assistant for financial document analysis.

Answer the user's question using ONLY the provided context.

If the answer is not available in the context, say:
"I could not find the answer in the provided document context."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "You answer questions using only the provided document context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content