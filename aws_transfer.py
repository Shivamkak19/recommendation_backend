import firebase_admin
from firebase_admin import credentials, firestore
import boto3
import time

# ######################################################################
import os

f = open("data.txt", "r")

lines = f.readlines()

def extract_name(file_path):
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return name


tMap = {}
for idx, line_ in enumerate(lines):
    line = line_.split("\t")
    author = line[1]
    description = line[2]
    vidName = line[3]
    vidName = extract_name(vidName)
    tMap[vidName] = (author, description)

# ######################################################################

# Initialize Firebase Admin SDK
# cred = credentials.Certificate('./firebase_certificate.json')
# firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# ######################################################################
# Generate titles of all scraped videos in AWS S3
s3_resource = boto3.resource('s3')

base_url = "https://video-storage-svfh2024.s3.us-west-1.amazonaws.com/"

video_list = []

pythonusecase = s3_resource.Bucket(name = 'video-storage-svfh2024')
for object in pythonusecase.objects.all():
    video = (object.key, base_url + object.key)
    video_list.append(video)

# Debug
# for i in range(len(video_list)):
#     print(i, video_list[i][0], video_list[i][1])

# Populate Firebase Firestore by iterating over all AWS Videos
# ######################################################################



def add_post_with_custom_id(video):
    post_id = generate_firestore_id()
    post_ref = db.collection('Post').document(post_id)

    data = {
        "authorName": "12",
        "author": "12",
        "caption": "12",
        "commentID": "12",
        "id": post_id,
        "likeCount": 12,
        "music": "12",
        "shareCount": 12,
        "video": video[0],
        "videoFileExtension": "mp4",
        "videoHeight": 1800,
        "videoURL": video[1],
        "videoWidth": 900
    }

    # Add the document to Firestore
    post_ref.set(data)
    print(f"Document added with ID: {post_ref.id}, video_url: {video[1]}")

def generate_firestore_id():
    import random
    import string

    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    auto_id = ''.join(random.choices(chars, k=20))
    return auto_id

# Call the function to add a post with a custom ID
# Iterate over all videos in AWS S3 Bucket
# for i in range(len(video_list)):
#     add_post_with_custom_id(video_list[i])
#     print("finished", i)

def update_post_with_custom_id(video):
    post_ref = db.collection('Post').document(video)

    print("CHECK", tMap.get(video))
    video_data = tMap.get(video)
    if video_data:
        author = video_data[0]
        authorName = video_data[0]
        caption = video_data[1]
    else:
        author = ""
        authorName = ""
        caption = ""

    update_fields = {
        "author": author,
        "authorName": authorName,
        "caption": caption
    }

    post_ref.update(update_fields)


test = "5297ccc9-7062-4832-8ed5-8432af45a085_shorts_FJXOOt9NmV0"


posts_ref = db.collection('Post')
post_docs = posts_ref.stream()

update_post_with_custom_id(test)
print("finished", test)

# for doc in post_docs:
#     file_name = doc.to_dict()["video"]
#     video_name = video_name.split('.mp4')[0]

#     update_post_with_custom_id(video_name)
#     print("finished", doc.to_dict()["videoURL"])
