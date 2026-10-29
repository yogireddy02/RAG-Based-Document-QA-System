import inspect
import os

import pinecone
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

print("Pinecone SDK version:", pinecone.__version__)

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY is missing from .env")

pc = Pinecone(api_key=api_key)
index = pc.Index(name="rag-document-qa")


def inspect_methods(label, obj):
    print(f"\n--- {label} ---")
    print("Object type:", type(obj))

    for name in dir(obj):
        if name.startswith("_"):
            continue

        method = getattr(obj, name, None)

        if callable(method):
            try:
                signature = inspect.signature(method)
            except (TypeError, ValueError):
                signature = "(signature unavailable)"

            print(f"{name}{signature}")


inspect_methods("Index methods", index)

if hasattr(index, "documents"):
    documents_api = index.documents
    inspect_methods("Documents API methods", documents_api)
else:
    print("\nNo index.documents attribute found.")

if hasattr(index, "upsert_records"):
    print("\n--- upsert_records signature ---")
    try:
        print(inspect.signature(index.upsert_records))
    except (TypeError, ValueError) as error:
        print(error)