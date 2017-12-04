#!/usr/bin/python
import SocketServer
import json
import uuid
import random

HOST = "localhost"
PORT = 1759

FILES = {}

def fileExists(filename):
    return filename in FILES

def getFile(filename):
    if fileExists(filename):
        return FILES[filename]
    else:
        return None

class ThreadedHandler(SocketServer.BaseRequestHandler):

      def handle(self):
	  msg = self.request.recv(1024)
	        
	  msg = json.loads(msg)
	  requestType = msg['request']
	  if requestType == "open":
	     if fileExists(msg['filename']):
          	openFile = getFile(msg['filename'])
                response = json.dumps({
                            "response": "open",
	                    "filename": msg['filename'],
	                    "File": True,
 			    "address": openFile['address'],
	                    "port": openFile['port']})
	     else:
	        response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "isFile": False})

          elif requestType == "close":
               if fileExists(msg['filename']):
                  response = json.dumps({
	                    "response": "close",
	                    "filename": msg['filename'],
	                    "File": True,
			    "address": openFile['address'],
	                    "port": openFile['port']})
               else:
	          response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "File": False})

	  elif requestType == "read":
	       if fileExists(msg['filename']):
	                readFile = getFile('filename')
	                response = json.dumps({
	                    "response": "read",
	                    "filename": msg['filename'],
	                    "File": True,
			    "address": readFile['address'],
	                    "port": readFile['port']})
               else:
	                response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "File": False
	                })

	  elif requestType == "write":
	       if fileExists(msg['filename']):
	                writeFile = getFile(msg['filename'])
	                response = json.dumps({
	                    "response": "write",
	                    "filename": msg['filename'],
	                    "File": True,
			    "address": writeFile['address'],
	                    "port": writeFile['port']})
	       else:               
	                response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "File": False})
	  self.request.sendall(response)

class DirectoryServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    address = (HOST, PORT)
    server = MasterServer(address, ThreadedHandler)
    server.serve_forever()
