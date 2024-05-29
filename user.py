import firebase_admin
from firebase_admin import credentials, firestore, storage
import base64
import io
import numpy as np
import random
import torch
import open_clip

# Initialize Firebase Admin SDK
# Initialize Firebase Admin SDK with a unique name
cred = credentials.Certificate('./firebase_certificate.json')
try:
    firebase_admin.get_app('user1')  # Try to get the app with the unique name
except ValueError:
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'video-storage-a70c9.appspot.com'
    }, name='user1')

# Initialize Firestore for the named app
db = firestore.client(firebase_admin.get_app('user1'))

# take image stored locally and store on Firebase storage
def add_profile_pic(name, img_base64):
    try:
        # Initialize Firestore Storage
        bucket = storage.bucket()

        # Decode the base64 image
        img_data = base64.b64decode(img_base64)
        img_io = io.BytesIO(img_data)

        # Create a new blob and upload the image data
        blob = bucket.blob(f'ProfilePictures/{name}')
        blob.upload_from_file(img_io, content_type='image/png')

        # Make the blob publicly viewable
        blob.make_public()

        # Return the public URL
        return blob.public_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def add_new_user(username, b64, img_name):
    # Check if a user document with the given username already exists
    user_ref = db.collection('Users').document(username)
    doc = user_ref.get()

    if doc.exists:
        print(f"User with username {username} already exists.")
        return "user name exists"
    else:
        # Define the user schema including the Views field
        user_data = {
            "uuid": "some-unique-uuid",
            "description": "A description about the user.",
            "tags": ["tag1", "tag2"],
            "profilePic": add_profile_pic(name=img_name, img_base64=b64),
            "posts": [],
            "likedPosts": [],
            "followerCount": 0,
            "followCount": 0,
            "likeCount": 0,
            "friendsCount": 0,
            "Views": {
            }
        }

        # Create the user document with the embedded Views field
        user_ref.set(user_data)
        print(f"User document created for username: {username}")


        return "user add success"



def add_view(username, uuid):

    # Define the Views collection schema
    views_data = {
        "timeSpent": 0,
        "numWatches": 0,
        "uniqueSessions": 0,
        "didShareBool": False,
        "didViewComment": False,
        "didLike": False,
        "didSave": False
    }

    # Create a document in the Views subcollection with the video UUID
    view_ref = db.collection('Users').document(username).collection('Views').document(uuid)
    view_ref.set(views_data)
    print(f"View document created with UUID: {uuid}")

    return "add view success"

def update_view(username, uuid, update_fields):
    # Create a document in the Views subcollection with the video UUID
    view_ref = db.collection('Users').document(username).collection('Views').document(uuid)

    # Update the document with the fields from the update_fields dictionary
    view_ref.update(update_fields)
    print(f"View document with UUID: {uuid} updated with fields: {update_fields}")

    return "update view success"

# Given user uuid, calculate weighted average of videos watched
def calculate_ideal_embedding(user_uuid):
    try:
        # Reference to the Views collection for the given user
        views_ref = db.collection('Users').document(user_uuid).collection('Views')

        # Retrieve all documents in the Views collection
        views_docs = views_ref.stream()

        video_uuids = []
        weights = []

        # Extract video UUIDs, numWatches, and timeSpent from each document
        for doc in views_docs:
            data = doc.to_dict()
            if 'numWatches' in data and 'timeSpent' in data:
                video_uuids.append(doc.id)
                weight = data['numWatches'] * data['timeSpent']
                weights.append(weight)

        if not video_uuids or not weights:
            print("No video UUIDs or weights found for the user.")
            return None

        embeddings_list = []

        # Fetch corresponding documents from the Post collection
        for video_uuid in video_uuids:
            post_doc = db.collection('Post').document(video_uuid).get()
            if post_doc.exists:
                post_data = post_doc.to_dict()
                if 'embeddings' in post_data:
                    embeddings_list.append(post_data['embeddings'])

        if not embeddings_list:
            print("No embeddings found in the Post collection.")
            return None

        # Convert to numpy arrays for easier computation
        embeddings_array = np.array(embeddings_list)
        weights_array = np.array(weights)

        # Compute the weighted average embedding
        weighted_avg_embedding = np.average(embeddings_array, axis=0, weights=weights_array)

        # print("Weighted Average Embedding:", weighted_avg_embedding)
        return weighted_avg_embedding

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
# Perform basic recommendation that takes input of user id and returns
# top K recommended videos based on user's liked videos
def basic_recommendation(user_uuid, k=20):
    ideal_embedding = calculate_ideal_embedding(user_uuid=user_uuid)

    if ideal_embedding is None:
        return []

    posts_ref = db.collection('Post')
    post_docs = posts_ref.stream()

    embeddings_list = []
    doc_ids = []
    video_urls = []

    doc_list = []

    for doc in post_docs:
        data = doc.to_dict()
        doc_list.append(data)

        if 'embeddings' in data and "id" in data and "videoURL" in data:
            embeddings_list.append(data['embeddings'])
            doc_ids.append(data['id'])
            video_urls.append(data['videoURL'])

    if not embeddings_list:
        print("No embeddings found in the post collection.")
        return None

    embeddings_array = np.array(embeddings_list)
    
    # Find the K nearest neighbors
    k_indices = knn_indices(IDEAL=ideal_embedding, ALL_ARRAYS=embeddings_array, k=k)

    # Prepare the result
    k_matches = [{
        "id": doc_ids[idx],
        "embedding": embeddings_array[idx].tolist(),  # Convert to list for JSON serialization
        "video_url": video_urls[idx]
    } for idx in k_indices]

    # Extract just the video URLs
    k_matches_url = [match['video_url'] for match in k_matches]

    # Compute the average embedding of the recommended videos
    recommended_embeddings = embeddings_array[k_indices]
    avg_embedding = np.mean(recommended_embeddings, axis=0).tolist()  # Convert to list for JSON serialization

    response = {
        "k_match_url": k_matches_url,
        "avg_embedding": avg_embedding
    }

    return response

