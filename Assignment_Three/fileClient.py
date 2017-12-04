#!/usr/bin/python
import socket
import json
import uuid
import time
import securityService

Main_Host = "localhost"
Main_Port = 44444
Lock_Host = "localhost"
Lock_Port = 8883
Auth_Host = "localhost"
Auth_Port = 19754


class Client():
    def __init__(self, mainHost, mainPort, lockHost, lockPort, authHost, authPort):
        self.mainAddr = mainHost
        self.mainPort = mainPort
	self.lockAddr = lockHost
        self.lockPort = lockPort
	self.authAddr = authHost
        self.authPort = authPort
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

         timestamp = time.time()

         msg = json.dumps({"request": "write", "filename": filename})
         sock.sendall(msg)
         response = sock.recv(1024)

         fileCheck = json.loads(response)

         addr = fileCheck['address']
         port = int(fileCheck['port'])

         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect((addr, port))

         edit = {"request": "write", "filename": filename, "data": data}

         self.cache[filename] = edit

         msg = json.dumps(edit)
         sock.sendall(msg)

         response = sock.recv(1024)
         return response

     def checkLock()
	 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect((self.lockAddr, self.lockPort))

	 msg = json.dumps({"request": "checklock", "filename": filename, "clientid": self.id})
         sock.sendall(msg)
         response = sock.recv(1024)

     def getLock()
	 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect((self.lockAddr, self.lockPort))

	 msg = json.dumps({"request": "obtainlock", "filename": filename, "clientid": self.id})
         sock.sendall(msg)
         response = sock.recv(1024)

     def authentication(self, username, password):
	 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect(self.authAddr, self.authPort)

	 encId = base64.b64encode(securityService.encrypt(userId, userPassword).encode()).decode()
         authorisationCheck = {'user_id': userId, 'password': userPassword, 'encrypted_id': encId, 'server_id': 'File Server 1'}

	 msg = json.dumps(authorisationCheck)
         sock.sendall(msg)  

	 response = sock.recv(1024)
         return response

if __name__ == '__main__':
    client = Client(Main_Host, Main_Port, Lock_Host, Lock_Port, Auth_Host, Auth_Port)

    requestType = ""
    response = ""

    userId = raw_input("Please Enter Username: ")
    userPassword = raw_input("Please Enter Password: ")
    response = client.authentication(userId, userPassword)
    print response

    while requestType != "quit":
        requestType = raw_input("Please enter a request type eg: open - close - read - write - checklock - getlock or type quit to terminate the program: ")

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
	elif requestType == "checklock":
            filename = raw_input("Please enter the filename: ")
            response = client.checkLock(filename)
        elif requestType == "getlock":
            filename = raw_input("Please enter the filename: ")
            response = client.obtainLock(filename)
        elif requestType == "quit":
            response = "Exiting Distributed File System!"
        else:
            response = "Not a valid request type, please try again."
        print response
