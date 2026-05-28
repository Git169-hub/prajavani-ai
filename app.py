import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

# Page config
st.set_page_config(
    page_title="Prajavani AI - Government Schemes Assistant",
    page_icon="🏛️",
    layout="centered"
)

st.title("🏛️ Prajavani AI")
st.subheader("Indian Government Schemes Assistant")
st.caption("PM Kisan • Ayushman Bharat • MGNREGA • PM Awas Yojana • Atal Pension")
st.divider()

# Load once using cache
@st.cache_resource
def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    return retriever, client

retriever, client = load_rag()

def answer_query(query):
    docs = retriever.invoke(query)
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
    return response.choices[0].message.content, sources

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            st.caption(f"📚 Sources: {', '.join(msg['sources'])}")

# Input
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
