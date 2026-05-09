from dotenv import load_dotenv
from openai import OpenAI
import os, json
from typing import List

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

def synthesize_multi_document_answer(
    question: str,
    document_answers: List[str],
    ) -> str:
    
    document_summaries = []
    
    for document_answer in document_answers:
        sources = document_answer.get("sources", [])
        
        source_pages = [
            {
                "document_id": source.get("document_id"),
                "document_name": source.get("document_name"),
                "company": source.get("company"),
                "year": source.get("year"),
                "page_number": source.get("page_number")
            } 
            for source in sources
        ]
        
        document_summaries.append({
            "document_id": document_answer.get("document_id"),
            "answer": document_answer.get("answer"), 
            "source_pages": source_pages, 

        })
        
    prompt = f"""
        You are an AI assistant performing comparative analysis across multiple financial documents.

        The user asked:
        {question}

        Below are answers generated separately from each selected document.
        Each answer was generated using only that specific document.

        Document answers:
        {json.dumps(document_summaries, indent=2, ensure_ascii=False)}

        Your task:
        Write the comparative analysis result only.

        Rules:
        1. Compare the document answers clearly.
        2. If the question is numeric and the needed numbers are available, calculate the difference and percentage change when possible.
        3. If the question is text-based, compare the relevant statements, strategies, policies, or facts.
        4. Mention the document year/company when available.
        5. Use only the provided document answers and source pages.
        6. If one document is missing evidence, say that clearly.
        7. Do not invent facts.
        8. Do not include the separate document answers again. Those are returned separately by the API.

        Comparative analysis result:
        """

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You compare document-specific answers using only the provided evidence."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content
    