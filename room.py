#!/usr/bin/python
import select, socket, sys, pdb, threading
from thread import *

MAX_CLIENTS = 30
S_PORT = 60040
JOIN_ID_NO = 1
ROOM_REF_NO = 200
clients = []
room_members = {}
rooms = []
room_refs = {}
join_ids = {}
socketconns = {}

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

     '''def client(self):
        while True:
            (clientSocket, client_address) = self.serverSocket.accept()   # Establish the connection
            p = threading.Thread(name=self._getClientName(client_address), target=self.client_thread, args=(clientSocket, client_address))
            p.setDaemon(True)
            p.start()

    def _getClientName(self, cli_addr):
        return "Client"'''

    def broadcast(self, player, client, ref, chat):
	msg = b'CHAT: {0}\nCLIENT_NAME: {1}\nMESSAGE: {2}\n\n'.format(ref, client, chat)
	msg_chatroom = room_refs[ref]
        if room_members[client] == msg_chatroom:
	    for player, msg_chatroom in socketconn.items():               
		player.socket.sendall(msg)

    def remove_player(self, client, chatroom):
       
	if room_members[client] == chatroom:
           del room_members[client]
        
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
	       join_ids[JOIN_ID_NO] = CLIENT_NAME

	    if CHATROOM in rooms:
	       if room_members[CLIENT_NAME] == CHATROOM:
	       #for CLIENT_NAME in room_members.values():
		 #  if CHATROOM is room_members.keys():			
		      CODE = "101"              	   
                      DESC = "ALREADY IN CHATROOM, SEND MESSAGES"
	              error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
	  
	              player.socket.sendall(error)

	    elif CHATROOM not in rooms:
                 rooms.append(CHATROOM)
		 room_members[CLIENT_NAME] = CHATROOM
		 socketconn[player] = CHATROOM
 	         global ROOM_REF_NO
                 ROOM_REF_NO+1
	         room_refs[ROOM_REF_NO] = CHATROOM
	         socketconn.append(player)
                 confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n \n'.format(CHATROOM, str(12343), C_PORT, ROOM_REF_NO, JOIN_ID_NO)
	
	         player.socket.sendall(confirmation)	       
       

	elif "MESSAGE:" in msg:

	     REF = message[0].split(": ")[1]
	     JOIN_ID = message[1].split(": ")[1]
	     CLIENT_NAME =  message[2].split(": ")[1]           
	     CHAT = message[2].split(": ")[1]

	     if len(message.split(": ")) >= 2: # error check
	        if CLIENT_NAME in room_members.keys(): # switching?	            
	           self.broadcast(player, REF, CLIENT_NAME, CHAT)
	              
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
              self.remove_player(CLIENT_NAME, CHATROOM)

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

