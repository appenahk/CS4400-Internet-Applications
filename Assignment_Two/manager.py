#!/usr/bin/python
from time import time
from flask import Flask
import requests

app = Flask(__name__)
url = 'https://api.github.com/repos/rubik/radon/commits'
def getCommits():
    
    commits = []
    with open('github-token.txt', 'r') as token_file:
        token = token_file.read().split()[0] 
        payload = {'access_token': token}

    response = requests.get(url, param=payload)
    while 'next' in response.links:
        for elem in response.get_json():
            commits.append(elem['commit']['tree']['url'])

    for elem in response.get_json():
        commits.append(elem['commit']['tree']['url'])
    return commits

@app.route('/work' , methods=['GET'])
def sendWork():
    commits = getCommits()
    global next
    while next <= len(commits) 
	  next += 1
	  sentWork = jsonify({"commit": commits[next]})
	  return sentWork

@app.route('/result', methods=['POST'])
def result():
    result = request.get_json()
    result_list.append(result)

if __name__ == '__main__':
    next = 0
    
    global result_list
    result_list = []
    app.run(threaded=True, debug=True)
