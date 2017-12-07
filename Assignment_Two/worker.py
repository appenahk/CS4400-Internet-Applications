#!/usr/bin/python
from radon.complexity import cc_visit, cc_rank
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
from shutil import rmtree
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
    with open('github-token.txt', 'r') as file_handle:
            return file_handle.read().split()[0]

def getWork():
    response = requests.get('http://localhost:5000/work', params={'key': 'value'})  
    if response.status_code == 200:    
       data = response.json()
       json_file = json_loads(data) 
       commits = json_file['commit']
    py_files = []
    payload = {'access_token': getToken()}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    
    for trees in commits:
	resp = requests.get(trees, params=payload, headers=headers))
	tree_files = resp.json()['tree']

    	for item in tree_files:
            if item['type'] == 'blob' and pyFile(item['path']):
	       tree_url = item['url']
	       filename = item['path']
	       filepath = tree_url + '<>' + filename
               py_files.append(filepath)

    return py_files

def computeComplexity(filepath):
	#need to begin and end a loop for files
    cc_filepath = open('./tmp/{}', 'r').format(filepath)
    complexity_analysis = CCHarvester(cc_filepath, cc_config) 
    cc_filepath.close()
    os.remove(file_path)

    cc_file = 0
    for cyclo in complexity_analysis:
        print (cyclo.complexity)
        cc_file += int(cyclo.complexity)
     
    print("Complexity of file: " + str(cc_file))
       
    return cc_file
    
def doWork():
    work = getWork()
    os.makedirs('tmp')
    
    payload = {'access_token': getToken()}
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    complexity = []
    for files in work:
	blob_url = files.split('<>')[0]
	filename = files.split('<>')[1]

	response = requests.get(blob_url, params=payload, headers=headers)
	with open('./tmp/{}.py'.format(filename), 'w') as tmp_file:
        	tmp_file.write(response.text)
	tmp_file.close()

	complexity.append(computeComplexity(files))
    rmtree('tmp')
    return complexity

def sendResults(complexity):
	result = {"Result: " : complexity}
	post = requests.post('http://localhost:5000/result', json=result)

def pyFile(self, filename):
        return True if match('.*\.py', filename) is not None else False

if __name__ == '__main__':
        result = doWork(work)
        sendResults(result)
