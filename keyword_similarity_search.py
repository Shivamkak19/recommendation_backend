from nltk.stem import WordNetLemmatizer
import pickle
import os
from firebase_admin import credentials, firestore
import firebase_admin
import nltk
from nltk.stem import PorterStemmer
import pickle
nltk.download("punkt")




# Initialize Python porter stemmer
ps = PorterStemmer()



tMap = pickle.load(open('captionMap.pkl', 'rb'))

pickle_docs = pickle.load(open('document_new.pkl', 'rb'))

def extract_name(file_path):
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    return name

# # Initialize Firebase Admin SDK with a unique name
# cred = credentials.Certificate('./firebase_certificate.json')
# try:
#     firebase_admin.get_app('user2')  # Try to get the app with the unique name
# except ValueError:
#     firebase_admin.initialize_app(cred, {
#         'storageBucket': 'video-storage-a70c9.appspot.com'
#     }, name='user2')

# # Initialize Firestore for the named app
# db = firestore.client(firebase_admin.get_app('user2'))


def count_word_occurrences(description, word, lemmatizer):
    # Ensure the search is case-insensitive and tokenize the description
    description = description.lower()
    word = word.lower()

    lemmatized = lemmatizer.lemmatize(word)

    cnt1 = description.count(lemmatized)
    if lemmatized != word:
        cnt1 += description.count(word)

    return cnt1

def keyword_search(searchPhrase):

    nltk.download("wordnet")

    words = searchPhrase.split()
    totalMatches = []

    # posts_ref = db.collection('Post')
    # post_docs = posts_ref.stream()

    docs = []
    descriptions = []
    lemmatizer = WordNetLemmatizer()

    # update description with all documents' values
    for doc in pickle_docs:
        # video_id = doc.id

        # dock = doc.to_dict()
        
        video_id = doc["video"][:-4]
        if doc.get("caption"):  # Safely check if 'caption' key exists

            if video_id in tMap:
                video_data = tMap[video_id]
                caption = video_data[1]

                descriptions.append(caption)
                # docs.append(dock)



    for description in descriptions:
        matches = 0
        for word in words:
            matches += count_word_occurrences(description, word, lemmatizer)
        totalMatches.append(matches)


    sorted_indices = sorted(range(len(totalMatches)),
                            key=lambda i: totalMatches[i], reverse=True)

    k = 3

    topDocs = [pickle_docs[i] for i in sorted_indices[0:k]]
    print("numDocs:", len(pickle_docs))

    for _, doc in enumerate(topDocs):
        if 'cat' in doc['caption']:
            print("FOUND IT")
        print(doc["videoURL"], totalMatches[sorted_indices[_]])

    return topDocs
