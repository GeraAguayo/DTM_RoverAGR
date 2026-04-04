# Code for the video transmission from the rover to the base station
# Gerardo Aguayo - Rover AGR
import struct
import cv2
import socket
import math
import config
import datetime_manager
import time
max_length = 65000
host = config.get_base_station_add()
port = 5000
net_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def raise_syslog(log_id):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.sendto(log_id.encode(), ('127.0.0.1', 5005))

def connectCamera():
	while True:
		for index in range(4):
			cap = cv2.VideoCapture(index)
			if cap.isOpened():
				#set low resolution
				cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
				cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
				return cap
			cap.release()
		#camera not found
		print(f"{datetime_manager.get_datetime()} Error - Camera not found")
		raise_syslog("4")

cap = connectCamera()
FPS = 30
frame_duration = 1.0 / FPS
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 35]

while True:
	start_time = time.time()

	#empty opencv buffer
	for _ in range(2):
		cap.grab()

	ret, frame = cap.read()
	if not ret:
		cap = connectCamera()
		continue

	retval, buffer = cv2.imencode(".jpg", frame, encode_param)


	if retval:
		data = buffer.tobytes()
		size = len(data)

		if size < max_length:
			net_socket.sendto(data, (host,port))
		else:
			num_packs = math.ceil(size / max_length)
			net_socket.sendto(struct.pack("<i",num_packs), (host, port))

			for i in range(num_packs):
				chunk = data[i * max_length : (i+1) * max_length]
				net_socket.sendto(chunk, (host,port))
	#LIMIT FPS
	elapsed = time.time() - start_time
	time_to_sleep = frame_duration - elapsed
	if time_to_sleep > 0:
		time.sleep(time_to_sleep)
