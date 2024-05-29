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
@app.route('/api/keyword_search', methods = ["POST"])
def keyword_search():

    query = flask.request.get_json()["query"]

    "expected schema"
    '''
    "query": string
    '''

    response = keyword.keyword_search(searchPhrase = query)

    return flask.jsonify(response)
