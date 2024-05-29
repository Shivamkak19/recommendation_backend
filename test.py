import requests
import json


# Define the payload
payload = {
    "username": "manuel",
    "video_uuid": "01FStJQwf2KxmGZMgioI",  # Replace with the actual base64 image string
    "update_fields": {}
}

payload2 = {
    "k": 10
}

payload3 = {
    "query" : "cat"
}

payload4 = {
    "username": "manuel"
}

# Define the headers
headers = {
    'Content-Type': 'application/json'
}

print("hello")
# Make the POST request to the Flask API endpoint
response = requests.post('http://localhost:5000/api/keyword_search', headers=headers, data=json.dumps(payload3))

# Print the response
if response.status_code == 200:
    pass
    # print('Success:', response.json())
else:
    pass
    # print('Failed:', response.status_code, response.text)
