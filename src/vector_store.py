from src.pinecone_service import connect_to_index

def store_embeddings(
        chunks: list[dict],
        embeddings: list[list[float]],
) -> int:
    """
    Store document chunks and thier embeddings in Pinecone.

    Returns the number of documents submitted for storage.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "The number of chunks must match the number of embeddings."
        )

    if not chunks:
        return 0

    index = connect_to_index()

    documents = []

    for chunk, embedding in zip(chunks, embeddings):
        document_id = f"{chunk['source']}-{chunk['chunk_index']}"

        documents.append(
            {
                "id": document_id,
                "text": chunk["text"],
                "embedding": embedding,
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    response = index.documents.upsert(
        namespace="",
        documents=documents,
    )

    print(f"Pinecone upsert response: {response}")

    return len(documents)