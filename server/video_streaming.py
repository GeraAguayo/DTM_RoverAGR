import cv2
import socket
import math
import pickle

max_length = 65000
host = "192.168.1.100" #Base station PC ip
port = 5000

net_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

cap = cv2.VideoCapture(1)
ret, frame = cap.read()

while ret:
    #compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        #Covert to byte array
        buffer = buffer.tobytes()
        #get size of frame
        buffer_size = len(buffer)

        num_packs = 1

        if buffer_size > max_length:
            num_packs = math.ceil(buffer_size/max_length)

        frame_info = {
            "packs" : num_packs
        }

        #send the number of packets to be expected
        print("Number of packets: ", num_packs)
        net_socket.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length

        for i in range(num_packs):
            #Truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            #send the frames accordingly
            net_socket.sendto(data, (host,port))
            print("Sending video...")

    ret, frame = cap.read()

print("done")
