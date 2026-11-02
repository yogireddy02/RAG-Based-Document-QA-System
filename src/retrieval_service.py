from pinecone import DenseVectorQuery

from src.embedding_service import generate_embeddings
from src.pinecone_service import connect_to_index

NAMESPACE = "document-qa"


def retrieve_relevant_chunks(
        query: str,
        top_k: int = 3,
) -> list[dict]:
    """
    Retrieve the most relevant chunks from pinecone.
    """

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k <= 0:
        raise ValueError("Top k cannot be greater than zero.")

    # Step 1: Convert the user's question into an embedding.
    query_embedding = generate_embeddings([query])[0]

    # Step 2: Connect to Pinecone.
    index = connect_to_index()

    # Step 3: Search for similar document chunks.
    response = index.documents.search(
        namespace=NAMESPACE,
        top_k=top_k,
        score_by=[
            DenseVectorQuery(
                field="embedding",
                values=query_embedding,
            )
        ],
        include_fields=[
            "text",
            "source",
            "chunk_index",
        ],
    )

    # Step 4: Format the search results.
    results = []

    for match in response.matches:
        results.append(
            {
                "id": match.id,
                "score": match.score,
                "text": match.text,
                "source": match.source,
                "chunk_index": match.chunk_index,
            }
        )
    return results