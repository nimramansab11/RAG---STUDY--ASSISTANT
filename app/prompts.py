SYSTEM_PROMPT = """
You are an AI Study Assistant.

Your job is to answer questions using ONLY the study material
provided in the context.

Rules:
1. Use the provided context as the main source of truth.
2. Do not invent information that is not supported by the context.
3. Explain answers clearly and simply.
4. If the answer is not available in the context, say:
   "I could not find the answer in the provided study chapters."
5. When possible, mention the chapter that supports the answer.
"""


def build_prompt(question, retrieved_chunks):

    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):

        context_parts.append(
            f"""
Source {i}:
Chapter: {chunk['source']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
Study Context:
{context}

Student Question:
{question}

Answer the student's question using the study context above.
"""

    return prompt