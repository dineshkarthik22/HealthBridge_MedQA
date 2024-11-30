from transformers import AutoTokenizer, AutoModel
import faiss
import numpy as np
import torch
import openai

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-small-v2")
model = AutoModel.from_pretrained("intfloat/e5-small-v2")

# Function to create embeddings
def create_embeddings(corpus):
    # Tokenize and generate embeddings
    inputs = tokenizer(corpus, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Take the mean of all token embeddings
    return embeddings

# Dummy corpus
corpus = ["This is a medical document.", "Patient is diagnosed with diabetes.", "The doctor recommends regular exercise."]
embeddings = create_embeddings(corpus)
print(embeddings.shape)  # Printing the shape of the embeddings tensor

# Convert list of embeddings to a numpy array (FAISS works with numpy arrays)
embedding_matrix = np.array(embeddings).astype('float32')

# Create a FAISS index for storing the embeddings
dimension = embedding_matrix.shape[1]  # The dimension of each embedding
index = faiss.IndexFlatL2(dimension)  # L2 distance index for similarity search
index.add(embedding_matrix)

# Now, the FAISS index contains the vectors and can be queried later
def query_vector_database(query, index, tokenizer, model):
    # Convert query to embedding
    query_embedding = create_embeddings([query])[0]  # Use the same create_embeddings function for the query
    query_embedding = np.array([query_embedding]).astype('float32')
    # Search for the top 3 most similar embeddings in the FAISS index
    D, I = index.search(query_embedding, k=3)
    
    return D, I

query = "What treatment is available for cancer?"
distances, indices = query_vector_database(query, index, tokenizer, model)
similar_docs = [corpus[i] for i in indices[0]]
print("Similar documents found:")
for doc in similar_docs:
    print(doc)

def llm(prompt):
    openai.api_key = "your-api-key"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

print("Checking if the above code works...")
try:
    response = llm("What treatment is available for diabetes?")
    print(response)
except Exception as e:
    print(f"Error: {e}")