def knn_indices(IDEAL, ALL_ARRAYS, k = 10):
    # Step 1: Calculate the distances
    distances = np.linalg.norm(ALL_ARRAYS - IDEAL, axis=1)
    
    # Step 2: Find the indices of the k smallest distances
    k_indices = np.argpartition(distances, k)[:k]
    
    # Step 3: Sort the k smallest distances
    k_sorted_indices = k_indices[np.argsort(distances[k_indices])]
    
    # Step 4: Retrieve the k nearest neighbors
    # K_MATCHES = ALL_ARRAYS[k_sorted_indices]
    
    return k_sorted_indices

def random_recommendation(k = 20):
    posts_ref = db.collection('Post')
    post_docs = posts_ref.stream()

    doc_list = []

    for doc in post_docs:
        data = doc.to_dict()
        doc_list.append(data)
    
    # Find the K nearest neighbors
    k_indices = [random.randint(0, len(doc_list) - 1) for _ in range(k)]

    k_matches = [doc_list[i] for i in k_indices]

    response = {
        "k_match_url": k_matches,
    }

    return response

# text embedding
def getTextEmbedding(searchQuery):
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='laion2b_s34b_b79k')


    tokenizer = open_clip.get_tokenizer('ViT-B-32')

    # searchQuery = "a dog"
    # text =  tokenizer([searchQuery])
    # print(type(text))
    text = [open_clip.tokenize(searchQuery)]

    with torch.no_grad(), torch.cuda.amp.autocast():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    return text_features


# Takes CLIP embedding of text, compares KNN with all videos in Firestore
def query_search(text_query, k = 10):

    print("gate 1")
    ideal_embedding = getTextEmbedding(text_query).numpy()

    print(ideal_embedding)
    print("gate 2")

    posts_ref = db.collection('Post')

    print("gate 3")

    post_docs = posts_ref.stream()

    print("gate 4")


    embeddings_list = []
    doc_ids = []
    video_urls = []

    doc_list = []

    # print(sum(1 for _ in post_docs))

    for doc in post_docs:
        data = doc.to_dict()
        # print(data['id'])
        doc_list.append(data)

        if 'embeddings' in data and "id" in data and "videoURL" in data:
            embeddings_list.append(data['embeddings'])
            doc_ids.append(data['id'])
            video_urls.append(data['videoURL'])

    if not embeddings_list:
        print("No embeddings found in the post collection.")
        return None

    embeddings_array = np.array(embeddings_list)

    print("gate 5")

    if not embeddings_list:
        print("No embeddings found in the post collection.")
        return None

    embeddings_array = np.array(embeddings_list)
    
    print("gate 6")
    # Find the K nearest neighbors
    k_indices = knn_indices(IDEAL=ideal_embedding, ALL_ARRAYS=embeddings_array, k=k)
    k_matches = [doc_list[i] for i in k_indices]

    print("gate 7")

    for _, el in enumerate(k_matches):
        print(el["videoURL"])

    response = {
        "k_match_url": k_matches
    }

    return response



# #####################################################################
# #####################################################################
# #####################################################################
# #####################################################################
