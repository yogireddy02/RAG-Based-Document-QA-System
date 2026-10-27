from src.document_loader import extract_text_from_document

def main():
    pdf_path = "data/sample_policy.pdf"
    documents  = extract_text_from_document(pdf_path)

    if not documents:
        print("No extractable text found in the document.")
        return

    for document in documents:
        print(f"\n--- Source: {document['source']} ---")
        print(document["text"])

    print(f"\nSuccessfully processed {len(documents)} document(s).")

if __name__ == "__main__":
    main()