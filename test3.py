import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Example text embeddings and corresponding texts
# In practice, you would load these from your data source
text_embeddings = np.array([
    [-4.00782041e-02, -2.32758243e-02, -3.22345831e-02, -2.01723762e-02, 5.22377109e-03, ...], # embedding for text 1
    [...], # embedding for text 2
    [...], # embedding for text 3
    # Add more embeddings as needed
])
texts = [
    "Example text 1",
    "Example text 2",
    "Example text 3",
    # Add more texts corresponding to the embeddings
]

# The given embedding to find the closest text for
given_embedding = np.array([[-4.00782041e-02, -2.32758243e-02, -3.22345831e-02, -2.01723762e-02, 5.22377109e-03, ...]])

# Compute cosine similarity between the given embedding and all other embeddings
similarity_scores = cosine_similarity(given_embedding, text_embeddings)

# Find the index of the most similar embedding
most_similar_index = np.argmax(similarity_scores)

# Get the corresponding text
most_similar_text = texts[most_similar_index]

print(f"The text that the given embedding represents is: {most_similar_text}")
