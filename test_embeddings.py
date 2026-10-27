from neo4j._codec.hydration.bolt.v3 import vector

from src.document_loader import extract_text_from_document
from src.text_chunker import split_documents
from src.embedding_service import generate_embeddings

def main():
    documents = extract_text_from_document("data/sample_policy.pdf")
    chunks = split_documents(documents)

    if not chunks:
        print("No chunks available to embed.")
        return

    texts = [chunks['text'] for chunks in chunks]
    embeddings = generate_embeddings(texts)

    print(f"Chunks processed: {len(chunks)}")
    print(f"Embeddings generated: {len(embeddings)}")

    if embeddings:
        print(f"Dimensions per embeding: {len(embeddings[0])}")
        print(f"First 5 values: {embeddings[0][:5]}")

    assert len(embeddings) == len(chunks)
    assert all(len(vector) == 1536 for vector in embeddings)

    print("Embeding test passed!")

if __name__ == "__main__":
    main()