from dotenv import load_dotenv
from openai import OpenAI
import os

from app.config import OPENAI_API_KEY, OPENAI_URL, OPENAI_MODEL_NAME


api_key = OPENAI_API_KEY
base_url = OPENAI_URL
model_name = OPENAI_MODEL_NAME

client = OpenAI(api_key=api_key, base_url=base_url)


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
        model=model_name,
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