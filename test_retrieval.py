from src.retrieval_service import retrieve_relevant_chunks


def main():
    query = "What is Retrieval Augmented Generation and how does it work?"

    results = retrieve_relevant_chunks(
        query=query,
        top_k=3,
    )

    print(f"\nUser Question: {query}")
    print(f"\nRelevant chunks found: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Score: {result['score']}")
        print(f"Chunk: {result['chunk_index']}")
        print(f"Content:\n{result['text']}")


if __name__ == "__main__":
    main()