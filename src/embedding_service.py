import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing from your .env file.")

client = OpenAI(api_key=api_key)

EMBEDDING_MODEL = "text-embedding-3-small"

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text strings into embedding vectors.
    """

    if not texts:
        return []

    if any(not text.strip() for text in texts):
        raise ValueError("Input texts must not contain empty strings.")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    # Preserve the input order explicitly.
    sorted_data = sorted(response.data, key=lambda item: item.index)

    return [item.embedding for item in sorted_data]