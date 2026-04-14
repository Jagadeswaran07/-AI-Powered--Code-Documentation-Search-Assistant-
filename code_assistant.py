import streamlit as st
from endee import EndeeClient
from sentence_transformers import SentenceTransformer
import subprocess
import tempfile

st.set_page_config(page_title="Code Assistant", layout="wide")

st.title("🤖 AI Code Documentation Assistant")
st.markdown("Ask questions about your codebase in plain English")

# Initialize
@st.cache_resource
def init():
    return {
        'client': EndeeClient(host='localhost', port=8080),
        'model': SentenceTransformer('all-MiniLM-L6-v2')
    }

components = init()

# Sidebar - Project setup
with st.sidebar:
    st.header("📁 Project Setup")
    
    repo_url = st.text_input("GitHub Repository URL", 
                             placeholder="https://github.com/user/repo")
    
    if st.button("📥 Clone & Index Repository"):
        with st.spinner("Cloning and indexing..."):
            # Clone repo
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            subprocess.run(f"git clone {repo_url}", shell=True)
            
            # Index code
            ingestor = CodeIngestor()
            count = ingestor.index_codebase(f"./{repo_name}")
            st.success(f"✅ Indexed {count} code components")
    
    st.divider()
    st.info("💡 Example questions:\n- Where is the login function?\n- Show me database queries\n- How is authentication handled?")

# Main chat interface
query = st.text_input("💬 Ask about your code:")

if query:
    # Search in codebase
    query_vec = components['model'].encode([query])[0]
    results = components['client'].query('codebase', query_vec.tolist(), top_k=3)
    
    st.subheader("🔍 Found in your code:")
    
    for result in results:
        with st.expander(f"📄 {result['metadata']['file']} - {result['metadata']['type']}: {result['metadata']['name']} (Score: {result['score']:.2f})"):
            st.code(result['metadata']['code'], language='python')
            st.caption(f"Description: {result['metadata']['description']}")

# Quick demo
with st.expander("🎬 Try Demo"):
    st.code("""
    Questions you can ask:
    1. "Find authentication code"
    2. "Where are API endpoints defined?"
    3. "Show me database connection code"
    4. "What functions handle user input?"
    """)
