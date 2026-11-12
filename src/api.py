import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException

from src.document_loader import extract_text_from_document
from src.text_chunker import split_documents
from src.embedding_service import generate_embeddings
from src.vector_store import store_embeddings

# Initialize FasTAPI application
app = FastAPI(
    title="RAG Document Q&A API",
    description="Backend API for the RAG-Based Document Q&A System",
    version="1.0.0",
)

@app.get("/")
def home():
    return {
        "message": "Welcome to RAG Document Q&A API",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RAG Document Q&A API",
    }

@app.post("/upload")
def upload_document(file: UploadFile = File(...)):

    # Validate PDF extension
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    temp_path = None

    try:
        # Read uploaded file
        file_content = file.file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        # Save PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp_file:

            temp_file.write(file_content)
            temp_path = temp_file.name

        # Extract document text
        documents = extract_text_from_document(temp_path)

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No text could be extracted from the PDF.",
            )

        # Preserve original filename
        for document in documents:
            document['source'] = Path(file.filename).name

        # Split into chunks
        chunks = split_documents(documents)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No chunks were generated.",
            )

        # Generate embeddings
        texts = [chunk['text'] for chunk in chunks]

        embeddings = generate_embeddings(texts)

        # Store in Pinecone
        stored_count = store_embeddings(
            chunks,
            embeddings
        )

        return {
            "message": "Document processed successfully.",
            "filename": Path(file.filename).name,
            "chunks_created": len(chunks),
            "chunks_stored": stored_count,
            "status": "success",
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}",
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)