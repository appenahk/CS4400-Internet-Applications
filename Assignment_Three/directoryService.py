import socketserver
import json
import uuid
import random

HOST = "localhost"#"192.168.0.1"
PORT = 8080

FILE_SERVERS = {}
FILE_DETAILS = {} #holds all details for files - id,address,port and timestamps

def fileExists(filename):
    return filename in FILE_DETAILS

def getFileDetails(filename):
    if fileExists(filename):
        return FILE_DETAILS[filename]
    else:
        return None

def addFileDetails(filename, nodeID, address, port, timestamp):
    FILE_DETAILS['filename'] = {"nodeID": nodeID, "address": address, "port": port, "timestamp": timestamp}

def deleteFileDetails(filename):
    del FILE_DETAILS[filename]

