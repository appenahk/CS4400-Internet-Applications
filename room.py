#!/usr/bin/python
import select, socket, sys, pdb
from thread import *
#from pychat_util import Room, Player
#import pychat_util

MAX_CLIENTS = 30
S_PORT = 60040
JOIN_ID_NO = 100
ROOM_REF_NO = 200
clients = []
room_members = {}
rooms = []
room_refs = {}
join_ids = {}

def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    return s

class Room:

    def __init__(self):
        self.clients = []
        self.rooms = []
	self.room_refs = {}
	self.join_ids = {}
	self.room_members = {}
    
    def broadcast(self,CHATROOM, CLIENT_NAME, CHAT):
	msg = b'CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}\n\n'.format(CHATROOM, CLIENT_NAME, CHAT)
        for client in room_members:
            client.socket.sendall(msg)

    def remove_player(self, client):
        self.clients.remove(client)
        
    def client_thread(self, player, msg):
		
	message = msg.split('\n')
	if "JOIN_CHATROOM:" in msg:
	    CHATROOM = message[0].split(": ")[1]
	    CLIENT_IP = message[1].split(": ")[1]
	    C_PORT = message[2].split(": ")[1]
	    CLIENT_NAME =  message[3].split(": ")[1]
	    
	    room_members[CHATROOM] = CLIENT_NAME

	    if CLIENT_NAME not in clients:
               clients.append(CLIENT_NAME)
	       global JOIN_ID_NO
               JOIN_ID_NO+1
	       join_ids[CLIENT_NAME] = JOIN_ID_NO

	    if CHATROOM in rooms 
		 for CLIENT_NAME in room_members.values() 
		     if CHATROOM in room_members.keys()

	    elif CHATROOM not in rooms:
               rooms.append(CHATROOM)
 	       global ROOM_REF_NO
               ROOM_REF_NO+1
	       room_refs[CHATROOM] = ROOM_REF_NO
	       
               confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n \n'.format(CHATROOM, str(12343), C_PORT, ROOM_REF_NO, JOIN_ID_NO)
	
	       player.socket.sendall(confirmation)	       
            else:
               CODE = "101"              	   
               DESC = "ALREADY IN CHATROOM, SEND MESSAGES"
	       error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
	  
	       player.socket.sendall(error)          

	elif "MESSAGE:" in msg:

	     CHATROOM = message[0].split(": ")[1]
	     JOIN_ID = message[1].split(": ")[1]
	     CLIENT_NAME =  message[2].split(": ")[1]           
	     CHAT = message[2].split(": ")[1]

	     if len(message.split(": ")) >= 2: # error check
	        if CLIENT_NAME in room_members: # switching?	            
	           self.broadcast(CHATROOM, CLIENT_NAME, CHAT)
	              
	        else: # switch
	           CODE = "102"              	   
                   DESC = "NOT JOINED CHATROOM"
		   error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
	         		
	elif "LEAVE_CHATROOM:" in msg:

	      CHATROOM = message[0].split(": ")[1]
              JOIN_ID = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]

              goner = b'LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n\n'.format(CHATROOM, JOIN_ID)

	      player.socket.sendall(goner)
              self.remove_player(CLIENT_NAME)

        elif "HELO text\n" in msg:

	      confirmation = b'HELO text\nIP:{0}\nPORT: {1}\nStudentID:{2}\n'.format(host, str(S_PORT), str(student_ID))
	      player.socket.sendall(confirmation)

	elif "KILL_SERVICE\n" in msg:

	      exit()

	elif "DISCONNECT: " in msg:

	      IP_DISC = message[0].split(": ")[1]
              PORT = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]

	      player.socket.close()
		     
class Client:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

