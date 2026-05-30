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

# Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

# Scheme keyword detection
SCHEME_KEYWORDS = {
    "pm_kisan": ["kisan", "pm-kisan", "pmkisan", "కిసాన్", "కిసాన"],
    "ayushman_bharat": ["ayushman", "ayushman bharat", "ఆయుష్మాన్", "ఆయుష్మాన"],
    "mgnrega": ["mgnrega", "nrega", "manrega"],
    "pm_awas_yojana": ["awas", "pmay", "awas yojana", "ఆవాస్"],
    "atal_pension": ["atal", "pension", "అటల్"],
}

def detect_language(text: str) -> str:
    telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
    return "telugu" if telugu_chars > 2 else "english"

def detect_scheme(query: str) -> str:
    query_lower = query.lower()
    print(f"DEBUG detecting scheme for: {repr(query_lower)}")
    for scheme, keywords in SCHEME_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in query_lower:
                print(f"DEBUG matched: {scheme} via keyword: {kw}")
                return scheme
    print("DEBUG no scheme matched")
    return None

def answer_query(query: str) -> dict:
    lang = detect_language(query)
    scheme = detect_scheme(query)

    # Build targeted search
    if scheme and lang == "telugu":
        target = f"{scheme}_telugu"
        docs = vectorstore.similarity_search(query, k=6, filter={"scheme": target})
        if not docs:
            docs = vectorstore.similarity_search(query, k=6, filter={"scheme": {"$contains": "_telugu"}})
    elif scheme and lang == "english":
        docs = vectorstore.similarity_search(query, k=6, filter={"scheme": scheme})
        if not docs:
            docs = vectorstore.similarity_search(query, k=6)
    elif lang == "telugu":
        docs = vectorstore.similarity_search(query, k=6, filter={"scheme": {"$contains": "_telugu"}})
    else:
        docs = vectorstore.similarity_search(query, k=6)

    if not docs:
        docs = vectorstore.similarity_search(query, k=6)

    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([doc.metadata.get("scheme", "unknown") for doc in docs]))

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
        "chunks_used": len(docs)
    }

# Test block
if __name__ == "__main__":
    test_queries = [
        "పీఎం కిసాన్ పథకం అంటే ఏమిటి?",
        "What is PM Kisan scheme and who is eligible?",
        "ఆయుష్మాన్ భారత్ అర్హత ఏమిటి?",
        "How much money does PM Kisan give per year?",
        "అటల్ పెన్షన్ యోజన వయసులో చేరవచ్చు?"
    ]
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = answer_query(query)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print(f"Chunks used: {result['chunks_used']}")
        print("-" * 50)