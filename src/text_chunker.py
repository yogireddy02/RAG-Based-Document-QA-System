from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
        documents: list[dict],
        chunk_size: int = 500,
        chunk_overlap: int = 100,
) -> list[dict]:
    """
    Split extracted documents text into chunks while preserving metadata.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be in range [0, chunk_size]."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = []

    for document in documents:
        text = document["text"].strip()

        if not text:
            continue

        text_chunks = splitter.split_text(text)

        for index, chunk in enumerate(text_chunks):
            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "chunk_index": index,
                }
            )
    return chunks