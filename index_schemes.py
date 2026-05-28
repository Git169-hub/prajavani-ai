from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Load all scheme files
data_dir = "data"
documents = []

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(data_dir, filename), encoding="utf-8")
        docs = loader.load()
        # Tag each doc with scheme name
        for doc in docs:
            doc.metadata["scheme"] = filename.replace(".txt", "")
        documents.extend(docs)
        print(f"✓ Loaded {filename}")

print(f"\nTotal documents loaded: {len(documents)}")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"Total chunks created: {len(chunks)}")

# Create embeddings and store in ChromaDB
print("\nCreating embeddings... (first time takes 2-3 minutes)")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("\n✓ Index created and saved to chroma_db/")
print(f"✓ Total chunks indexed: {len(chunks)}")
