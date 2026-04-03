# This script reads the data from the DCM and saves it to an csv file locally
import datetime_manager
import read_data #returns an array containing sensor data
import math
from collections import deque
import csv


class DistanceCalculator:
	def __init__(self, size=15):
		self.size = size
		self.lat_history = deque(maxlen=size)
		self.lon_history = deque(maxlen=size)
		self.last_avg_lat = 0.0
		self.last_avg_lon = 0.0
		self.total_distance_traveled = 0.0

	def add_coordinates(self, lat, lon):
		if lat == 0.0 or lon == 0.0:
			return #skip first invalid coords

		r_lat = round(lat,5)
		r_lon = round(lon,5)
		self.lat_history.append(r_lat)
		self.lon_history.append(r_lon)

	def get_average(self):
		avg_lat = sum(self.lat_history) / len(self.lat_history)
		avg_lon = sum(self.lon_history) / len(self.lon_history)
		return avg_lat, avg_lon

	def calculate_delta(self):
		if len(self.lat_history) < self.size:
			return 0.0

		current_avg_lat, current_avg_lon = self.get_average()

		if self.last_avg_lat == 0.0:
			self.last_avg_lat = current_avg_lat
			self.last_avg_lon = current_avg_lon
			return 0.0

		#haversine formula
		R =6371000
		phi1 = math.radians(self.last_avg_lat)
		phi2 = math.radians(current_avg_lat)

		d_lat = math.radians(current_avg_lat - self.last_avg_lat)
		d_lon = math.radians(current_avg_lon - self.last_avg_lon)

		a = (math.sin(d_lat / 2)**2 +
		    math.cos(phi1) * math.cos(phi2) * math.sin(d_lon / 2)**2)

		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		delta = R*c

		self.last_avg_lat = current_avg_lat
		self.last_avg_lon = current_avg_lon
		if delta >= 5.0:
			self.total_distance_traveled += delta
			self.last_avg_lat = current_avg_lat
			self.last_avg_lon = current_avg_lon
			return delta
		return 0.0

#main script
date_file = datetime_manager.get_datetime()
FILENAME = "local_telemetry_" + date_file + "_roverAGR.csv"
FILEPATH = "/home/gerardo/local_telemetry/"
HEADERS = ["Date", "Time", "Temperature", "Altitude", "Pressure", "Humidity", "Gas", "Latitude", "Longitude","Distance Traveled"]
TELEMETRY_VALUES = 7
dist_calc = DistanceCalculator(size=15)
new_file = True

while True:
	sensor_data = read_data.get_data()

	if isinstance(sensor_data, list) and len(sensor_data) == TELEMETRY_VALUES:
		date_str = datetime_manager.get_date()
		time_str = datetime_manager.get_time()

		temp, pres, alt, hum, gas, lat, lon = sensor_data

		dist_calc.add_coordinates(lat,lon)
		dist_calc.calculate_delta()
		current_total_dist = dist_calc.total_distance_traveled

		row = [date_str, time_str, temp, alt, pres, hum, gas, lat, lon, current_total_dist]
		print(row)
		if lat != 0.0 and lon != 0.0:
			if new_file:
				with open(FILEPATH+FILENAME, 'w', newline='', encoding='utf-8') as file:
					writer = csv.writer(file)
					writer.writerow(HEADERS)
					new_file = False

			with open(FILEPATH+FILENAME, 'a', newline='',encoding='utf-8') as file:
				writer = csv.writer(file)
				writer.writerow(row)

