import os
import ast
from pathlib import Path
from endee import EndeeClient
from sentence_transformers import SentenceTransformer
import hashlib

class CodeIngestor:
    def __init__(self):
        self.client = EndeeClient(host='localhost', port=8080)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_code_chunks(self, file_path):
        """Extract functions, classes, and comments from code"""
        chunks = []
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse Python code
        try:
            tree = ast.parse(content)
            
            # Extract functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node) or "No description"
                    code = ast.unparse(node)
                    chunks.append({
                        'type': 'function',
                        'name': node.name,
                        'description': docstring,
                        'code': code[:500],
                        'file': file_path
                    })
                
                elif isinstance(node, ast.ClassDef):
                    chunks.append({
                        'type': 'class',
                        'name': node.name,
                        'description': ast.get_docstring(node) or "No description",
                        'code': ast.unparse(node)[:500],
                        'file': file_path
                    })
        except:
            pass
        
        return chunks
    
    def index_codebase(self, directory):
        """Index entire codebase"""
        all_chunks = []
        
        for file_path in Path(directory).rglob('*.py'):
            chunks = self.extract_code_chunks(file_path)
            all_chunks.extend(chunks)
        
        # Generate embeddings and store in Endee
        for chunk in all_chunks:
            text = f"{chunk['type']}: {chunk['name']}\n{chunk['description']}\n{chunk['code']}"
            embedding = self.model.encode([text])[0]
            
            self.client.upsert('codebase', [{
                'id': hashlib.md5(text.encode()).hexdigest(),
                'vector': embedding.tolist(),
                'metadata': chunk
            }])
        
        return len(all_chunks)

if __name__ == "__main__":
    ingestor = CodeIngestor()
    count = ingestor.index_codebase('./my_project')
    print(f"✅ Indexed {count} code components")
