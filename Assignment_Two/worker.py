#!/usr/bin/python
from pygit2 import Repository, clone_repository
from radon.complexity import cc_visit, cc_rank
import json

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
def doWork():
def sendResults():

