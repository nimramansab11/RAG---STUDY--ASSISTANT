import os
import shutil

import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.embeddings import EmbeddingService


DOCUMENTS_DIR = "documents"
CHROMA_DIR = "chroma_db"

COLLECTION_NAME = "study_chapters"


class DocumentIngestion:
    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.client = chromadb.PersistentClient(
            path=CHROMA_DIR
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def extract_pdf_text(self, pdf_path):
        reader = PdfReader(pdf_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text
                })

        return pages

    def ingest_documents(self):
        pdf_files = [
            file
            for file in os.listdir(DOCUMENTS_DIR)
            if file.lower().endswith(".pdf")
        ]

        if not pdf_files:
            print("No PDF files found in documents folder.")
            return 0

        total_chunks = 0

        for pdf_file in sorted(pdf_files):

            pdf_path = os.path.join(
                DOCUMENTS_DIR,
                pdf_file
            )

            print(f"\nProcessing: {pdf_file}")

            pages = self.extract_pdf_text(pdf_path)

            for page_data in pages:

                chunks = self.text_splitter.split_text(
                    page_data["text"]
                )

                if not chunks:
                    continue

                embeddings = self.embedding_service.embed_documents(
                    chunks
                )

                ids = [
                    f"{pdf_file}_page_{page_data['page']}_chunk_{i}"
                    for i in range(len(chunks))
                ]

                metadatas = [
                    {
                        "source": pdf_file,
                        "page": page_data["page"]
                    }
                    for _ in chunks
                ]

                self.collection.add(
                    ids=ids,
                    documents=chunks,
                    embeddings=embeddings,
                    metadatas=metadatas
                )

                total_chunks += len(chunks)

                print(
                    f"  Page {page_data['page']}: "
                    f"{len(chunks)} chunks added"
                )

        print(
            f"\nIngestion completed. "
            f"Total chunks: {total_chunks}"
        )

        return total_chunks


if __name__ == "__main__":
    ingestion = DocumentIngestion()
    ingestion.ingest_documents()