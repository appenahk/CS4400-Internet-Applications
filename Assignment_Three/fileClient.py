#!/usr/bin/python
import socket
import json
import uuid
import time

Main_Host = "localhost"
Main_Port = 44444


class Client():
    def __init__(self, masterHost, masterPort):
        self.id = str(uuid.uuid4())
        self.masterAddr = masterHost
        self.masterPort = masterPort

    def open(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "open", "filename": filename)
        sock.sendall(msg)
        response = sock.recv(1024)

        return response

    def close(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.masterAddr, self.masterPort))

        msg = json.dumps({"request": "close", "filename": filename)
        sock.sendall(msg)
        response = sock.recv(1024)
        return response
    

# client test
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
        elif requestType == "quit":
            response = "Exiting Distributed File System!"
        else:
            response = "Not a valid request type, please try again."
        print response
