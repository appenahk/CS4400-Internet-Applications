#!/usr/bin/python
from radon.complexity import cc_visit, cc_rank
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import json
import requests 

cc_config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
)
def getToken():
    with open('github_token', 'r') as file_handle:
            return file_handle.read().split()[0]

def getWork():
    response = requests.get('http://127.0.0.1:1759/work', params={'key': 'value'})
    #response.encoding = 'utf-8'

    commits = response.json()['commit']
    py_files = []

    payload = {'access_token': getToken()}
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    for item in tree:
        if item['type'] == 'blob' and pyFile(item['path']):
           py_files.append(item['path'])

    os.makedirs('tmp')
    for index, url in enumerate(py_files):
        response = requests.get(url, params=payload, headers=headers)

        with open('./tmp/{}.py'.format(index), 'w') as tmp_file:
             tmp_file.write(response.text)

    return py_files

def computeComplexity(code):
    complexity = CCHarvester(cc_filepath, cc_config)
    
def doWork():
	work = getWork()
	complexity = []
	for files in work:
	    complexity.append(computeComplexity(files))
	return complexity

def sendResults(complexity):
	result = {"Result: " : complexity}
	post = requests.post('http://127.0.0.1:1759/result', json=result)

def pyFile(self, filename):
        return True if match('.*\.py', filename) is not None else False

if __name__ == '__main__':
    bool = True
    while bool: #run until work is finished
      
        result = doWork(work)
        sendResults(result)
