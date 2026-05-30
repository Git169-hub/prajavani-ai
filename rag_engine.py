import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

# Load vectorstore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Increased k to 6 for better candidate pool
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# Groq client — replace with your actual key
client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

def detect_language(text: str) -> str:
    telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
    return "telugu" if telugu_chars > 2 else "english"

def answer_query(query: str) -> dict:
    docs = retriever.invoke(query)
    lang = detect_language(query)

    # Filter using 'scheme' metadata key which has clean names
    if lang == "telugu":
        filtered = [d for d in docs if d.metadata.get("scheme", "").endswith("_telugu")]
        if not filtered:
            filtered = docs
    else:
        filtered = [d for d in docs if not d.metadata.get("scheme", "").endswith("_telugu")]
        if not filtered:
            filtered = docs

    context = "\n\n".join([doc.page_content for doc in filtered])
    sources = list(set([doc.metadata.get("scheme", "unknown") for doc in filtered]))

    prompt = f"""You are a helpful assistant explaining Indian government schemes to rural citizens.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have that information."
Reply in the same language as the question (Telugu or English).

Context:
{context}

Question: {query}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources,
        "chunks_used": len(filtered)
    }

# Test block
if __name__ == "__main__":
    test_queries = [
        "పీఎం కిసాన్ పథకం అర్హత ఏమిటి?",
        "What is PM Kisan scheme and who is eligible?",
        "ఆయుష్మాన్ భారత్ అర్హత ఏమిటి?",
        "How much money does PM Kisan give per year?",
        "అటల్ పెన్షన్ యోజన ఏ వయసులో చేరవచ్చు?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = answer_query(query)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 50)