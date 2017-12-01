#!/usr/bin/python
import socket
import json
import uuid
import time

Main_Host = "localhost"
Main_Port = 44444


class Client():
    def __init__(self, mainHost, mainPort):
        #self.id = str(uuid.uuid4())
        self.mainAddr = mainHost
        self.mainPort = mainPort
	self.lockAddr = lockHost
        self.lockPort = lockPort
	self.cache = {}

    def open(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.mainAddr, self.mainPort)

        msg = json.dumps({"request": "open", "filename": filename)
        sock.sendall(msg)
        response = sock.recv(1024)
        return response

    def close(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.mainAddr, self.mainPort)

        msg = json.dumps({"request": "close", "filename": filename)
        sock.sendall(msg)
        response = sock.recv(1024)
        return response

    def read(self, filename):
        fileCheck = json.loads(self.open(filename))
	if fileCheck['isFile']:
	   if (filename in self.cache)
	       cacheFile = self.cache[filename]
	       print "Read from cache: " +filename
	   else:
	       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               sock.connect(self.mainAddr, self.mainPort)
	       msg = json.dumps({"request": "read", "filename": filename})
               sock.sendall(msg)

               response = sock.recv(1024)
	       self.cache['filename'] = json.loads(response)
	else:
           return filename + " no exist"

     def write(self, filename, data):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.mainAddr, self.mainPort)

        #timestamp = time.time()

        msg = json.dumps({"request": "write", "filename": filename})
        sock.sendall(msg)
        response = sock.recv(1024)

        fileCheck = json.loads(response)

        addr = fileServerInfo['address']
        port = int(fileServerInfo['port'])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))

        content = {"request": "write", "filename": filename, "data": data}

        self.cache[filename] = content

        msg = json.dumps(content)
        sock.sendall(msg)

        response = sock.recv(1024)
        return response

if __name__ == '__main__':
    client = Client(Main_Host, Main_Port)

    requestType = ""
    response = ""

    while requestType != "quit":
        requestType = raw_input("Please enter a request type eg: open - close - checklock - obtainlock - read - write or type quit to terminate the program: ")

        if requestType == "open":
            filename = raw_input("Please enter the filename: ")
            response = client.open(filename)
        elif requestType == "close":
            filename = raw_input("Please enter the filename: ")
            response = client.close(filename)
	elif requestType == "read":
            filename = raw_input("Please enter the filename: ")
            response = client.read(filename)
        elif requestType == "write":
            filename = raw_input("Please enter the filename: ")
            data = raw_input("Please enter the file contents to write: ")
            response = client.write(filename, data)    
        elif requestType == "quit":
            response = "Exiting Distributed File System!"
        else:
            response = "Not a valid request type, please try again."
        print response
