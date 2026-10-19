# ✦ StudySpace AI — AI Study Assistant

> An intelligent RAG-powered study assistant that answers questions directly from your study chapters using local embeddings, ChromaDB, and Groq LLM.

---

## 📚 Overview

**StudySpace AI** is an AI-powered study assistant designed to help students understand their study material through natural-language questions.

Instead of searching manually through multiple PDF chapters, students can simply ask a question and the system retrieves the most relevant information from the uploaded study material.

The retrieved content is then provided to an AI model, which generates a clear and context-based answer.

The project uses a **Retrieval-Augmented Generation (RAG)** architecture.

---

## ✦ How It Works

```text
                  STUDENT QUESTION
                         │
                         ▼
                ┌─────────────────┐
                │   Query         │
                │   Embedding     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    ChromaDB     │
                │ Vector Search   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Relevant Study  │
                │     Chunks      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Groq LLM      │
                │   Generation    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ AI Answer +     │
                │ Sources         │
                └─────────────────┘