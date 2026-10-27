from src.pinecone_service import connect_to_index

def main():
    index = connect_to_index()

    stats = index.describe_index_stats()

    print("\nPinecone connection successful")
    print(f"Vector count: {stats.total_vector_count}")

if __name__ == "__main__":
    main()