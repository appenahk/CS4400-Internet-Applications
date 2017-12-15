import time
from flask import Flask, request, jsonify
import requests, sys

app = Flask(__name__)
commits = []
received = 0
next_commit = 0
time_start = time.clock()
time_finish = time.clock()
#num_workers = sys.argv[1]

def getCommits():
    url = 'https://api.github.com/repos/frcs/EE4C16-self-driving-lab/commits'
    global commits
    with open('github-token.txt', 'r') as token_file:
        token = token_file.read()
        payload = {'access_token': token}
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    response = requests.get(url, params=payload, headers=headers)

    for elem in response.json():
        commits.append(elem["commit"]["tree"]["url"])
    return commits

@app.route('/work', methods=['GET'])
def sendWork():
    queue = getCommits()
    global next_commit
    try:
        while next_commit <= len(queue):
            sendCommit = queue[next_commit]
            next_commit += 1
            print(next_commit)
            sentWork = {"commit": sendCommit}
            return jsonify(sentWork)
    except:
        return {"commit": "complete"}


@app.route('/result', methods=['POST'])
def result():
    result = request.json()['complexity']
    global total_cc
    total_cc+= int(result)
    num += 1
    if num == next_commit:
        average = total/next_commit
        print("Complexity of Repository: ", total)
        print("Average: ", average)
        shutdown_server()
    return 'Submission Received'

def shutdown_server():

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    next_commit = 0
    time_start = time.clock()
    app.run(port=6790, threaded=True, debug=True)
    time_finish = time.clock()
    total_time = time_start - time_finish
    print("Total time taken was: " + str(total_time))
    with open('results.txt', 'a') as results:
        results.write('Workers: {}\nTime: {}\n'.format(1, total_time))