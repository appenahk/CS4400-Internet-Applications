#!/usr/bin/python
from time import time
from flask import Flask
import requests

app = Flask(__name__)

def getCommits():
    url = 'https://api.github.com/repos/rubik/radon/commits'
    commits = []
    with open('github-token.txt', 'r') as token_file:
        token = token_file.read().split()[0] 
        payload = {'access_token': token}

    response = requests.get(url, param=payload)
    while 'next' in response.links:
        for elem in response.json():
            commits.append(elem['commit']['tree']['url'])
	response = requests.get(response.links['next']['url'], params=payload)

    for elem in response.json():
        commits.append(elem['commit']['tree']['url'])
    return commits

@app.route('/work' , methods=['GET'])
def sendWork():
    commits = getCommits()
    global next_commit
    try:
	while next_commit <= len(commits) 	
	      sendCommit = commits[next_commit]
    	      next_commit += 1
	  
	      sentWork = {"commit": sendCommit}
	      return jsonify(sentWork)
    except:
	return None
@app.route('/result', methods=['POST'])
def result():
    result = request.get_json()
    result_list.append(result)

if __name__ == '__main__':
    next_commit = 0   
    global result_list
    result_list = []
    app.run(threaded=True, debug=True)
