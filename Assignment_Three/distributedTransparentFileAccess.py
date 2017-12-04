#!/usr/bin/python
import SocketServer
import socket
import json
import os

NODEID = ""
HOST = "localhost"
PORT = 0

MAIN_ADDRESS = "localhost"#"127.0.0.1"
MAIN_PORT = 44444

CURRENT_DIRECTORY = os.getcwd()
FOLDER_NAME = "testfiles"              #directory to store files
FILE_PATH = os.path.join(CURRENT_DIRECTORY, FOLDER_NAME)


def dfsOpen(filename):
    path = os.path.join(FILE_PATH, filename)
    exists = os.path.isfile(path)
    return exists

def dfsClose(filename):
    path = os.path.join(FILE_PATH, filename)

def dfsRead(filename):
    path = os.path.join(FILE_PATH, filename)
    file_handle = open(path, "r")
    data = file_handle.read()
    return data

def dfsWrite(filename, data):
    path = os.path.join(FILE_PATH, filename)
    file_handle = open(path, "a")
    file_handle.write(data)

class ThreadHandler(SocketServer.BaseRequestHandler):
      def handle(self):
          req = self.request.recv(1024)
          print req

          msg = json.loads(req)
          requestType = msg['request']
          response = ""

          if requestType == "open":
             exists = dfsOpen(msg['filename'])
             response = json.dumps({"response": requestType, "filename": msg['filename'], "File": exists, "address": HOST, "port": PORT})

          elif requestType == "close":
               response = json.dumps({"response": requestType, "filename": msg['filename'], "address": HOST, "port": PORT})

          elif requestType == "read":
               data = dfsRead(msg['filename'])
               response = json.dumps({"response": requestType,"filename": msg['filename'], "data": data}, "address": HOST, "port": PORT})

          elif requestType == "write":
               dfsWrite(msg['filename'], msg['data'])
               response = json.dumps({"response": requestType,"filename": msg['filename'], "address": HOST, "port": PORT})

       	  else:
               response = json.dumps({"response": "Error", "error": requestType+" is not a valid request", "address": HOST, "port": PORT})

          self.request.sendall(response)

class FileServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
      pass

if __name__ == '__main__':
	address = (HOST, PORT)
	server = FileServer(address, ThreadHandler)
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((MAIN_ADDRESS, MAIN_PORT))
	response = sock.recv(1024)
	sock.close()
	
	server.serve_forever()
