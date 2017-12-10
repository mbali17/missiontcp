import base64

import msgpack
import pickle
import socket
from random import randint

import time

from tcp_packet import TcpPacket
#mir basheer ali(1001400462) neerja narayannapa (1001575625)
class Agent():
    map_of_agent_port ={"ann":111,"jan":200,"chan":111}
    def __init__(self,logger,src_port,agent_name):
        self.logger = logger
        self.src_port = src_port
        self.agent_name = agent_name
    def generate_sequence_number(self):
        print("generate sequence number as some random number")
        return randint(100, 999)
    def perform_three_way_handshake(self):
        print("Performing three way handshake",self.agent_name)
        #TODO: Re-use socket. Currently it creates a new socket every time.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost",Agent.map_of_agent_port.get('ann')))
        handshakePacket=TcpPacket(str(Agent.map_of_agent_port.get('jan')),
                                  str(Agent.map_of_agent_port.get('ann')),
                                  str(self.generate_sequence_number()),"1","20",
                                  "20","20","0","Intiating Handshake",syn="1")
        s.send(pickle.dumps(handshakePacket))
        print("sent connection request",self.agent_name)
        self.no_of_packets = 0
        while True:
            print("received response",self.agent_name)
            recieved_data = s.recv(1024)
            if not recieved_data:
                break
            recieved_packet = pickle.loads(recieved_data)
            if recieved_packet.ter == 0 :
                self.no_of_packets +=1
                print("Number of packets recieved: ",self.no_of_packets)
                if(self.no_of_packets>= 3):
                   #Continue noraml conversation
                   print("handhake sucessfull continuing to talk")
                   self.continueConversation(self.no_of_packets,s,response_packet)
                else:
                    ack = int(recieved_packet.ack)+1
                    seq_num = int(recieved_packet.acknowledgement)+1
                    print("The acknowledgement number of ",str(ack))
                    print("the sequence number is "+str(seq_num))
                    response_packet = TcpPacket("111","110",
                                      str(seq_num),str(ack),"20",
                                      "20","20","0","Handshake continued..",syn="1")
                    s.send(pickle.dumps(response_packet))


    def start_communication(self):
        print("Starting communication")
        self.perform_three_way_handshake()

    def continueConversation(self,no_of_packets,current_socket,packet):
        if self.agent_name == 'jan':
            with open("communicationFiles/Ann-_Jan.txt","r") as com_text:
                self.send_normal_packets(com_text.readline(), current_socket, no_of_packets, packet)

        if self.agent_name == 'chan':
           with open("communicationFiles/Ann-_Chan.txt","r") as com_text:
                self.send_normal_packets(com_text.readline(), current_socket, no_of_packets, packet)


    def send_normal_packets(self, current_line, current_socket, no_of_packets, packet):
        ack = int(packet.ack) + 1
        seq_num = int(packet.acknowledgement) + 1
        print("The acknowledgement number of ",str(ack))
        print("the sequence number is ",str(seq_num))
        # Using base64 encoding as the checksum
        checksum = base64.b64encode(current_line.encode('utf-8'))
        communicationPacket = TcpPacket("111", "110",
                                        str(seq_num), str(ack), "20",
                                        "20", checksum, "0", current_line, syn="1")
        current_socket.send(pickle.dumps(communicationPacket))
        while True:
            no_of_packets += 1
            recieved_data = current_socket.recv(1024)
            if not recieved_data:
                break
            recieved_packet = pickle.loads(recieved_data)
            print("The number of packets received is ", no_of_packets)
            if(no_of_packets == 5):
                msg = "Eavesdropping detected hence terminating connection. The mission continues "+"with aother agents hope to complete this."
                print(msg)
                print("setting urgent pointer and termination pointer!!")
                communicationPacket = TcpPacket("111", "110",
                                        str(seq_num), str(ack), "20",
                                        "20", checksum, "1", msg, syn="1",other="1")
                current_socket.send(pickle.dumps(communicationPacket))
                break
            else:
                #This is to terminate the mission
                if(no_of_packets == 10):
                    msg ="jan sending location to ann: (32° 43’ 22.77” N,97° 9’ 7.53” W )"
                    print(msg)
                    print("setting urgent pointer for the location disovered message!!")
                    communicationPacket = TcpPacket("111", "110",
                                            str(seq_num), str(ack), "20",
                                            "20", checksum, "1", msg, syn="1",ter="1")
                    current_socket.send(pickle.dumps(communicationPacket))
                    while True:
                        #X`print("received response",self.agent_name)
                        recieved_data = current_socket.recv(1024)
                        if not recieved_data:
                            break
                        recieved_packet = pickle.loads(recieved_data)
                        print("Message from jan ", recieved_packet.data)
                        print("The value of fin bit", recieved_packet.fin)
                        print("The value of ter bit", recieved_packet.ter)
                        break
                    print("Jan Communicating with Airforce HQ (Head quarters)")
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(("localhost",9000))
                    final_message = TcpPacket("9000","999",
                                      str(seq_num),str(ack),"20",
                                      "20","20","1","PEPPER THE PEPPER",syn="1",fin="1")
                    s.send(pickle.dumps(final_message))
                    msg = "Jan informing ann by  CONGRATULATIONS WE FRIED DRY GREEN LEAVES"
                    print("setting urgent pointer  pointer!!")
                    communicationPacket = TcpPacket("111", "110",
                                         str(seq_num), str(ack), "20",
                                         "20", checksum, "1", msg, syn="1",ter='1')
                    current_socket.send(pickle.dumps(communicationPacket))
                    while True:
                         #X`print("received response",self.agent_name)
                        recieved_data = current_socket.recv(1024)
                        if not recieved_data:
                            break
                        recieved_packet = pickle.loads(recieved_data)
                        print("Message from jan ", recieved_packet.data)
                        print("The value of fin bit", recieved_packet.fin)
                        print("The value of ter bit", recieved_packet.ter)
                if recieved_packet.ter == 0:
                    time.sleep(5)
                    ack = int(recieved_packet.ack) + 1
                    seq_num = int(recieved_packet.acknowledgement) + 1
                    current_socket.send(pickle.dumps(communicationPacket))
