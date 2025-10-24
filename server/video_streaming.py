import cv2
import socket
import math
import pickle

max_length = 65000
host = "192.168.1.100" #Base station PC ip
#host = "192.168.1.169" #test
port = 5000

net_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

#define resolution for resizing
NEW_WIDTH = 320
NEW_HEIGHT = 240
JPEG_QUALITY = 70
 
while ret:
    #compress frame
    small_frame = cv2.resize(frame, (NEW_WIDTH, NEW_HEIGHT), interpolation=cv2.INTER_AREA)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]

    #retval, buffer = cv2.imencode(".jpg", frame)
    retval, buffer = cv2.imencode(".jpg", small_frame, encode_param)

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

