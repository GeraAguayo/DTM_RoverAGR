from datetime import datetime

def get_date():
	date = datetime.now().strftime("%Y-%m-%d")
	return date

def get_time():
	time = datetime.now().strftime("%H:%M:%S")
	return time

def get_datetime():
	datetime_ans = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	return datetime_ans
