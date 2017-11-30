import socketserver
import socket
import json
import os

NODEID = ""
HOST = "localhost"
PORT = 0

MASTER_ADDRESS = "localhost"#"127.0.0.1"
MASTER_PORT = 8080

CURRENT_DIRECTORY = os.getcwd()
FOLDER_NAME = "testfiles"              #directory to store files
FILE_PATH = os.path.join(CURRENT_DIRECTORY, BUCKET_NAME)


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
    file_handle = open(path, "w+")
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
             response = json.dumps({"response": requestType, "filename": msg['filename'], "isFile": exists)
          elif requestType == "close":
               response = json.dumps({"response": requestType, "filename": msg['filename'])
          elif requestType == "read":
               data = dfsRead(msg['filename'])
               response = json.dumps({"response": requestType,"filename": msg['filename'], "data": data})
          elif requestType == "write":
               dfsWrite(msg['filename'], msg['data'])
               response = json.dumps({"response": requestType,"filename": msg['filename'], "uuid": NODEID})
       	  else:
               response = json.dumps({"response": "Error", "error": requestType+" is not a valid request")

          self.request.sendall(response)
class FileServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

