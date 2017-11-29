import socketserver
import socket
import json
import os

NODEID = ""
HOST = "localhost"#"192.168.0.1"
PORT = 0 # automatically assigned

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

class FileServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

