from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Union
import json
import glob
import pandas as pd
from datasets import Dataset, DatasetDict
import os

class EmbeddingGenerator:
    def __init__(self, model_name: str = "intfloat/e5-large-v2"):
        """
        Initialize the embedding generator with the specified model.
        
        Args:
            model_name (str): Name of the model to use for generating embeddings
        """
        self.model = SentenceTransformer(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate_embeddings(self, texts: Union[str, List[str]], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for the given texts.
        
        Args:
            texts (Union[str, List[str]]): Single text or list of texts to generate embeddings for
            batch_size (int): Batch size for processing multiple texts
            
        Returns:
            np.ndarray: Array of embeddings
        """
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]
            
        # Prefix for e5 models as per their requirements
        texts = [f"passage: {text}" for text in texts]
        
        # Generate embeddings
        with torch.no_grad():
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
        
        return embeddings

    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            emb1 (np.ndarray): First embedding
            emb2 (np.ndarray): Second embedding
            
        Returns:
            float: Cosine similarity score
        """
        return float(np.dot(emb1, emb2))

if __name__ == "__main__":
    # Example usage
    generator = EmbeddingGenerator()

    file_paths = glob.glob("../corpus/*.json")
    data = []
    for file_path in file_paths:
        with open(file_path, "r") as f:
            file_data = json.load(f)
            for chunk in file_data["chunks"]:
                data.append({
                    "heading": chunk["heading"],
                    "content": chunk["content"],
                    "source_url": file_data["source_url"],
                    "text": "passage: " + chunk["heading"] + "\n" + chunk["content"]
                })

    # Create huggingface dataset
    dataset = Dataset.from_list(data)

    # Generate embeddings
    embeddings = generator.generate_embeddings(dataset["text"])
    # Convert embeddings to list before adding as column
    embeddings_list = embeddings.tolist()
    dataset = dataset.add_column("embeddings", embeddings_list)

    print(f"Generated embeddings shape: {embeddings.shape}")

    save_dir = os.path.join(os.path.dirname(__file__), "..", "embedded_corpus")
    os.makedirs(save_dir, exist_ok=True)
    dataset.save_to_disk(save_dir)
    print(f"Saved embedded corpus to {save_dir}")
