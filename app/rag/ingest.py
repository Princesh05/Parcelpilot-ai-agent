from pathlib import Path

import chromadb

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.metadata import get_document_metadata


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

CHROMA_DIR = PROJECT_ROOT / "chroma_db"


def extract_text(pdf_path):
    """
    Extract text from a PDF.
    """

    reader = PdfReader(str(pdf_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def ingest_documents():

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name="parcelpilot_documents"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    documents = []
    metadatas = []
    ids = []

    chunk_id = 0

    for pdf_path in DOCUMENTS_DIR.glob("*.pdf"):

        print(f"Processing: {pdf_path.name}")

        text = extract_text(pdf_path)

        chunks = splitter.split_text(text)

        metadata = get_document_metadata(
            pdf_path.name
        )

        for chunk in chunks:

            documents.append(chunk)

            metadatas.append({
                **metadata,
                "source": pdf_path.name
            })

            ids.append(
                f"chunk_{chunk_id}"
            )

            chunk_id += 1

    if documents:

        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    print()
    print("================================")
    print("Document ingestion completed")
    print("Total chunks:", len(documents))
    print("================================")


if __name__ == "__main__":
    ingest_documents()