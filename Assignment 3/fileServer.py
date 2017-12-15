#!/usr/bin/python
import socketserver
import socket
import json
import os

HOST = 'localhost'
PORT = 0

Server_ID = ""
MAIN_ADDRESS = 'localhost'
MAIN_PORT = 1759

CURRENT_DIRECTORY = os.getcwd()
FOLDER_NAME = "testfiles/"
FILE_PATH = os.path.join(CURRENT_DIRECTORY, FOLDER_NAME)


def dfsOpen(filename):
    path = os.path.join(FILE_PATH, filename)
    exists = os.path.isfile(path)
    return exists

def dfsRead(filename):
    path = os.path.join(FILE_PATH, filename)
    file_handle = open(path, "r")
    data = file_handle.read()
    return data

def dfsWrite(filename, data):
    path = os.path.join(FILE_PATH, filename)
    file_handle = open(path, "a")
    file_handle.write(data)

class ThreadHandler(socketserver.BaseRequestHandler):
      def handle(self):
          req = self.request.recv(1024)
          print (req.decode('utf-8'))

          msg = json.loads(req.decode('utf-8'))
          requestType = msg['request']
          response = ""

          if requestType == "open":
             exists = dfsOpen(msg['filename'])
             response = json.dumps({"response": requestType, "filename": msg['filename'], "File": exists, "address": HOST, "port": PORT})

          elif requestType == "close":
             response = json.dumps({"response": requestType, "filename": msg['filename'], "address": HOST, "port": PORT})

          elif requestType == "read":
             data = dfsRead(msg['filename'])
             response = json.dumps({"response": requestType,"filename": msg['filename'], "address": HOST, "port": PORT, "data": data})

          elif requestType == "write":
             dfsWrite(msg['filename'], msg['data'])
             response = json.dumps({"response": requestType,"filename": msg['filename'], "address": HOST, "port": PORT})
          else:
             response = json.dumps({"response": "Error", "error": requestType+" is not a valid request", "address": HOST, "port": PORT})

          self.request.sendall(response.encode('utf-8'))

class FileServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
      pass

if __name__ == '__main__':
    address = (HOST, PORT)
    server = FileServer(address, ThreadHandler)
    PORT = server.socket.getsockname()[1]

    msg = json.dumps({"request": "new_dfs", "server": Server_ID, "address": HOST, "port": PORT})
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((MAIN_ADDRESS, MAIN_PORT))
    sock.sendall(msg.encode('utf-8'))
    response = sock.recv(1024)
    sock.close()
    print(msg)
    data = json.loads(response.decode('utf-8'))
    print(data)
    print("Server Running")
    server.serve_forever()
