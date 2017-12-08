import msgpack
import pickle
import socket
from random import randint
from tcp_packet import TcpPacket
class Agent():
    map_of_agent_port ={"ann":111,"jan":200,"chan":111}
    def __init__(self,logger,src_port,agent_name):
        print("Creating agent object.Implement agent specific code here")
        self.logger = logger
        self.src_port = src_port
        self.agent_name = agent_name
    def generate_sequence_number(self):
        print("generate sequence number as some random number")
        return randint(100, 999)
    def perform_three_way_handshake(self):
        print("Performing three way handshake",self.agent_name)
        if(self.agent_name == "ann"):
            print("agent ann's communication")
            #TODO: Re-use socket. Currently it creates a new socket every time.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost",Agent.map_of_agent_port.get('ann')))
            handshakePacket=TcpPacket(str(Agent.map_of_agent_port.get('jan')),
                                      str(Agent.map_of_agent_port.get('ann')),
                                       str(self.generate_sequence_number()),"1","20","20","20","0","data",syn="1")
            # packet ={}
            # packet['src']=bytes(str(Agent.map_of_agent_port.get('jan')),'utf-8')
            s.send(pickle.dumps(handshakePacket))
        if(self.agent_name == "jan"):
            print("agent jan's communication")
        if(self.agent_name == "chan"):
            print("chans communication")
    def start_communication(self):
        print("Starting communication")
        self.perform_three_way_handshake()
