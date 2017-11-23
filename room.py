#!/usr/bin/python
import select, socket, sys, pdb, threading
from thread import *

MAX_CLIENTS = 30
S_PORT = 60040
JOIN_ID_NO = 1
ROOM_REF_NO = 200
student_ID =12308540

host = '134.226.44.154'

clients = []
room_members = {}
rooms = []
room_refs = {}
user_id = {}
socketconns = {}
users = []
connection_list = []

def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    return s

class Client():
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
    def fileno(self):
        return self.socket.fileno()

class Room:
	
    def __init__(self):
        self.clients = []
        self.rooms = []
	self.room_refs = {}
	self.user_ids = {}
	self.room_members = {}

    

   
    def remove_player(self, chatroom, joinid):
	#join = user_ids[client] 
	#room_members[join] = CHATROOM
        #room_members[chatroom].users
	if joinid in room_members[chatroom].users:
           room_members[chatroom].users.remove(joinid)
        
    def client_thread(self, player, msg):
		
	message = msg.split('\n')
	if "JOIN_CHATROOM:" in msg:
	    CHATROOM = message[0].split(": ")[1]
	    CLIENT_IP = message[1].split(": ")[1]
	    C_PORT = message[2].split(": ")[1]
	    CLIENT_NAME =  message[3].split(": ")[1]

	    if CLIENT_NAME not in clients:
               clients.append(CLIENT_NAME)
	       global JOIN_ID_NO
               JOIN_ID_NO+1
	       user_id[CLIENT_NAME] = JOIN_ID_NO

	    if CHATROOM in rooms:
	     
	       if CLIENT_NAME in self.room_members[CHATROOM].users:
	      		
		  CODE = "101"              	   
                  DESC = "ALREADY IN CHATROOM, SEND MESSAGES"
	          error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
	  
	          player.socket.sendall(error)
	    if CHATROOM in rooms:
	       refno = room_refs[CHATROOM]
	       if CLIENT_NAME not in self.room_members[CHATROOM].users:
		  confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n \n'.format(CHATROOM, host, C_PORT, refno, JOIN_ID_NO)
	
	          player.socket.sendall(confirmation)	
	          data = b'CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2} HAS JOINED_CHATROOM\n\n'.format(ROOM_REF_NO, CLIENT_NAME, chat)
	          room_members[CHATROOM].users.socket.sendall(data) 
	    
	    elif CHATROOM not in rooms:
                 rooms.append(CHATROOM)	
		 join = user_id[CLIENT_NAME] 
                 room_members[join] = CHATROOM
		 #socketconn[player] = CHATROOM
 	         global ROOM_REF_NO
                 ROOM_REF_NO+1
	         self.room_refs[CHATROOM] = ROOM_REF_NO
	         #socketconn.append(player)'''

                 confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n \n'.format(CHATROOM, host, C_PORT, ROOM_REF_NO, JOIN_ID_NO)
	
	         player.socket.sendall(confirmation)
		 
       		 data = '{2} HAS JOINED_CHATROOM'.format(ROOM_REF_NO, CLIENT_NAME, CLIENT_NAME)
	         broadcast(ROOM_REF_NO, CLIENT_NAME, CLIENT_NAME)

	elif "MESSAGE:" in msg:

	     REF = message[0].split(": ")[1]
	     JOIN_ID = message[1].split(": ")[1]
	     CLIENT_NAME =  message[2].split(": ")[1]           
	     CHAT = message[2].split(": ")[1]
	     croom = room_refs[REF]

	     if len(message.split(": ")) >= 2: # error check
	        if CLIENT_NAME in self.room_members[msg_chatroom].users: # switching?	            
	           self.broadcast(player, REF, CLIENT_NAME, CHAT)
	              
	        else: # switch
	           CODE = "102"              	   
                   DESC = "NOT JOINED CHATROOM"
		   error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
		   player.socket.sendall(error)
	         		
	elif "LEAVE_CHATROOM:" in msg:

	      CHATROOM = message[0].split(": ")[1]
              JOIN_ID = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]

              goner = b'LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n\n'.format(CHATROOM, JOIN_ID)

	      player.socket.sendall(goner)
              self.remove_player(CHATROOM, JOIN_ID)

        elif "HELO" in msg:

	      confirmation = b'HELO text\nIP:{0}\nPORT: {1}\nStudentID:{2}\n'.format(host, str(S_PORT), str(student_ID))
	      player.socket.sendall(confirmation)

	elif "KILL_SERVICE\n" in msg:

	      exit()

	elif "DISCONNECT: " in msg:

	      IP_DISC = message[0].split(": ")[1]
              PORT = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]

	      player.socket.close()
		     
def broadcast(self, ref, client, chat):
	 msg = b'CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}\n\n'.format(ref, client, chat)
	 msg_chatroom = room_refs[ref]
		
	 for user in room_members[msg_chatroom].users:               
	     user.socket.sendall(msg)

