from radon.complexity import cc_visit, cc_rank
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
import json
import requests
import os
from re import match

complexity = 0
class Worker:

    cc_config = Config(
        exclude='',
        ignore='venv',
        order=SCORE,
        no_assert=True,
        show_closures=False,
        min='A',
        max='F',
    )

    def __init__(self):
        self.finished = False

    #token required for github authentication
    def getToken(self):
        with open('github-token.txt', 'r') as file_handle:
            return file_handle.read()


    #get the commits usinng http GET
    def getCommit(self):
        response = requests.get('http://localhost:6790/work', params={'key': 'value'})
        if response.status_code == 200:
            return response.json()['commit']
        self.finished = True

    #parse the commits to get the python files
    def getWork(self):
        commits = self.getCommit()

        py_files = []

        payload = {'access_token': self.getToken()}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        resp = requests.get(commits, params=payload, headers=headers)
        tree_files = resp.json()['tree']
        for item in tree_files:
            if item['type'] == 'blob' and self.pyFile(item['path']):
                tree_url = item['url']
                filename = item['path']

                file_path = tree_url + '///' + filename
                py_files.append(file_path)
        return py_files

    #compute complexity of each file in the list
    def computeComplexity(self, filepath):

        cc_filepath = open(filepath, 'r')
        complexity_analysis = CCHarvester(filepath, self.cc_config).gobble(cc_filepath)
        cc_filepath.close()
        os.remove(filepath)

        cc_file = 0
        for cyclomatic in complexity_analysis:
            cc_file += int(cyclomatic.complexity)

        print("Complexity of file: " + str(cc_file))
        return int(cc_file)

    #perform work on the commit
    def doWork(self):
        while not self.finished:
            work = self.getWork()
            for elem in work:
                print(elem)

            payload = {'access_token': self.getToken()}
            headers = {'Accept': 'application/vnd.github.v3.raw'}
            global complexity
            for files in work:
                blob_url = files.split('///')[0]
                filename = files.split('///')[1]
                flag = self.pyFile(filename)
                num = 0

                if flag == True:
                        response = requests.get(blob_url, params=payload, headers=headers)
                        file_path = num = 1
                        name = os.path.basename(__file__)
                        name = name.split('.')[0]
                        file_path = name + str(file_path) + '.py'

                        with open(file_path, 'w') as tmp_file:
                            tmp_file.write(response.text)
                        tmp_file.close()

                        complexity += self.computeComplexity(file_path)
                        print(complexity)
            return complexity


    #send results back to manager
    def sendResults(self):
        response = requests.get('http://localhost:6790/work').json()
        while response != "done":
            cc_result = self.doWork()
            response = requests.get('http://localhost:6790/work').json()
        print("Complexity of commit: " + str(cc_result))
        result = {"Result: ": cc_result}
        if requests.post('http://localhost:6790/result', json=result)

    #check if python file as radon is for python cc
    def pyFile(self, filename):
        return True if match('.*\.py', filename) is not None else False


if __name__ == '__main__':
    worker = Worker()
    worker.sendResults()