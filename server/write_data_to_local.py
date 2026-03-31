# This script reads the data from the DCM and saves it to an csv file locally

from datetime import datetime
import read_data #returns an array containing sensor data
import math
from collections import deque


class DistanceCalculator:
	def __init__(self, size=15):
		self.size = size
		self.lat_history = deque(maxlen=size)
		self.lon_history = deque(maxlen=size)
		self.last_avg_lat = 0.0
		self.last_avg_lon = 0.0
		self.total_distance_traveled = 0.0

	def add_coordinates(self, lat, lon):
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

		if delta >= 5.0:
			self.total_distance_traveled += delta
			self.last_avg_lat = current_avg_lat
			self.last_avg_lon = current_avg_lon

		return 0.0

#main script
date_file = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
FILENAME = "local_telemetry_" + date_file + "_roverAGR.csv"
HEADERS = ["Date", "Time", "Temperature", "Altitude", "Pressure", "Humidity", "Gas", "Latitude", "Longitude","Distance Traveled"]
TELEMETRY_VALUES = 7
dist_calc = DistanceCalculator(size=15)
while True:
	sensor_data = read_data.get_data()

	if isinstance(sensor_data, list) and len(sensor_data) == TELEMETRY_VALUES:
		date_str = datetime.now().strftime("%Y-%m-%d")
		time_str = datetime.now().strftime("%H:%M:%S")

		temp, pres, alt, hum, gas, lat, lon = sensor_data

		dist_calc.add_coordinates(lat,lon)
		dist_calc.calculate_delta()
		current_total_dist = dist_calc.total_distance_traveled

		row = [date_str, time_str, temp, alt, pres, hum, gas, lat, lon, current_total_dist]
		print(row)
