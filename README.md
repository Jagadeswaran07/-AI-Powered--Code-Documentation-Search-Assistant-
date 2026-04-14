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
Here’s a **clear, professional “OUTPUT” section** you can add to your project / README / viva 👇

---

# 📊 Project Output

## 🧠 1. AI Code Documentation Assistant

### 🔍 User Input

```
Where is the authentication logic?
```

### ✅ System Output

```
🔍 Found in your code:

📄 demo_project/app.py - function: authenticate_user (Score: 0.92)

def authenticate_user(username, password):
    """Verify user credentials"""
    return username == "admin" and password == "secret"

Description: Verify user credentials
```

---

### 🔍 User Input

```
Show me database functions
```

### ✅ System Output

```
📄 demo_project/app.py - function: get_database_connection (Score: 0.89)

def get_database_connection():
    """Create database connection"""
    return {"host": "localhost", "port": 5432}

Description: Create database connection
```

---

### 💬 What the Output Shows

* 📂 File location of code
* 🧩 Function/Class name
* 💻 Actual code snippet
* 📝 Description (docstring)
* 📊 Relevance score

👉 This proves the system understands **natural language queries** and retrieves **relevant code intelligently**.

---

# 🎯 2. Smart Product Recommender System

## 🔍 User Input

```
something for gaming
```

## ✅ System Output

```
📦 Recommendations:

🎮 Gaming Laptop (Score: 0.95)
High performance laptop for gaming with RTX 3060

🎧 Gaming Headset (Score: 0.91)
Surround sound headset for gaming

⌨️ Mechanical Keyboard (Score: 0.87)
RGB mechanical keyboard with blue switches
```

---

## 🔄 User Action

```
Select: Gaming Laptop
```

## ✅ System Output

```
Products similar to Gaming Laptop:

• Gaming Headset - Surround sound headset for gaming  
• Mechanical Keyboard - RGB mechanical keyboard  
• Wireless Mouse - Ergonomic wireless mouse  
```

---

# 📈 Final Output Summary

## 🔹 Code Assistant

* Converts code into **vector embeddings**
* Converts query into **vector**
* Finds **most relevant code snippets**
* Displays results instantly

## 🔹 Recommender System

* Understands **meaning of user query**
* Suggests **contextually similar products**
* Works beyond keyword matching

Code Assistant – Web UI Mockup
┌─────────────────────────────────────────────────────────────────────────────┐
│  🤖 AI Code Documentation Assistant                                        │
│  Ask questions about your codebase in plain English                        │
├───────────────────────────────┬─────────────────────────────────────────────┤
│  📁 Project Setup             │  💬 Ask about your code:                     │
│                               │  ┌───────────────────────────────────────┐  │
│  GitHub Repository URL        │  │ Where is the authentication logic?   │  │
│  [https://github.com/...   ]  │  └───────────────────────────────────────┘  │
│                               │                                             │
│  [📥 Clone & Index Repository]│  🔍 Found in your code:                     │
│                               │                                             │
│  ─────────────────────────    │  📄 demo_project/app.py - function:        │
│  💡 Example questions:        │     authenticate_user (Score: 0.94)        │
│  • Where is the login func?   │  ┌───────────────────────────────────────┐  │
│  • Show me database queries   │  │ def authenticate_user(username, pwd): │  │
│  • How is authentication done?│  │     """Verify user credentials"""      │  │
│                               │  │     return username=="admin" and ...   │  │
│                               │  └───────────────────────────────────────┘  │
│                               │  Description: Verify user credentials       │
│                               │                                             │
│                               │  📄 demo_project/app.py - function:        │
│                               │     handle_api_request (Score: 0.72)        │
│                               │  ┌───────────────────────────────────────┐  │
│                               │  │ def handle_api_request(data):         │  │
│                               │  │     """Process incoming API request"""│  │
│                               │  │     return {"status":"success",...}    │  │
│                               │  └───────────────────────────────────────┘  │
└───────────────────────────────┴─────────────────────────────────────────────┘
code output:

📄 demo_project/app.py - function: authenticate_user (Score: 0.94)
┌─────────────────────────────────────────────────────────────┐
│ def authenticate_user(username, password):                 │
│     """Verify user credentials"""                          │
│     return username == "admin" and password == "secret"    │
└─────────────────────────────────────────────────────────────┘
Description: Verify user credentials

📄 demo_project/app.py - function: handle_api_request (Score: 0.52)
┌─────────────────────────────────────────────────────────────┐
│ def handle_api_request(data):                              │
│     """Process incoming API request"""                     │
│     return {"status": "success", "data": data}             │
└─────────────────────────────────────────────────────────────┘

