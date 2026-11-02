import os

from dotenv import load_dotenv
from openai import OpenAI

from src.retrieval_service import retrieve_relevant_chunks

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"))

CHAT_MODEL = os.getenv("OPEN_AI_CHAT_MODEL","gpt-4o-mini")


def generate_answer(
        question: str,
        top_k: int= 3,
) -> dict:
    """
    Generate an answer using retrieved document context.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Retrieve relevant document chunks.
    retrieved_chunks = retrieve_relevant_chunks(
        query=question,
        top_k=top_k,
    )

    if not retrieved_chunks:
        return {
            "answer": "I couldn't find relevant information in the uploaded documents.",
            "sources": [],
        }

    # Step 2: Build context from retieved chunks.
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    # Step 3: Prepare the prompt.
    system_prompt = """
    You are a document question-answering assistant.
    
    Answer the user's question using ONLY the provided document context.
    
    Rules:
    1. Do not use outside knowledge.
    2. Do not invent facts or information.
    3. If the context does not contain the answer, clearly say:
        "The provided documents do not contain enough information to answer this question.
    4. Give clear and concise answers.
    """

    user_prompt = f"""
    Document Context:
    {context}
    
    User Question:
    {question}
    
    Answer based only on the document context.
    """

    # Step 4: Genearte the answer using OpenAI.
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    answer = response.choices[0].message.content

    # Step 5: Return answer and source information.
    sources = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "score": chunk["score"],
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }