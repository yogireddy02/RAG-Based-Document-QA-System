from src.document_loader import extract_text_from_document
from src.text_chunker import split_documents
from src.embedding_service import generate_embeddings
from src.vector_store import store_embeddings

def main():
    file_path = "data/sample_policy.pdf"

    documents = extract_text_from_document(file_path)
    chunks = split_documents(documents)

    if not chunks:
        print("No chunks available to store.")
        return

    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    stored_count = store_embeddings(chunks, embeddings)

    print(f"Chunks prepared: {len(chunks)}")
    print(f"Vectors stored: {stored_count}")
    print(f"Vector storage test passed!")

if __name__ == "__main__":
    main()