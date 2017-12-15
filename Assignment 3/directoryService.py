#!/usr/bin/python
import socketserver
import json
import uuid
from random import choice

HOST = "localhost"
PORT = 1759

FILE_SERVERS = {}
FILES = {}

def fileExists(filename):
    return filename in FILES

def getFile(filename):
    if fileExists(filename):
        return FILES[filename]
    else:
        return None

def addFile(filename, server_id, address, port, timestamp):
    FILES['filename'] = {"server": nodeID, "address": address, "port": port, "timestamp": timestamp}

def deleteFile(filename):
    del FILES[filename]

def getRandomServer():
    return choice(list(FILE_SERVERS.items()))

class ThreadedHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = self.request.recv(1024)
        msg = json.loads(msg.decode('utf-8'))

        requestType = msg['request']
        response = ""
        if requestType == "open":
            if fileExists(msg['filename']):
                openFile = getFile(msg['filename'])
                response = json.dumps({
	                    "response": "open",
	                    "filename": msg['filename'],
	                    "file": True,
	                    "address": openFile['address'],
	                    "port": openFile['port'],
	                    "timestamp": openFile['timestamp']
	                })
            else:
                randomServer = getRandomServer()
                response = json.dumps({
	                    "response": "open-null",
	                    "filename": msg['filename'],
	                    "file": False,
	                    "server": randomServer[0],
	                    "address": randomServer[1]['address'],
	                    "port": randomServer[1]['port']
	                })
        elif requestType == "close":
                if fileExists(msg['filename']):
                    closeFile = getFile(msg['filename'])
                    response = json.dumps({
                        "response": "close",
                        "filename": msg['filename'],
                        "file": True,
                        "address": closeFile['address'],
                        "port": closeFile['port'],
                        "timestamp": closeFile['timestamp']})
                else:
                    randomServer = getRandomServer()
                    response = json.dumps({
                        "response": "close-null",
                        "filename": msg['filename'],
                        "file": False,
                        "server": randomServer[0],
                        "address": randomServer[1]['address'],
                        "port": randomServer[1]['port']
	            })
        elif requestType == "read":
            if fileExists(msg['filename']):
                readFile = getFile('filename')
                response = json.dumps({
	                    "response": "read-exists",
	                    "filename": msg['filename'],
	                    "file": True,
	                    "address": readFile['address'],
	                    "port": readFile['port'],
	                    "timestamp": readFile['timestamp']
	                })
            else:
                response = json.dumps({
	                    "response": "read-null",
	                    "filename": msg['filename'],
	                    "file": False
	                })
        elif requestType == "write":
            if fileExists(msg['filename']):
                writeFile = getFile(msg['filename'])
                response = json.dumps({
	                    "response": "write-exists",
	                    "filename": msg['filename'],
	                    "file": True,
	                    "server": writeFile['server'],
	                    "address": writeFile['address'],
	                    "port": writeFile['port'],
	                    "timestamp": msg['timestamp']
	                })
            else:
                randomServer = getRandomServer()
                print("here")
                FILES[msg['filename']] = {"server": randomServer[0], "address": randomServer[1]['address'], "port": randomServer[1]['port'], "timestamp": msg['timestamp']}
                response = json.dumps({
	                    "response": "write-null",
	                    "filename": msg['filename'],
	                    "file": False,
	                    "server": randomServer[0],
	                    "address": randomServer[1]['address'],
	                    "port": randomServer[1]['port'],
	                    "timestamp": msg['timestamp']
	                })
        elif requestType == "new_dfs":
            serverID = msg['server']
            if(serverID == ""):
                serverID = str(uuid.uuid4())
                FILE_SERVERS[serverID] = {"address": msg['address'], "port": msg['port']}
                response = json.dumps({"response": requestType, "server": serverID})
                print (FILE_SERVERS)
            else:
                response = json.dumps({"response": "error", "error": requestType+" is not a valid request"})
        self.request.sendall(response.encode('utf-8'))

class DirectoryServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    address = (HOST, PORT)
    server = DirectoryServer(address, ThreadedHandler)
    print("Directory Server Running")
    server.serve_forever()
