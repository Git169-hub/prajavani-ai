import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

st.set_page_config(
    page_title="Prajavani AI - Government Schemes Assistant",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ Prajavani AI")
st.subheader("Indian Government Schemes Assistant")
st.caption("PM Kisan • Ayushman Bharat • MGNREGA • PM Awas Yojana • Atal Pension")
st.divider()

@st.cache_resource
def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    return retriever, client

retriever, client = load_rag()

def detect_language(text: str) -> str:
    telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
    return "telugu" if telugu_chars > 2 else "english"

def answer_query(query):
    docs = retriever.invoke(query)
    lang = detect_language(query)

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

    return response.choices[0].message.content, sources

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.caption(f"📚 Sources: {', '.join(msg['sources'])}")

if query := st.chat_input("Ask about any government scheme (Telugu or English)..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)
    with st.chat_message("assistant"):
        with st.spinner("వెతుకుతున్నాను..."):
            answer, sources = answer_query(query)
        st.write(answer)
        st.caption(f"📚 Sources: {', '.join(sources)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })