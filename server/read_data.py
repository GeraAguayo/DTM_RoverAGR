import serial
import RPi.GPIO as GPIO
import time
import os

#Set up
BAUDRATE = 9600
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = BAUDRATE
DATA_LIMIT = 7 #Change here acording the number of values the arduino returns

def get_data():
	print("get_data() called")
	ser.reset_input_buffer()
	sensor_data = [None] * DATA_LIMIT #0 = temp, 1 = press, 2 = alt
	log_id = None

	while True:
		msg = ""
		read_ser = ser.readline()
		try:
			msg = read_ser.decode()
		except:
			print("Could not handle serial input: ", read_ser)

		if msg == "DATA\r\n":
			for i in range(DATA_LIMIT):
				val = 0.0
				try:
					val = float(ser.readline().decode())
				except:
					continue
				sensor_data[i] = val
			print("Returning value: ",sensor_data)
			return sensor_data
		elif msg == "SYSLOG\r\n":
			try:
				log_id = ser.readline().decode()
				log_id = int(log_id)
			except:
				continue
			print("Returning value: ",log_id)
			return log_id

