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
	client_ip = None
	client_pair = server_socket.recvfrom(buffer_size)
	client_ip = client_pair[1]
	print("Now working with client: ",client_ip)
	if client_pair[0]:
		#Get data from DCM
		data = read_data.get_data()
		#If sensor data received
		if (type(data) is list):
			print("Sensor data received - Server")
			server_socket.sendto(str.encode("START_TM"),client_ip)
			#send number of values
			server_socket.sendto(str.encode(str(len(data))),client_ip)
			#Send telemetry values
			for d in data:
				val = str.encode(str(d))
				server_socket.sendto(val,client_ip)
			data = [0.0,0.0,0.0]
		#If system log received
		elif (type(data) is int):
			print("Syslog received - Server")
			server_socket.sendto(str.encode("SYSLOG"),client_ip)
			server_socket.sendto(str.encode(str(data)),client_ip)
		else:
			print("Unexpected message")
			continue
		#End the message
		server_socket.sendto(str.encode("END"),client_ip)
		print("End of transmission")
		print("-------------------------------------------")

