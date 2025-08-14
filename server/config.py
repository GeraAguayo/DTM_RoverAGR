import json

#Ip address of the rover in the network
IP_ADDR = "192.168.137.117"

#Local port from udp comms
LOCAL_PORT = 20001

#Buffer size for upd msgs
BUFFER_SIZE = 1024


#Helper funtions if used as an import
def get_ip_address():
	with open("net_config.json") as json_file:
		config_data = json.load(json_file)
		return config_data["IP_ADDR"]

def get_local_port():
	with open("net_config.json") as json_file:
		config_data = json.load(json_file)
		return config_data["LOCAL_PORT"]

def get_buffer_size():
	with open("net_config.json") as json_file:
		config_data = json.load(json_file)
		return config_data["BUFFER_SIZE"]



#Main if executed as script
if __name__ == '__main__':
	with open("net_config.json") as json_file:
		config_data = json.load(json_file)

		#User prompt
		print("ROVER AGR network configuration")
		print("Press enter to leave the deafult option")
		ip_add = input(f"Ip address [{config_data['IP_ADDR']}]: ")
		port = input(f"Local port [{config_data['LOCAL_PORT']}]: ")
		buff = input(f"Buffer size[{config_data['BUFFER_SIZE']}]:  ")

		if ip_add != "":
			config_data["IP_ADDR"] = ip_add
		if port != "":
			config_data["LOCAL_PORT"] = int(port)
		if buff != "":
			config_data["BUFFER_SIZE"] = int(buff)
		#Write changes to json
		with open("net_config.json","w") as file_to_wr:
			json.dump(config_data, file_to_wr, indent=4)
		print("Configuration changed!")
