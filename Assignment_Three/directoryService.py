#!/usr/bin/python
import SocketServer
import json
import uuid
import random

HOST = "localhost"
PORT = 44444

FILE_SERVERS = {}
FILES = {} #holds all details for files - id,address,port and timestamps

def fileExists(filename):
    return filename in FILES

def getFile(filename):
    if fileExists(filename):
        return FILES[filename]
    else:
        return None

def addFile(filename, nodeID, address, port, timestamp):
    FILES['filename'] = {"nodeID": nodeID, "address": address, "port": port, "timestamp": timestamp}

def deleteFile(filename):
    del FILES[filename]

class ThreadedHandler(SocketServer.BaseRequestHandler):

      def handle(self):
	  msg = self.request.recv(1024)
	        
	  msg = json.loads(msg)
	  requestType = msg['request']

	 
