import read_data
import datetime_manager
import socket
import config
import time

SERVER_SOCKET = None	#For external comms with telemetry center
RELAY_SOCKET = None	#For internal comms with other modules

def setup_relay():
	global RELAY_SOCKET
	try:
		RELAY_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		RELAY_SOCKET.bind(('127.0.0.1', 5005))
		RELAY_SOCKET.setblocking(False)
	except Exception as e:
		print(f"{datetime_manager.get_datetime()} - Failed to create relay socket: {e}")

def check_local_logs():
	try:
		data, addr = RELAY_SOCKET.recvfrom(1024)
		log_id = data.decode()
		raise_system_log(log_id)
	except Exception:
		pass

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

def raise_system_log(log_id):
	destination = (config.get_base_station_add(), config.get_local_port())
	SERVER_SOCKET.sendto(str.encode("SYSLOG"), destination)
	SERVER_SOCKET.sendto(str.encode(str(log_id)), destination)
	SERVER_SOCKET.sendto(str.encode("END"), destination)

def send_data_array(data_array):
	destination = (config.get_base_station_add(), config.get_local_port())
	SERVER_SOCKET.sendto(str.encode("START_TM"), destination)
	#send the number of values
	SERVER_SOCKET.sendto(str.encode(str(len(data_array))), destination)
	#send telemetry values
	for d in data_array:
		val = str.encode(str(d))
		SERVER_SOCKET.sendto(val, destination)
	SERVER_SOCKET.sendto(str.encode("END"), destination)

#main if executed as a single script
if __name__ == '__main__':
	SERVER_SOCKET = None
	while SERVER_SOCKET is None:
		SERVER_SOCKET = create_socket()

	setup_relay()

	while True:
		check_local_logs()
		sensor_data = read_data.get_data()
		if isinstance(sensor_data, list):
			#sensor values
			send_data_array(sensor_data)
		elif isinstance(sensor_data, int):
			#syslog
			raise_system_log(sensor_data)
		else:
			print(f"{datetime_manager.get_date()} - Unexpected data received from DCM")
		sensor_data = None
		time.sleep(0.05)
