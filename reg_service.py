import socket
PORT = 9090

ip_list = []

sock = socket.socket() #create socket
sock.bind(('', PORT)) # '' means it can be reached from localhost and anwhere else, 9090 - port
for i in range(4):
	sock.listen(1) #1 client at a time
	conn, addr = sock.accept() #new socket and addres of the client

	print "CONNECTED TO ", addr

	#get data
	ip_list.append(addr)

	ip_send = ip_list

	ip_send = str(ip_send)
	ip_send = ip_send.encode()
	conn.sendall(ip_send) #send list of IPs

sock.close()
