import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
# cred = credentials.Certificate('./firebase_certificate.json')
# firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


# Specify the collection name
collection_name = 'Post'

posts_ref = db.collection(collection_name)
top_posts = posts_ref.limit(10).get()

# Print the retrieved items
for post in top_posts:
    print(f'{post.id} => {post.to_dict()}')
