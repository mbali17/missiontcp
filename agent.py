import socket
from random import randint
from tcp_packet import TcpPacket
class Agent():
    def __init__(self,logger,src_port):
        print("Creating agent object.Implement agent specific code here")
    def generate_sequence_number(self):
        print("generate sequence number as some random number")
        return randint(100, 999)
    def perform_three_way_handshake(self):
        print("Performing three way handshake")
        #TODO: Create packet for each communication.
        #tcp_packet = TcpPacket()
    def start_communication(self):
        print("Starting communication")
        print(self.generate_sequence_number())
        self.perform_three_way_handshake()
