import serial
import RPi.GPIO as GPIO
import time
import os

#Set up
BAUDRATE = 9600
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = BAUDRATE
DATA_LIMIT = 3 #Change here acording the number of values the arduino returns

def get_data():
	print("get_data() called")
	data = [None] * DATA_LIMIT #0 = temp, 1 = press, 2 = alt
	log_id = None

	while True:
		read_ser = ser.readline()
		try:
			msg = read_ser.decode()
		except:
			pass
		if msg == "END\r\n":
			if log_id is not None:
				print("Returning log")
				print("----------")
				return log_id
			else:
				print("Returning sensor data")
				print("----------")
				return data
		elif msg == "DATA\r\n":
			print("Data from sensor")
			for i in range(DATA_LIMIT):
				read_ser = ser.readline()
				try:
					#if valid value from sensor received
					data[i] = float(read_ser)
				except:
					#Invalid value from sensor
					data[i] = 0.0
		elif msg == "SYSLOG\r\n":
			print("System log")
			read_ser = ser.readline()
			log_id = int(read_ser)

