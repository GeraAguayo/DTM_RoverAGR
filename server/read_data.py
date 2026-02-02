import serial
import RPi.GPIO as GPIO
import time
import os
from datetime import datetime

#Set up
BAUDRATE = 9600
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = BAUDRATE
DATA_LIMIT = 7 #Change here acording the number of values the arduino returns

def get_data():
	ser.reset_input_buffer()
	sensor_data = [None] * DATA_LIMIT #0 = temp, 1 = press, 2 = alt
	log_id = None

	while True:
		msg = ""
		read_ser = ser.readline()
		try:
			msg = read_ser.decode()
		except:
			date = get_date()
			print(f"{date} ERROR - Could not handle serial input {read_ser}")

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


def get_date():
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return date
