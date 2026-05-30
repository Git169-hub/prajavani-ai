**# 🏛️ Prajavani AI — Government Schemes Assistant**



**A bilingual RAG chatbot that answers questions about Indian government** 

**welfare schemes in Telugu and English.**



**Built for rural Telugu-speaking citizens who cannot navigate** 

**government websites.**



**---**



**## 🎯 Problem**



**Rural citizens in Andhra Pradesh and Telangana are eligible for** 

**government welfare schemes but cannot access information because:**

**- Government websites are in English only**

**- Information is scattered across multiple portals**

**- No conversational interface exists in Telugu**



**## 💡 Solution**



**A RAG-powered chatbot that:**

**- Accepts questions in Telugu or English**

**- Retrieves relevant information from indexed scheme documents**

**- Answers in the same language the user asked in**

**- Cites the source scheme for every answer**



**---**



**## 📊 Performance**



**| Metric | Result |**

**|---|---|**

**| Test queries run | 20 |**

**| Retrieval accuracy | 100% (20/20) |**

**| Languages supported | Telugu, English |**

**| Schemes covered | 5 |**

**| Total chunks indexed | 217 |**



**\*\*Known limitation:\*\* Cross-scheme queries and PM Awas Yojana** 

**application steps return partial results. Telugu corpus added** 

**in v2 to fix regional language retrieval failures.**



**---**



**## 🏗️ Architecture**



**User Query (Telugu/English)**

**↓**

**Language Detection (Unicode range check)**

**↓**

**HuggingFace Embeddings (all-MiniLM-L6-v2)**

**↓**

**ChromaDB Vector Search (k=6)**

**↓**

**Language Filter (Telugu chunks for Telugu queries)**

**↓**

**Groq LLaMA 3.1 8b Instant**

**↓**

**Answer in user's language + source citation**



**---**



**## 📋 Schemes Covered**



**| Scheme | Language |**

**|---|---|**

**| PM Kisan Samman Nidhi | English + Telugu |**

**| Ayushman Bharat (PMJAY) | English + Telugu |**

**| MGNREGA | English + Telugu |**

**| PM Awas Yojana | English + Telugu |**

**| Atal Pension Yojana | English + Telugu |**



**---**



**## 🛠️ Tech Stack**



**| Component | Technology |**

**|---|---|**

**| LLM | Groq LLaMA 3.1 8b Instant |**

**| Embeddings | HuggingFace all-MiniLM-L6-v2 |**

**| Vector DB | ChromaDB |**

**| Framework | LangChain |**

**| UI | Streamlit |**

**| Deployment | Streamlit Cloud |**



**---**



**## 🚀 Run Locally**



**```bash**

**git clone https://github.com/YOUR\_USERNAME/prajavani-ai**

**cd prajavani-ai**

**pip install -r requirements.txt**

**```**



**Add your Groq API key to `.streamlit/secrets.toml`:**

**GROQ\_API\_KEY = "your\_grok\_key"**



**Index the documents:**

**```bash**

**python index\_schemes.py**

**```**



**Run the app:**

**```bash**

**streamlit run app.py**

**```**



**---**



**## 📁 Project Structure**



**scheme\_rag/**

**├── app.py                  # Streamlit UI**

**├── rag\_engine.py           # RAG logic + language detection**

**├── index\_schemes.py        # Document ingestion**

**├── data/**

**│   ├── pm\_kisan.txt**

**│   ├── pm\_kisan\_telugu.txt**

**│   ├── ayushman\_bharat.txt**

**│   ├── ayushman\_bharat\_telugu.txt**

**│   ├── mgnrega.txt**

**│   ├── mgnrega\_telugu.txt**

**│   ├── pm\_awas\_yojana.txt**

**│   ├── pm\_awas\_yojana\_telugu.txt**

**│   ├── atal\_pension.txt**

**│   └── atal\_pension\_telugu.txt**

**├── chroma\_db/              # Vector index**

**└── requirements.txt**



**---**



**## 🔮 Future Improvements**



**- Add more schemes (PM Mudra, Sukanya Samriddhi, etc.)**

**- Improve Telugu retrieval with dedicated Telugu embeddings**

**- Add voice input for low-literacy users**

**- Expand to other Indian languages (Hindi, Tamil, Kannada)**



**---**



**## 👤 Author**



**\*\*Razak Shaik\*\***  

**VIT-AP University | CS Final Year**  

**\[LinkedIn](https://linkedin.com/in/YOUR\_PROFILE) |** 

**\[GitHub](https://github.com/YOUR\_USERNAME)**

