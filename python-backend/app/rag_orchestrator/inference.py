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
            "titl": document_answer.get("title"),
            "evidence_status": document_answer.get("evidence_status"), 
            "answer": document_answer.get("answer"), 
            "source_pages": source_pages, 

        })
        
        prompt = f"""
        You are an AI assistant answering a user's comparison question across multiple financial documents.

        User question:
        {question}

        Below are document-specific answers generated separately from each selected document.
        Each answer was generated using only that document.

        Document answers:
        {json.dumps(document_summaries, indent=2, ensure_ascii=False)}

        Write the final comparative answer for the user.

        Rules:
        1. Answer the user's question directly.
        2. Do not explain the internal retrieval process.
        3. Do not mention technical fields such as evidence_status, source_pages, chunks, retrieval, context, or document_summaries.
        4. If enough evidence is available, provide a clear comparison.
        5. If numeric values are available, calculate the absolute difference and percentage change when possible.
        6. If evidence is missing from one or more documents, say this briefly in user-friendly language.
        7. Do not invent missing numbers or facts.
        8. Do not repeat the full separate document answers.
        9. Keep the answer concise and business-readable.

        Final comparative answer:
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
    