import firebase_admin
from firebase_admin import credentials, firestore, storage
import base64
import io
import numpy as np
import random
from sklearn.cluster import KMeans


# Initialize Firebase Admin SDK
# cred = credentials.Certificate('./firebase_certificate.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'video-storage-a70c9.appspot.com'
# })

# Initialize Firestore
db = firestore.client()

# Function to perform K-means clustering
def cluster_posts(k=20):
    try:
        posts_ref = db.collection('Post')
        post_docs = posts_ref.stream()

        embeddings_list = []
        doc_ids = []

        # Retrieve embeddings and document IDs
        for doc in post_docs:
            data = doc.to_dict()
            if 'embeddings' in data:
                embeddings_list.append(data['embeddings'])
                doc_ids.append(data["videoURL"])

        if not embeddings_list:
            print("No embeddings found in the post collection.")
            return []

        embeddings_array = np.array(embeddings_list)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=k, random_state=0).fit(embeddings_array)
        labels = kmeans.labels_

        # Assign clusters to documents
        clustered_docs = []
        for i, doc_id in enumerate(doc_ids):
            clustered_docs.append({
                "cluster": int(labels[i]),
                "doc_id": doc_id
            })

        return clustered_docs

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
k = 20
clustered_documents = cluster_posts(k=k)

# Sort the documents by cluster
clustered_documents.sort(key=lambda x: x['cluster'])

# Print every 20th document ordered by cluster
for i, cluster in enumerate(clustered_documents):
    if i % 20 == 0:
        print(f"Cluster: {cluster['cluster']}\n Document ID: {cluster['doc_id']}")