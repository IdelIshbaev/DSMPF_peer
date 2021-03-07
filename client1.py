import socket
import sys
import time 
HOST = '10.0.0.11'
PORT = 9090
NUMBER_OF_PLAYERS = 4

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.connect((HOST, PORT))
ip_queue = sock.recv(1024)

sock.close()

ip_queue.decode('utf-8')
ip_queue = eval(ip_queue)
print ip_queue
my_port = ip_queue[len(ip_queue)-1][1]
my_order = len(ip_queue)
# hellow to other clients
for i in range(len(ip_queue)-1):
	print 'TRY TO CONNECT', ip_queue[i][0], ip_queue[i][1]

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip_queue[i][0], ip_queue[i][1]))
	addr = ip_queue[len(ip_queue)-1]
	addr = str(addr)
	addr = addr.encode()
	sock.sendall(addr)
	print 'CONNECTED', ip_queue[i][0], ip_queue[i][1]
	sock.close()

#listen
i = len(ip_queue)
while i >= 1 and i < NUMBER_OF_PLAYERS:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	sock.bind(('', my_port))
	sock.listen(1)
	
	conn, addr = sock.accept()
	new_addr = conn.recv(1024)
	new_addr.decode('utf-8')
	new_addr = eval(new_addr)
	ip_queue.append(new_addr)

	print 'RECIEVED CONNECTION FROM', addr
	print ip_queue
	sock.close()
	i += 1

print 'FINAL LIST OF PLAYERS: \n'
count = 1
for i in ip_queue:
	if count == my_order:
		print count, '. ', i, ' MY TURN'
	else:
		print count, '. ', i
	count += 1


