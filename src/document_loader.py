import html
from pathlib import Path

from docling.document_converter import DocumentConverter

def extract_text_from_document(filepath: str) -> list[dict]:
    """
    Extract structured text from a document using Docling.
    Returns the extracted text with page metadata where available.
    """

    document_path = Path(filepath)

    if not document_path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    converter = DocumentConverter()
    result = converter.convert(str(document_path))

    markdown_text = html.unescape(
        result.document.export_to_markdown()
    ).strip()

    if not markdown_text:
        return []

    return [
        {
            "text": markdown_text,
            "source": document_path.name
        }
    ]