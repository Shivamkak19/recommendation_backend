import flask
from flask import Flask, Response
import requests
import json
from flask_cors import CORS
import csv

import user as user_functions
import keyword_similarity_search as keyword

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# Login reroute
@app.route('/api/add_new_user', methods = ["POST"])
def add_new_user():

    data = flask.request.get_json()
    '''
    Expected Schema:
    'username': string, (primary key)
    'b64': string,
    'profile_image_name': string
    'description': string, 
    'tags': [string],
    'profilePic': string,
    'posts': 

    etc
    '''

    username = data["username"]
    b64 = data["b64"]
    profile_image_name = data["profile_image_name"]

    ret = user_functions.add_new_user(username= username, b64= b64, img_name= profile_image_name)

    response = {
        "response": ret
        }
    
    return flask.jsonify(response)
    

@app.route('/api/add_video_view', methods = ["POST"])
def add_video_view():

    data = flask.request.get_json()

    '''
    Expected Schema:
    'username': string
    'video_uuid': string,
    '''

    username = data['username']
    uuid = data["video_uuid"]

    ret = user_functions.add_view(username= username, uuid= uuid)

    response = {
        "response": ret
        }
    
    return flask.jsonify(response)


@app.route('/api/update_video_view', methods = ["POST"])
def update_video_view():

    data = flask.request.get_json()

    '''
    Expected Schema:
    'username': string
    'video_uuid': string,
    'update_fields': fields to be updated etc
    '''

    username = data['username']
    uuid = data["video_uuid"]
    # update_fields = data["update_fields"]

    update_fields = {
        "timeSpent": 120,
        "numWatches": 5,
        "didLike": True
    }

    ret = user_functions.update_view(username= username, uuid= uuid, update_fields= update_fields)

    response = {
        "response": ret
        }
    
    return flask.jsonify(response)



@app.route('/api/basic_recommendation', methods = ["POST"])
def basic_recommendation():

    username = flask.request.get_json()["username"]

    '''
    Expected Schema:
    'username': string
    '''

    response = user_functions.basic_recommendation(user_uuid= username, k= 20)

    return flask.jsonify(response)


@app.route('/api/avg_embedding', methods = ["POST"])
def avg_embedding():
    
    username = flask.request.get_json()["username"]

    '''
    Expected Schema:
    'username': string
    '''

    response = user_functions.calculate_ideal_embedding(user_uuid= username)

    return flask.jsonify(response)

@app.route('/api/random_recommendation', methods = ["POST"])
def random_recommendation():
    
    "expected schema"
    '''
    "k": string
    '''
    k = flask.request.get_json()["k"]

    response = user_functions.random_recommendation(k)

    return flask.jsonify(response)

@app.route('/api/semantic_search', methods = ["POST"])
def semantic_search():

    query = flask.request.get_json()["query"]

    
    "expected schema"
    '''
    "query": string
    '''

    response = user_functions.query_search(text_query= query)

    return flask.jsonify(response)


@app.route('/api/keyword_search', methods = ["POST"])
def keyword_search():

    query = flask.request.get_json()["query"]

    "expected schema"
    '''
    "query": string
    '''

    response = keyword.keyword_search(searchPhrase = query)

    return flask.jsonify(response)
