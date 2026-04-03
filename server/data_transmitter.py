import read_data #Returns an array that contains sensor data
import socket
import config

#set up
try:
	ip_add = config.get_ip_address()
	local_port = config.get_local_port()
	buffer_size = config.get_buffer_size()
	TELEMETRY_VALUES = 7
	print(f"{read_data.get_date()} - Server started. Binding to {ip_add}")
except Exception as e:
	print(f"{read_data.get_date()} - Could not load settings {e}")

#Create datagram socket
bound = False
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
while not bound:
	try:
		server_socket.bind((ip_add, local_port))
		bound = True
	except Exception as e:
		print(f"{read_data.get_date()} - Socket error: {e}")

#Send telemetry to client
while True:
	try:
		#Get client info
		client_ip = None
		client_pair = server_socket.recvfrom(buffer_size)
		client_ip = client_pair[1]

		if client_pair[0]:
			data = read_data.get_data()
			#If sensor data received
			if (type(data) is list):
				server_socket.sendto(str.encode("START_TM"),client_ip)
				#send number of values
				server_socket.sendto(str.encode(str(len(data))),client_ip)
				#Send telemetry values
				for d in data:
					val = str.encode(str(d))
					server_socket.sendto(val,client_ip)
				data = [0.0] * TELEMETRY_VALUES
			#If system log received
			elif (type(data) is int):
				server_socket.sendto(str.encode("SYSLOG"),client_ip)
				server_socket.sendto(str.encode(str(data)),client_ip)
			else:
				print(f"{read_data.get_date()} - Unexpected message")
				continue

			#End the message
			server_socket.sendto(str.encode("END"),client_ip)
	except socket.error as se:
		print(f"{read_data.get_date()} - Network error: {se}")
	except Exception as e:
		print(f"{read_data.get_date()} - Internal error: {e}")
