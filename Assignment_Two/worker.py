#!/usr/bin/python
from pygit2 import Repository, clone_repository
from radon.complexity import cc_visit, cc_rank
import json

class Worker():
    def __init__(self, mainHost, mainPort):
        self.mainAddr = mainHost
        self.mainPort = mainPort
    def getRepository():
    	try:
            repo = Repository('./repo')
    	except:
            repo_url = 'https://github.com/rubik/radon.git'
            repo_path = './repo'
            repo = clone_repository(repo_url, repo_path)
        return repo

    def computeComplexity(code):
    def getWork():
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect(self.mainAddr, self.mainPort)

	work = self.request.recv(1024)
	work = json.loads(msg)

    def doWork(work):
	complexity = []
	for files in work:
	    complexity.append(computeComplexity(files)
	return complexity

    def sendResults(complexity):
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect(self.mainAddr, self.mainPort)
	
	result = json.dumps({"Result: " : complexity})
	socket.sendall(result)

if __name__ == '__main__':

