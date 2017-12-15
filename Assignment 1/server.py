import select, socket, sys, pdb
from room import Room, Client
import room

READ_BUFFER = 4096
host = '127.0.0.1'
#host = sys.argv[1]
listen_sock = room.create_socket((host, room.S_PORT))

hall = Room()
connection_list = []
connection_list.append(listen_sock)

while True:
	try:
		read_players, _, _ = select.select(connection_list,[],[])

		for player in read_players:
			if player is listen_sock: # new connection, player is a socket
				new_socket, address = player.accept()
				new_player = Client(new_socket)
				connection_list.append(new_player)
		    
			else: # new message
				msg = player.socket.recv(READ_BUFFER)
				if msg:
					msg = msg.decode()
					hall.client_thread(player, msg)
	except select.error:
		break
