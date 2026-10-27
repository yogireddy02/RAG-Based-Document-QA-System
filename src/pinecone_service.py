import os

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-document-qa",)

EMBEDDING_DIMENSION = 1536

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing from your .env file.")

pc = Pinecone(api_key=PINECONE_API_KEY)

def connect_to_index():
    """
    Connect to the confiured Pinecone index.
    Create it if does not exist.
    """

    existing_indexes = [
        index.name for index in pc.indexes.list()
    ]

    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")

        pc.indexes.create(
            name=PINECONE_INDEX_NAME,
            schema={
                "fields": {
                    "embedding": {
                        "type": "dense_vector",
                        "dimension": EMBEDDING_DIMENSION,
                        "metric": "cosine",
                    }
                }
            },
            deployment={
                "deployment_type": "managed",
                "cloud": "aws",
                "region": "us-east-1",
            },
        )

        print("Pinecone index created successfully.")

    index = pc.index(name=PINECONE_INDEX_NAME)

    print(f"Connected to Pinecone index: {PINECONE_INDEX_NAME}")

    return index