import streamlit as st
from endee import EndeeClient
from sentence_transformers import SentenceTransformer
import pandas as pd

st.set_page_config(page_title="AI Recommender", layout="wide")

st.title("🎯 Smart Product Recommender")
st.markdown("*Find similar items based on meaning, not just keywords*")

# Sample product database
products = [
    {"id": 1, "name": "Gaming Laptop", "desc": "High performance laptop for gaming with RTX 3060", "category": "electronics"},
    {"id": 2, "name": "Wireless Mouse", "desc": "Ergonomic wireless mouse with long battery life", "category": "accessories"},
    {"id": 3, "name": "Mechanical Keyboard", "desc": "RGB mechanical keyboard with blue switches", "category": "accessories"},
    {"id": 4, "name": "Office Laptop", "desc": "Lightweight laptop for business and productivity", "category": "electronics"},
    {"id": 5, "name": "USB-C Hub", "desc": "Multi-port adapter for laptops", "category": "accessories"},
    {"id": 6, "name": "Gaming Headset", "desc": "Surround sound headset for gaming", "category": "audio"},
    {"id": 7, "name": "Noise Cancelling Headphones", "desc": "Wireless headphones with ANC", "category": "audio"},
]

@st.cache_resource
def init_recommender():
    client = EndeeClient(host='localhost', port=8080)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Index products
    try:
        client.create_namespace('products')
    except:
        pass
    
    for product in products:
        text = f"{product['name']} - {product['desc']}"
        embedding = model.encode([text])[0]
        client.upsert('products', [{
            'id': str(product['id']),
            'vector': embedding.tolist(),
            'metadata': product
        }])
    
    return client, model

client, model = init_recommender()

# UI
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Find Similar Products")
    
    # Method 1: Text search
    search_text = st.text_input("Describe what you're looking for:", 
                                placeholder="e.g., 'something for gaming' or 'quiet headphones'")
    
    if search_text:
        query_vec = model.encode([search_text])[0]
        results = client.query('products', query_vec.tolist(), top_k=5)
        
        st.subheader("📦 Recommendations:")
        for r in results:
            st.info(f"**{r['metadata']['name']}** (Score: {r['score']:.2f})\n{r['metadata']['desc']}")
    
    # Method 2: Similar to product
    st.subheader("🔄 Find Similar To:")
    selected = st.selectbox("Select a product", [p['name'] for p in products])
    
    if selected:
        selected_product = next(p for p in products if p['name'] == selected)
        text = f"{selected_product['name']} - {selected_product['desc']}"
        query_vec = model.encode([text])[0]
        results = client.query('products', query_vec.tolist(), top_k=4)
        
        st.subheader(f"Products similar to {selected}:")
        for r in results[1:]:  # Skip the first (same product)
            st.write(f"• **{r['metadata']['name']}** - {r['metadata']['desc']}")

with col2:
    st.subheader("📊 How It Works")
    st.markdown("""
    1. Products are converted to vectors
    2. Your search becomes a vector
    3. Endee finds semantically similar items
    4. Results ranked by relevance
    
    **Example:**
    - Search "gaming" → finds gaming laptop AND gaming headset
    - Understands context, not just keywords!
    """)

# Demo table
st.subheader("📋 Product Database")
st.dataframe(pd.DataFrame(products))
