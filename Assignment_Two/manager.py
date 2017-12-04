#!/usr/bin/python
from pygit2 import Repository, clone_repository
from time import time

Host = "localhost"
Port = 8883

def getRepository():
    try:
        repo = Repository('./repo')
    except:
        repo_url = 'https://github.com/rubik/radon.git'
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

def getCommits(repo):
    commits = []
    for commit in repo.walk(repo):
        commits.append(repo.get(commit.id))
    return commits

def sendWork():
    repo = getRepository()
    commits = get_commits(repo)

class ThreadedHandler(SocketServer.BaseRequestHandler):
    def handle(self):

class managerServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
if __name__ == '__main__':
    address = (Host, Port)
    server = managerServer(address, ThreadedHandler)
    server.serve_forever()
