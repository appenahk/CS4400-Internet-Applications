#!/usr/bin/python
import SocketServer
import socket
import random
import json
import string
import os
import base64
import sqlite3 as sql

host = "localhost"
port = 19754

db = sql.connect('database.db')
cursor = db.cursor()

def encrypt(data, key):
    enc = ''
    for i in range(len(data)):
        enc += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return enc

def decrypt(data, key):
    dec = ''
    enc = data
    for i in range(len(data)):
        dec += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return dec

def getPassword(user_id):
    cursor.execute('''SELECT password FROM users WHERE id=?''', (user_id,))
    data = cursor.fetchone()
    if data is None:
        return None
    return data[0]

def getServerKey(server_id):
    cursor.execute('''SELECT key FROM servers WHERE id=?''', (server_id,))
    data = cursor.fetchone()
    if data is None:
        return None
    return data[0]

def checkUser(user_id, enc_id):
    password = getPassword(user_id)
    if password is None:
        return False
    encrypted = encrypt(user_id, password)
    return base64.b64encode(encrypted.encode()) == enc_id

def generateKey(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))

def createDatabase():
    cursor.execute('''CREATE TABLE users(id TEXT PRIMARY KEY, password TEXT, enc_id TEXT)''')
    cursor.execute('''CREATE TABLE servers(id TEXT PRIMARY KEY, key TEXT)''')
    db.commit()

class ThreadedHandler(SocketServer.BaseRequestHandler):
    def handle(self):

	msg = self.request.recv(1024)
	msg = json.loads(msg)
	user_id = msg['user_id']
        enc_id = msg['encrypted_id'].encode()
	server_id = msg['server_id']

	cursor.execute('''INSERT OR REPLACE INTO users(id, password, enc_id) VALUES(?,?,?)''',
                   (msg['user_id'], msg['password'], msg['encrypted_id']))
        cursor.execute('''INSERT OR REPLACE INTO servers(id, key) VALUES(?,?)''',
                   (msg['server_id'], msg['server_id']))
        db.commit()

        if checkUser(user_id, enc_id):
           key = getServerKey(server_id)

	   if key is None:
	      response = json.dumps( {'error': 'No server with this key exists'})
              return response

           sessKey = generateKey(16)
           encSessKey = encrypt(sessKey, key)
           encSessKey = base64.b64encode(encSessKey.encode()).decode()
           token = {'ticket': encSessKey, 'session_key': sessKey, 'server_id': server_id, 'timeout': 200 }
           encToken = base64.b64encode(encrypt(json.dumps(token), getPassword(user_id)).encode())
           response =  json.dumps({'token': encToken.decode()})

        else:
           response =  json.dumps({'error': 'User does not exist or encrpyted ID is wrong'})

        self.request.sendall(response)

class SecurityServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    createDatabase()
    address = (host, port)
    server = SecurityServer(address, ThreadedHandler)
    server.serve_forever()
