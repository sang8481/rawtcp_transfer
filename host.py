# Server as well as host of connection.
# receive file from client.

import socket
import sys
import struct
from headerstructs import ip_header, tcp_header

def main() :
	host_port = 18482
	expected_client_ip = '192.168.35.147'
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	server_socket.bind(('192.168.35.14', 18481))

	print("listening from... : " + str(server_socket.getsockname()))
	while True :
		data, addr = server_socket.recvfrom(2048)
		if str(addr[0]) == expected_client_ip :
			print("packet received from addr" + str(addr))
			print("printing packet :")
			printcount = 1
			for byte in (data) :
				if printcount % 2 == 1 :
					print(str(byte), end="")
				else :
					print(str(byte)+" ", end="")
				if printcount % 8 == 0 :
					print()
				printcount+= 1
		"""
		if tcp_socket
		"""

	server_socket.close()


if __name__ == '__main__' :
	main()

