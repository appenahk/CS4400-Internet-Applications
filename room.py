#!/usr/bin/python
import select, socket, sys, pdb, threading
from thread import *

MAX_CLIENTS = 30
S_PORT = 60040
JOIN_ID_NO = 0
ROOM_REF_NO = 50000
student_ID =12308540

host = '134.226.44.146'

clients = []
room_members = {}
rooms = []
room_refs = {}
user_id = {}

connection_list = []

def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    return s

def broadcast(messg, ref):
    #messg = b'CHAT:{0}\nCLIENT_NAME:{1}\n MESSAGE: {2}\n'.format(str(ref), client, chat)	
    for user in room_members[ref]:              
	user.socket.sendall(messg)

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
   
    def remove_player(self, chatroom, player):

	if player in room_members[chatroom]:
           room_members[chatroom].remove(player)
        
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
               JOIN_ID_NO = JOIN_ID_NO+1
	       user_id[CLIENT_NAME] = JOIN_ID_NO
	    
	    join = user_id[CLIENT_NAME] 
	    if CHATROOM not in rooms:
                 		
 	         global ROOM_REF_NO
                 ROOM_REF_NO = ROOM_REF_NO+1

	         rooms.append(CHATROOM)	
		 join = user_id[CLIENT_NAME] 
                 room_members[ROOM_REF_NO] = []
		 room_members[ROOM_REF_NO].append(player)

		 room_refs[CHATROOM] = ROOM_REF_NO
                 confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT:{2}\nROOM_REF: {3}\nJOIN_ID: {4}\n'.format(CHATROOM, host, str(C_PORT), ROOM_REF_NO, join)
	       
	         player.socket.sendall(confirmation)
	                 
                 data = (str(CLIENT_NAME) + ' has joined this chatroom')
                 messag = ('CHAT: ' + str(ROOM_REF_NO) + '\nCLIENT_NAME: ' + str(CLIENT_NAME) +'\nMESSAGE: ' + data + '\n\n')     
     
		 broadcast(messag, ROOM_REF_NO)
	
	    elif CHATROOM in rooms:	         
	         refno = room_refs[CHATROOM]
	         if player in room_members[refno]:
	      		
		    CODE = "101"              	   
                    DESC = "ALREADY IN CHATROOM, SEND MESSAGES"
	            error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
	  
	            player.socket.sendall(error)
	         else:
		    confirmation = b'JOINED_CHATROOM: {0}\nSERVER_IP: {1}\nPORT: {2}\nROOM_REF: {3}\nJOIN_ID: {4}\n \n'.format(CHATROOM, host, str(C_PORT), refno, join)
	
	            player.socket.sendall(confirmation)	
	            data = (str(CLIENT_NAME) + ' has joined this chatroom')
                    messg = ('CHAT: ' + str(ROOM_REF_NO) + '\nCLIENT_NAME: ' + str(CLIENT_NAME) +'\nMESSAGE: ' + data + '\n\n') 
	            broadcast(messg, refno)

	elif "MESSAGE:" in msg:

	     REF = message[0].split(": ")[1]
	     JOIN_ID = message[1].split(": ")[1]
	     CLIENT_NAME =  message[2].split(": ")[1]           
	     CHAT = message[2].split(": ")[1]
	     #croom = room_refs[REF]
	     refno = int(REF)
	     if len(message.split(": ")) >= 2: # error check
	        if player in room_members[refno]: # switching?
		   messg = b'CHAT: {0}\nCLIENT_NAME: {1} \n MESSAGE: {2}\n\n'.format(REF, CLIENT_NAME, CHAT)	            
	           broadcast(messg, refno)
	              
	        else: # switch
	           CODE = "102"              	   
                   DESC = "NOT JOINED CHATROOM"
		   error = b'ERROR CODE: {0}\nERROR DESCRIPTION: {1}\n'.format(CODE, DESC)
		   player.socket.sendall(error)
	         		
	elif "LEAVE_CHATROOM:" in msg:

	      CHATROOM = message[0].split(": ")[1]
              JOIN_ID = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]
	      refno = int(CHATROOM)
	      
              goner = b'LEFT_CHATROOM: {0}\nJOIN_ID: {1}\n\n'.format(CHATROOM, JOIN_ID)

	      player.socket.sendall(goner)
	      
	      leave_msg = ('CHAT: ' + str(refno) + '\nCLIENT_NAME: ' + str(CLIENT_NAME) + '\nMESSAGE: ' + str(CLIENT_NAME) + ' has left this chatroom.\n\n')
	      player.socket.sendall(leave_msg)
	      broadcast(leave_msg, refno)
              self.remove_player(refno, player)

        elif "HELO" in msg:

	      confirmation = b'HELO BASE_TEST\nIP:{0}\nPORT:{1}\nStudentID:{2}\n'.format(host, S_PORT, student_ID)
	      player.socket.sendall(confirmation)

	elif "KILL_SERVICE\n" in msg:

	      exit()

	elif "DISCONNECT: " in msg:

	      IP_DISC = message[0].split(": ")[1]
              PORT = message[1].split(": ")[1]
	      CLIENT_NAME =  message[2].split(": ")[1]

	      player.socket.close()
		     

