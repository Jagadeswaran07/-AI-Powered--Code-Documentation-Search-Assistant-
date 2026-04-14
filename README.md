# 🚀 AI-Powered Code Documentation & Search Assistant

## 🔍 Overview
This project is an intelligent AI-powered system designed to simplify code understanding and exploration. It allows developers to upload or index their codebase and interact with it using natural language queries. Instead of manually searching through files, users can ask questions like *“Where is the authentication logic?”* or *“Show me database functions”* and instantly receive relevant code snippets with explanations.

In addition to code search, the project also includes a **Smart Product Recommender System**, demonstrating how semantic search can be applied to real-world use cases beyond programming.

---

## 💡 Key Features
- 🔎 **Natural Language Code Search** – Ask questions in plain English  
- 🧠 **Semantic Understanding** – Uses embeddings to understand meaning, not just keywords  
- 📂 **Code Indexing Pipeline** – Extracts functions, classes, and docstrings automatically  
- ⚡ **Fast Vector Search** – Powered by Endee vector database  
- 🎯 **Smart Recommender System** – Suggests similar products based on context  
- 🖥️ **Interactive UI** – Built using Streamlit for an easy user experience  

---

## 🛠️ Tech Stack
- **Python** – Core programming language  
- **Streamlit** – Frontend interface  
- **Endee** – Vector database for similarity search  
- **Sentence Transformers** – Embedding generation  
- **Docker** – Containerized database setup  

---

## ⚙️ How It Works
1. Code files are parsed to extract meaningful components (functions/classes)  
2. Each component is converted into vector embeddings  
3. User queries are also converted into vectors  
4. Endee performs similarity search to find the most relevant results  
5. Matching code snippets are displayed instantly  

---

## ▶️ Getting Started
```bash
# Start vector database
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run Code Assistant
streamlit run code_assistant.py

# Run Recommender System
streamlit run smart_recommender.py
