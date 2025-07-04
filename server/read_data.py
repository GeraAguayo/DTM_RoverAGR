import serial 
import RPi.GPIO as GPIO
import time
import os

#Set up
BAUDRATE = 9600
ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = BAUDRATE
DATA_LIMIT = 3 #Change here acording the number of values the arduino returns
data = [None,None,None] #0 = temp, 1 = press, 2 = alt 

def get_data():
	print("Getting data...")
	serial_counter = 0
	while True:
		read_ser = ser.readline()
		msg = read_ser.decode()
		if msg == "END\r\n":
			print("End of packet")
			serial_counter = 0
			print(data)
			return data
		else:
			try:
				#if valid value from sensor received
				data[serial_counter] = float(read_ser)
				serial_counter+=1
			except:
				#Invalid value from sensor received None
				pass
