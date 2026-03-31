# Code for the video transmission from the rover to the base station
# Gerardo Aguayo - Rover AGR

import struct
import cv2
import socket
import math
import config
from datetime import datetime
import time
max_length = 65000
host = config.get_base_station_add()
port = 5000
net_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


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
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		print(f"{date} Error - Camera not found")

cap = connectCamera()
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]

while True:
	start_time = time.time()

	ret, frame = cap.read()
	if not ret:
		cap = connectCamera(0)
		continue

	retval, buffer = cv2.imencode(".jpg", frame, encode_param)


	if retval:
		buffer = buffer.tobytes()
		buffer_size = len(buffer)
		num_packs = math.ceil(buffer_size / max_length)

		net_socket.sendto(struct.pack("i",num_packs), (host, port))

		for i in range(num_packs):
			left = i * max_length
			right = left + max_length
			data = buffer[left:right]
			net_socket.sendto(data, (host,port))
	#LIMIT FPS
	time_to_sleep = (1./30.) - (time.time() - start_time)
	if time_to_sleep > 0:
		time.sleep(time_to_sleep)
