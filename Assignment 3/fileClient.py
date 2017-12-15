#!/usr/bin/python
import socket
import json
import uuid
import time
import securityService
import base64

Main_Host = 'localhost'
Main_Port = 1759
Lock_Host = 'localhost'
Lock_Port = 8883
Auth_Host = 'localhost'
Auth_Port = 19754


class Client():
    def __init__(self, mainHost, mainPort, lockHost, lockPort, authHost, authPort):
        self.id = str(uuid.uuid4())
        self.mainAddr = mainHost
        self.mainPort = mainPort
        self.lockAddr = lockHost
        self.lockPort = lockPort
        self.authAddr = authHost
        self.authPort = authPort
        self.cache = {}

    def open(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.mainAddr, self.mainPort))

        msg = json.dumps({"request": "open", "filename": filename, "clientid": self.id})
        sock.sendall(msg.encode('utf-8'))
        response = sock.recv(1024)
        return response

    def close(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.mainAddr, self.mainPort))

        msg = json.dumps({"request": "close", "filename": filename, "clientid": self.id})
        sock.sendall(msg.encode('utf-8'))
        response = sock.recv(1024)
        return response

    def read(self, filename):

        fileCheck = json.loads(self.open(filename))
        if fileCheck['file']:
            if (filename in self.cache):
                cacheFile = self.cache[filename]
                print ("Read from cache: " +filename)
                return cacheFile["data"]
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.mainAddr, self.mainPort))
                msg = json.dumps({"request": "read", "filename": filename, "clientid": self.id})
                sock.sendall(msg.encode('utf-8'))

                response = sock.recv(1024)
                self.cache['filename'] = json.loads(response.decode("utf-8"))
                return response
        else:
           return filename + " no exist"

    def write(self, filename, data):
        lockcheck = json.loads(client.checkLock(filename))

        if lockcheck['response'] == "locked":
            print("Cannot write as file is locked by another client!")
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.mainAddr, self.mainPort))

        timestamp = time.time()

        msg = json.dumps({"request": "write", "filename": filename, "timestamp": timestamp, "clientid": self.id})

        sock.sendall(msg.encode('utf-8'))
        print(msg)
        response = sock.recv(1024)

        fileCheck = json.loads(response.decode("utf-8"))

        addr = fileCheck['address']
        port = int(fileCheck['port'])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))

        edit = {"request": "write", "filename": filename, "data": data, "timestamp": timestamp, "clientid": self.id}

        self.cache[filename] = edit

        msg = json.dumps(edit)
        sock.sendall(msg.encode('utf-8'))
        #print(msg)
        response = sock.recv(1024)
        return response.decode('utf-8')

    def checkLock(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lockAddr, self.lockPort))

        msg = json.dumps({"request": "checklock", "filename": filename, "clientid": self.id})
        sock.sendall(msg.encode('utf-8'))
        response = sock.recv(1024)
        return response

    def getLock(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.lockAddr, self.lockPort))

        msg = json.dumps({"request": "getlock", "filename": filename, "clientid": self.id})
        sock.sendall(msg.encode('utf-8'))
        response = sock.recv(1024)
        return response

    def authentication(self, username, password):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.authAddr, self.authPort))

        encId = base64.b64encode(securityService.encrypt(username, password).encode()).decode()
        #authorisationCheck = {'user_id': username, 'password': password, 'encrypted_id': encId, 'server_id': 'File Server 1'}

        msg = json.dumps({'user_id': username, 'password': password, 'encrypted_id': encId, 'server_id': 'File Server 1'})
        sock.sendall(msg.encode('utf-8'))

        response = sock.recv(1024)
        return response

if __name__ == '__main__':
    client = Client(Main_Host, Main_Port, Lock_Host, Lock_Port, Auth_Host, Auth_Port)

    requestType = ""
    response = ""

    userId = input("Please Enter Username: ")
    userPassword = input("Please Enter Password: ")
    response = client.authentication(userId, userPassword)

    while requestType != "quit":
        requestType = input("Please enter a request type eg: open - close - read - write - checklock - getlock or type quit to terminate the program: ")

        if requestType == "open":
            filename = input("Please enter the filename: ")
            response = client.open(filename)
        elif requestType == "close":
            filename = input("Please enter the filename: ")
            response = client.close(filename)
        elif requestType == "read":
            filename = input("Please enter the filename: ")
            response = client.read(filename)
        elif requestType == "write":
            filename = input("Please enter the filename: ")
            data = input("Please enter the file contents to write: ")
            response = client.write(filename, data)
        elif requestType == "checklock":
            filename = input("Please enter the filename: ")
            response = client.checkLock(filename)
        elif requestType == "getlock":
            filename = input("Please enter the filename: ")
            response = client.obtainLock(filename)
        elif requestType == "quit":
            response = "Exiting Distributed File System!"
        else:
            response = "Not a valid request type, please try again."
        print(response)
