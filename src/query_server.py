from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from datasets import load_from_disk
import numpy as np
import torch
from typing import List, Dict, Any

app = Flask(__name__)

# Global constants and variables
DATASET_PATH = "../embedded_corpus"  # To be populated later
model = SentenceTransformer('intfloat/e5-large-v2')
dataset = None
embedding_matrix = None

def load_embeddings():
    """Load embeddings and dataset globally"""
    global dataset, embedding_matrix
    
    if DATASET_PATH is None:
        raise ValueError("DATASET_PATH must be set before loading embeddings")
    
    # Load the dataset from huggingface
    dataset = load_from_disk(DATASET_PATH)
    
    # Convert embeddings to numpy array for efficient similarity search
    embedding_matrix = np.array(dataset['embeddings'])

def similarity_search(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Perform similarity search for the given query
    Args:
        query: Input query string
        top_k: Number of top results to return
    Returns:
        List of dictionaries containing similar documents and their metadata
    """
    # Generate embedding for the query
    query_embedding = model.encode(query, convert_to_tensor=True)
    query_embedding = query_embedding.cpu().numpy()

    # Calculate cosine similarity
    similarities = np.dot(embedding_matrix, query_embedding) / (
        np.linalg.norm(embedding_matrix, axis=1) * np.linalg.norm(query_embedding)
    )
    
    # Get top-k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Prepare results
    results = []
    for idx in top_indices.tolist():
        results.append({
            'text': dataset[idx]['text'],
            'source_url': dataset[idx]['source_url'],
            'similarity_score': float(similarities[idx])
        })
    
    return results

@app.route('/query', methods=['GET'])
def query():
    """REST endpoint for query processing"""
    try:
        query_text = "query: " + request.args.get('query')
        if not query_text:
            return jsonify({'error': 'Query parameter not provided'}), 400
        
        print("Query:", query_text)

        top_k = request.args.get('top_k', type=int, default=5)
        
        results = similarity_search(query_text, top_k)
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load embeddings when the server starts
    load_embeddings()
    app.run(host='0.0.0.0', port=5000)