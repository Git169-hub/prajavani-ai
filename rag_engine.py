from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq
import os

# Load vectorstore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Groq client
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")

def answer_query(query: str) -> dict:
    # Retrieve relevant chunks
    docs = retriever.invoke(query)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = list(set([doc.metadata.get("scheme", "unknown") for doc in docs]))
    
    # Build prompt
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

# Test it
if __name__ == "__main__":
    test_queries = [
        "Ayushman Bharat scheme benefits enti?"
	"PMJAY lo free treatment entha vastundi?"
	"Ayushman Bharat ki ela apply cheyali?"    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = answer_query(query)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print("-" * 50)
