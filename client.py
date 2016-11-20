import threading
import queue
import time
import os
import socket
import sys
import struct
import time
import queue
from headerstructs import ip_header, tcp_header
# Command line arguments check
if len(sys.argv) < 4 :
    print ('Usage : sudo python3 client.py [Dest IP Addr] [Dest Port] [File Path] [MSS size]')
	
def main() :
	source_ip = '192.168.35.147'
	source_port = 28481
	dest_ip = str(sys.argv[1])
	dest_port = int(sys.argv[2])
	file_path = str(sys.argv[3])
	arg_mss = int(sys.argv[4])
	src_dest_ip = (source_ip, dest_ip)
	src_dest_port = (source_port, dest_port)
	payload_data = "sample message".encode()
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	mss_chunk_queue = queue.Queue()

	packet = (ip_header(src_dest_ip).get_ip_struct() 		
			+ tcp_header(src_dest_port, src_dest_ip, payload_data).mss(arg_mss).syn().get_tcp_struct()
			+ payload_data)
	print('ip packet length : ' + str(len(packet)))
	bytes_sent = client_socket.sendto(packet, (dest_ip, dest_port))
	print(str(bytes_sent)+ " bytes sent.")

if __name__ == '__main__' :
	main()











