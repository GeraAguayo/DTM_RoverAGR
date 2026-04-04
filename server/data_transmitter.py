import read_data #Returns an array that contains sensor data
import datetime_manager
import socket
import config

def create_socket():
	try:
		ip_add = config.get_ip_address()
		local_port = config.get_local_port()
		server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((ip_add, local_port))
		print(f"{datetime_manager.get_datetime()} - Socket started. Binding to {ip_add}")
		return server_socket
	except Exception as e:
		print(f"{datetime_manager.get_datetime()} - Could not create socket: {e}")
		return None

def raise_system_log(log_id, server_socket):
	client_pair = server_socket.recvfrom(config.get_buffer_size())
	server_socket.sendto(str.encode("SYSLOG"), client_pair[1])
	server_socket.sendto(str.encode(str(log_id)), client_pair[1])
	server_socket.sendto(str.encode("END"), client_pair[1])

def send_data_array(data_array, server_socket):
	client_pair = server_socket.recvfrom(config.get_buffer_size())
	server_socket.sendto(str.encode("START_TM"), client_pair[1])
	#send the number of values
	server_socket.sendto(str.encode(str(len(data_array))), client_pair[1])
	#send telemetry values
	for d in data_array:
		val = str.encode(str(d))
		server_socket.sendto(val, client_pair[1])
	server_socket.sendto(str.encode("END"), client_pair[1])

#main if executed as a single script
if __name__ == '__main__':
	SERVER_SOCKET = None

	while SERVER_SOCKET is None:
		SERVER_SOCKET = create_socket()

	while True:
		sensor_data = read_data.get_data()
		if isinstance(sensor_data, list):
			#sensor values
			send_data_array(sensor_data, SERVER_SOCKET)
		elif isinstance(sensor_data, int):
			#syslog
			raise_system_log(sensor_data, SERVER_SOCKET)
		else:
			print(f"{datetime_manager.get_date()} - Unexpected data received from DCM")
		sensor_data = None
