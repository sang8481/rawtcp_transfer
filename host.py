# Server as well as host of connection.
# receive file from client.

import socket
import sys
import struct
from headerstructs import IpHeader, TcpHeader
if len(sys.argv) < 3 :
	print("Usage : sudo python3 host.py [Host IP] [Host Port] [Client IP]")
	sys.exit()

class socket_controller :
	def __init__(self, server_socket, expected_client_ip) :
		self.sock = server_socket
		self.expected_client_ip = expected_client_ip
	
	def recieved_syn_packet() :
		while True :
			data, addr = sock.recvfrom(2048)
			
			if str(addr[0]) == self.expected_client_ip :
				return str(addr[0])
			else :
				print('received pkt from not expected ip addr')
				return str(addr[0])
				
		soc

def main() :
	host_ip = sys.argv[1]
	host_port = sys.argv[2]
	expected_client_ip = sys.argv[3]
	expected_client_port = 0
	ip_tuple = (host_ip, expected_client_ip)
	port_tuple = (host_ip, expected_client_port) 
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	server_socket.bind((host_ip, host_port))
	controller = socket_controller(server_socket)

	sender_ip = controller.recieved_syn_packet()
	controller.handshake_with(sender_ip)
	

	print("listening from... : " + str(server_socket.getsockname()))
	while True :
		data, addr = server_socket.recvfrom(2048)
		if str(addr[0]) == expected_client_ip :
			print("packet received from addr" + str(addr))
			print("printing packet :")
			printcount = 1
			for byte in (data[:20].hex()) :
				if printcount % 2 == 1 :
					print(str(byte), end="")
				else :
					print(str(byte)+" ", end="")
				if printcount % 8 == 0 :
					print()
				printcount+= 1
			IpHeader().reconstruct_with(data)
			TcpHeader().reconstruct_with(data[20:])
		"""
		if tcp_socket
		"""

	server_socket.close()


if __name__ == '__main__' :
	main()

