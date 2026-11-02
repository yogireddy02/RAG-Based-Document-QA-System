from src.answer_generator import generate_answer

def main():

    questions = [
        "What is Retrieval Augmented Generation and how does it work?",
        "What is the company's annual leave policy?"
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print(f"QUESTION: {question}")

        result = generate_answer(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"File: {source['source']} | "
                f"Chunk: {source['chunk_index']} | "
                f"Score: {source['score']:.4f}"
            )

        print("=" * 70)

if __name__ == "__main__":
    main()