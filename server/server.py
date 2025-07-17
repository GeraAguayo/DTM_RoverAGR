import read_data #Returns an array that contains [Temperature, Pressure, Altitude]
import socket
import config

#set up
ip_add = config.IP_ADDR
local_port = config.LOCAL_PORT
buffer_size = config.BUFFER_SIZE

#Create datagram socket
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.bind((ip_add, local_port))
print("The server is up and working!")

#Send telemetry to client
while True:
	#Get client info
	client_pair = server_socket.recvfrom(buffer_size)
	client_ip = client_pair[1]
	print("Now working with client: ",client_ip)
	#Start the message
	server_socket.sendto(str.encode("START_TM"),client_ip)

	#Set the num of values for the client to receive
	data = read_data.get_data()
	server_socket.sendto(str.encode(str(len(data))),client_ip)

	#Send telemetry values
	for d in data:
		val = str.encode(str(d))
		server_socket.sendto(val,client_ip)
	data = [0.0,0.0,0.0]

	#End the message
	server_socket.sendto(str.encode("END_TM"),client_ip)

