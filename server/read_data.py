import serial
import serial.tools.list_ports
import RPi.GPIO as GPIO
import time
import os
import datetime_manager
ser = None

def find_serial():
        ports = serial.tools.list_ports.comports()
        for port in ports:
                if "Arduino" in port.description or "ACM" in port.description or "USB" in port.description or "CH340" in port.description:
                        return port.device
        return None

def get_data():
	global ser
	DATA_LIMIT = 7

	if ser is None:
		path = find_serial()
		if path is None:
			return None
		try:
			ser = serial.Serial(path, 9600, timeout=1)
		except:
			return None

	sensor_data = [None] * DATA_LIMIT
	log_id = None
	try:
		ser.reset_input_buffer()
	except:
		print(f"{datetime_manager.get_datetime()} - Arduino not found")
		log_id = 3
		return log_id

	while True:
		msg = ""
		read_ser = ser.readline()
		try:
			msg = read_ser.decode()
		except:
			print(f"{datetime_manager.get_datetime()} ERROR - Arduino not found")
			log_id = 3
			return log_id

		if msg == "DATA\r\n":
			for i in range(DATA_LIMIT):
				val = 0.0
				try:
					val = float(ser.readline().decode())
				except:
					continue
				sensor_data[i] = val
			return sensor_data
		elif msg == "SYSLOG\r\n":
			try:
				log_id = ser.readline().decode()
				log_id = int(log_id)
			except:
				continue
			return log_id
