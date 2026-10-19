import os

import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.embeddings import EmbeddingService
from app.prompts import SYSTEM_PROMPT, build_prompt


load_dotenv()

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "study_chapters"


class RAGService:

    def __init__(self):

        print("Initializing RAG service...")

        # Load embedding model
        self.embedding_service = EmbeddingService()

        # Connect to ChromaDB
        self.client = chromadb.PersistentClient(
            path=CHROMA_DIR
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

        # Load Groq API key
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        # Initialize Groq model
        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
            groq_api_key=api_key
        )

        print(
            f"RAG service ready. "
            f"Documents in database: {self.collection.count()}"
        )

    def retrieve(self, question, top_k=3):

        question_embedding = (
            self.embedding_service.embed_query(question)
        )

        results = self.collection.query(
            query_embeddings=[question_embedding],
            n_results=top_k
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        retrieved_chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append({
                "text": document,
                "source": metadata.get("source"),
                "page": metadata.get("page"),
                "distance": distance
            })

        return retrieved_chunks

    def ask(self, question):

        # Retrieve relevant information
        retrieved_chunks = self.retrieve(
            question,
            top_k=3
        )

        if not retrieved_chunks:

            return {
                "answer": (
                    "I could not find the answer in "
                    "the provided study chapters."
                ),
                "sources": []
            }

        # Build RAG prompt
        prompt = build_prompt(
            question,
            retrieved_chunks
        )

        messages = [
            (
                "system",
                SYSTEM_PROMPT
            ),
            (
                "human",
                prompt
            )
        ]

        # Generate answer with Groq
        response = self.llm.invoke(messages)

        sources = [
            {
                "source": chunk["source"],
                "page": chunk["page"],
                "distance": chunk["distance"]
            }
            for chunk in retrieved_chunks
        ]

        return {
            "answer": response.content,
            "sources": sources
        }


if __name__ == "__main__":

    rag = RAGService()

    question = input(
        "\nAsk a question about your study chapters: "
    )

    result = rag.ask(question)

    print(
        "\n================ ANSWER ================\n"
    )

    print(result["answer"])

    print(
        "\n================ SOURCES ================\n"
    )

    for source in result["sources"]:

        print(
            f"{source['source']} | "
            f"Page {source['page']} | "
            f"Distance: {source['distance']}"
        )