"""                                                                                       
#IP HEADER STRUCTURE
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#TCP HEADER STRUCTURE

+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""

import struct
import socket
import sys

class IpHeader :
	def __init__(self, ip_tuple = ('0.0.0.0', '0.0.0.0')) :
		self.version = 4 
		self.ip_header_length = 5
		self.type_of_service = 0
		self.total_length = 0
		self.identification = 0
		self.flags = 0
		self.frag_offset = 0
		self.time_to_live = 255
		self.protocol = 6
		self.header_checksum = 0
		self.source_ip_addr = socket.inet_aton(ip_tuple[0])
		self.dest_ip_addr = socket.inet_aton(ip_tuple[1])

	def get_ip_struct(self) :
		ihl_with_ver = (self.version << 4) + self.ip_header_length
		flags_with_offset = (self.flags << 13) + self.frag_offset
		binary_ip_header = struct.pack("!BBHHHBBH4s4s",
										ihl_with_ver,
										self.type_of_service,
										self.total_length,
										self.identification,
										flags_with_offset,
										self.time_to_live,
										self.protocol,
										self.header_checksum,
										self.source_ip_addr,
										self.dest_ip_addr)
		return binary_ip_header

	def reconstruct_with(self, data) :
		raw_ip_header = struct.unpack("!BBHHHBBH4s4s", data[:20])
		version_ihl = raw_ip_header[0]
		self.version = version_ihl >> 4
		self.ip_header_length = (version_ihl & 0xf) * 4


		return self
	
class TcpHeader :
	def __init__(self, port_tuple = (0, 0), ip_tuple = ('0.0.0.0', '0.0.0.0')) :
		self.ip_tuple = ip_tuple
		self.source_port = port_tuple[0]
		self.dest_port = port_tuple[1]
		self.sequence_number = 0
		self.acknowledge_number = 0
		self.data_offset = 5
		self.reserved = 0
		self.tcpflag_fin = 0
		self.tcpflag_syn = 0
		self.tcpflag_rst = 0
		self.tcpflag_psh = 0
		self.tcpflag_ack = 0
		self.tcpflag_urg = 0
		self.window = 365
		self.checksum = 0
		self.urgent_pointer = 0
		self.option_kind = 0
		self.option_legnth = 0
		self.mss_size = 0
		self.data = b''

	def syn(self) :
		self.tcpflag_syn = 1
		return self

	def ack(self) :
		self.tcpflag_ack = 1
		return self

	def mss(self, mss_size) :
		self.data_offset = 6
		self.option_kind = 2
		self.option_legnth = 4
		self.mss_size = mss_size
		return self
	
	def data(self, data) :
		self.data = data
		return self

	def reconstruct_with(self, raw_tcpheader) :
		raw_tcp_header = struct.unpack("!HHLLBBHHH", raw_tcpheader)
		self.source_port = raw_tcp_header[0]
		self.dest_port = raw_tcp_header[1]
		self.sequence_number = raw_tcp_header[2]
		self.acknowledge_number = raw_tcp_header[3]
		self.data_offset = (raw_tcp_header[4] >> 4)
		flags = raw_tcp_header[5]
		self.tcpflag_syn = (flags >> 1) & 0x1
		self.tcpflag_ack = (flags >> 4) & 0x1
		self.window = tcp_header[6]
		self.checksum = tcp_header[7]
		self.urgent_pointer = tcp_header[8]


	def get_tcp_struct(self) :
		data_offset_multiplied = (self.data_offset << 4)
		flags = ( (self.tcpflag_fin)
				+ (self.tcpflag_syn << 1)
				+ (self.tcpflag_rst << 2)
				+ (self.tcpflag_psh << 3)
				+ (self.tcpflag_ack << 4)
				+ (self.tcpflag_urg << 5))

		binary_tcp_header = struct.pack('!HHLLBBHHH',
										self.source_port,
										self.dest_port,
										self.sequence_number,
										self.acknowledge_number,
										data_offset_multiplied,
										flags,
										self.window,
										self.checksum,
										self.urgent_pointer)

		# If mss option specified : 24 bytes header
		if self.data_offset == 6 :
			binary_tcp_header += struct.pack('!BBH',
											self.option_kind,
											self.option_legnth,
											self.mss_size)

		# Pseudo Header 
		ps_source_ip = socket.inet_aton(self.ip_tuple[0])
		ps_dest_ip = socket.inet_aton(self.ip_tuple[1])
		reserved = 0
		protocol = socket.IPPROTO_TCP
		tcp_header_length = len(binary_tcp_header) + len(self.data)
		pseudo_header = struct.pack("!4s4sBBH",
									ps_source_ip,
									ps_dest_ip,
									reserved,
									protocol,
									tcp_header_length)
		tcp_block = pseudo_header + binary_tcp_header + self.data
		self.checksum = checksum(tcp_block)

		# Re-packing tcp header includes its calculated checksum
		binary_tcp_header = (struct.pack('!HHLLBBH',
										self.source_port,
										self.dest_port,
										self.sequence_number,
										self.acknowledge_number,
										data_offset_multiplied,
										flags,
										self.window)
							+struct.pack('H',
										self.checksum)
							+struct.pack('!H',
										self.urgent_pointer))

		if self.data_offset == 6 :
			binary_tcp_header += struct.pack('!BBH',
											self.option_kind,
											self.option_legnth,
											self.mss_size)
		return binary_tcp_header

# checksum functions needed for calculation checksum
def checksum(data):
	s = 0

	# loop taking 2 characters at a time
	for i in range(0, len(data) - 1, 2):
		w = data[i] + (data[i+1] << 8)
		s = s + w

	s = (s>>16) + (s & 0xffff);
	s = s + (s >> 16);

	#complement and mask to 4 byte short
	s = ~s & 0xffff

	return s
