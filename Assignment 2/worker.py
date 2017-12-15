from radon.complexity import cc_visit, cc_rank
from radon.complexity import SCORE
from radon.cli.harvest import CCHarvester
from radon.cli import Config
from shutil import rmtree
import json
import requests
import os
from re import match


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

    def getToken(self):
        with open('github-token.txt', 'r') as file_handle:
            return file_handle.read()

    def getCommit(self):
        response = requests.get('http://localhost:6790/work', params={'key': 'value'})
        print(response)
        if response.status_code == 200:
            return response.json()['commit']
        self.finished = True

    def getWork(self):
        commits = self.getCommit()

        py_files = []

        payload = {'access_token': self.getToken()}
        headers = {'Accept': 'application/vnd.github.v3.raw'}

        resp = requests.get(commits, params=payload, headers=headers)
        tree_files = resp.json()['tree']
        print(tree_files)
        for item in tree_files:
            if item['type'] == 'blob' and self.pyFile(item['path']):
                tree_url = item['url']
                filename = item['path']
                print(filename)
                file_path = tree_url + '<>' + filename
                py_files.append(file_path)

        return py_files

    def computeComplexity(self, filepath):
        # need to begin and end a loop for files
        cc_filepath = open('./tmp/{}', 'r').format(filepath)
        complexity_analysis = CCHarvester(cc_filepath, cc_config).gobble(cc_filepath)
        cc_filepath.close()
        os.remove(file_path)

        cc_file = 0
        for cyclomatic in complexity_analysis:
            cc_file += int(cyclomatic.complexity)

        print("Complexity of file: " + str(cc_file))

        return cc_file


    def doWork(self):
        while not self.finished:
            work = self.getWork()
            os.makedirs('temporary')

            payload = {'access_token': self.getToken()}
            headers = {'Accept': 'application/vnd.github.v3.raw'}
            complexity = []
            for files in work:
                blob_url = files.split('<>')[0]
                filename = files.split('<>')[1]
                flag = self.check_py(filename)
                if flag == True:
                    response = requests.get(blob_url, params=payload, headers=headers)
                    with open('./tmp/{}.py'.format(filename), 'w') as tmp_file:
                        tmp_file.write(response.text)
                    tmp_file.close()

                    complexity.append(self.computeComplexity(filename))
                rmtree('temporary')
        return complexity


    def sendResults(self, complexity):
        total_commit = 0
        for cc in complexity:
            total_commit += int(cc)
        print("Complexity of commit: " + str(total_commit))
        result = {"Result: ": complexity}
        requests.post('http://localhost:6790/result', data=result)

    def pyFile(self, filename):
        return True if match('.*\.py', filename) is not None else False


if __name__ == '__main__':
    worker = Worker()
    worker.doWork()