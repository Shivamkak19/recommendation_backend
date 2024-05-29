import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
# cred = credentials.Certificate('./firebase_certificate.json')
# firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


# Specify the collection name
collection_name = 'Post'

# Get all documents in the collection
def iterate_over_documents():
    try:
        # Stream all documents in the collection
        docs = db.collection(collection_name).stream()

        # Iterate over the documents
        for doc in docs:
            print(f'Document ID: {doc.id}')
            print(f'Document Data: {doc.to_dict()}')
    except Exception as e:
        print(f'An error occurred: {e}')

# Call the function to iterate over documents
iterate_over_documents()



