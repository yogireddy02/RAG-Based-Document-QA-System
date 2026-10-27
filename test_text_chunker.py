from src.document_loader import extract_text_from_document
from src.text_chunker import split_documents

def main():
    file_path = "data/sample_policy.pdf"

    documents = extract_text_from_document(file_path)
    chunks = split_documents(
        documents,
        chunk_size=500,
        chunk_overlap=100,
    )

    if not chunks:
        print("No text chunks were created.")
        return

    for chunk in chunks:
        print(
            f"\n--- Chunk {chunk['chunk_index']} "
            f"| Source: {chunk['source']} ---"
        )
        print(chunk["text"])

    print(f"\nDocuments processed: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")


if __name__ == "__main__":
    main()
