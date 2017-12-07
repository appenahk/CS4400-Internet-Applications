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
def addFile(filename, address, port, timestamp):
    FILES[filename] = {"address": address, "port": port, "timestamp": timestamp}

def deleteFile(filename):
    del FILES[filename]

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
	                    "file": True,
 			    "address": openFile['address'],
	                    "port": openFile['port'],
			    "timestamp": openFile['timestamp']})
	     else:
	        response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "file": False})

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
	          response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "file": False})

	  elif requestType == "read":
	       if fileExists(msg['filename']):
	          readFile = getFile('filename')
	          response = json.dumps({
	              "response": "read",
	               "filename": msg['filename'],
	              "file": True,
	 	      "address": readFile['address'],
	              "port": readFile['port'],
		      "timestamp": readFile['timestamp']})
               else:
	          response = json.dumps({
	              "response": "file no exist",
	              "filename": msg['filename'],
	              "file": False})

	  elif requestType == "write":
	       if fileExists(msg['filename']):
	          writeFile = getFile(msg['filename'])
		  if writeFile['timestamp'] < msg['timestamp']:
		     deleteFile(writeFile['filename'])
		     addFile(msg['filename'], msg['address'], msg['port'], msg['timestamp'])
	          response = json.dumps({
	              "response": "write",
	              "filename": msg['filename'],
	              "file": True,
            	      "address": msg['address'],
	              "port": msg['port'],
	              "timestamp": msg['timestamp']})
	       else:               
	                response = json.dumps({
	                    "response": "file no exist",
	                    "filename": msg['filename'],
	                    "file": False})
	  self.request.sendall(response)

class DirectoryServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    address = (HOST, PORT)
    server = MasterServer(address, ThreadedHandler)
    server.serve_forever()
