'''
This would be a thread class. Which is started for each network entity( agent,router or HQ)
'''
import socket
from random import randint
from threading import Thread
import pickle
import polling as polling
import time

import sys

from agent import Agent
from router import Router
import mission_helper
import os
from tcp_packet import TcpPacket
#mir basheer ali(1001400462) neerja narayannapa (1001575625)
"""
Spins a new thread for each network entity in the network_entities file.
"""
class NetworkEnity(Thread):
        def __init__(self,entity_details):
            super(NetworkEnity, self).__init__()
            self.entity_details = entity_details
            self.is_filefound = False

        def read_data_and_send_response(self):
            while True:
                #Define the bytes of data to be received each time.
                #TODO: Make this buffer size configurable via properties file or console.
                recieved_data = self.socket_curr.recv(1024)
                if not recieved_data:
                    #   print("End of data")
                    break
                #Deseralize the recieved object
                #TODO: Fix infinite loop.TO be continued later
                #print("the source port is",self.recieved_packet.sourceID)
                self.recieved_packet = pickle.loads(recieved_data)
                print("is the packet urgent",self.recieved_packet.urgentpointer)
                if self.recieved_packet.sourceID == "9000":
                    print("HQ received code",self.recieved_packet.data)
                    sys.exit()
                if(self.recieved_packet.ter == 0):
                    #print("sending response!")
                    ack = int(self.recieved_packet.ack)+1
                    seq_num = int(self.recieved_packet.acknowledgement)+1
                    print("the data in the packet is",self.recieved_packet.data)
                    response_packet = TcpPacket("111","110",
                                      str(seq_num),str(ack),"20",
                                      "20","20","0","data",syn="1")
                    self.socket_curr.send(pickle.dumps(response_packet))
                else:
                    msg ="Ann confirming the taget with ’Execute’ and the code for HQ is 'PEPPER THE PEPPER.'"
                    print("sending command to execute")
                    communicationPacket = TcpPacket("111", "110",
                                            str(seq_num), str(ack), "20",
                                            "20", "20", "1", msg, syn="1",other="1")
                    self.socket_curr.send(pickle.dumps(communicationPacket))
                    while True:
                        recieved_data = self.socket_curr.recv(1024)
                        if not recieved_data:
                            break
                        self.recieved_packet = pickle.loads(recieved_data)
                        print("received location with urgent pointer",self.recieved_packet.urgentpointer)
                        print(self.recieved_packet.data)
                        break
                    msg = "Meet me at(32.76” N, -97.07” W )"
                    ack = int(self.recieved_packet.ack)+1
                    seq_num = int(self.recieved_packet.acknowledgement)+1
                    print("Terminating connection with ann setting fin bit and ter bit")
                    response_packet = TcpPacket("111","110",
                                      str(seq_num),str(ack),"20",
                                      "20","20","1",msg,syn="1",fin="1",ter="1")
                    self.socket_curr.send(pickle.dumps(response_packet))


                    #print("Response sent!")
        #https://pypi.python.org/pypi/polling/0.3.0 -- python polling to know if the file exists
        #TODO : Make the times configurable via a properties file.,
        def poll_if_file_exists(self):
            self.entityLogger.info("Polling to check if the start communication file is created")
            #Check if the file exists every 30 seconds for 2 minutes this is the flag to start communication
            file_handle = polling.poll(
                lambda: open('start_communication.txt'),
                        ignore_exceptions=(IOError),
                        timeout=60,
                        step=17,)
            return file_handle
        def start_server(self):
            #setting up socket stream.
            entity_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #binding the port to the hostname.Since bind accepts only one param we need to create tuple for the host and port.
            server_details = (self.entity_details_split[0], int(self.entity_details_split[1]))
            entity_socket.bind(server_details)
            #Server mode on and accepts upto 5 connections,before ignoring the incoming request.
            #TODO : Make the number of connections configurable.
            entity_socket.listen(5)
            #self.poll_if_file_exists()
            self.entityLogger.info("Starting  communication"+self.entity_details_split[3].rstrip("\n"))
            #Check to see if the current thread is an agent and run djikstras
            if int(self.entity_details_split[2]) == 1 and not os.path.exists("dijkstra.csv"):
                mission_helper.find_shortest_path()
            #print("AM i here")
            self.start_communication()
            #accept connections infinitely until interrupted.
            self.listen_to_connections(entity_socket)


        def listen_to_connections(self, entity_socket):
            while True:
                self.entityLogger.info("accepting connection")
                # Rerurns the new socket for the connection and the host connected to.x
                current_socket, host = entity_socket.accept()
                #print("Obtained request")
                self.socket_curr = current_socket
                self.read_data_and_send_response()
                self.socket_curr.close()

        def run(self):
            self.entity_details_split = self.entity_details.split(",")
            #Assing the value of the flag to check if it is router or agent
            self.is_router = self.entity_details_split[2]
            #Line in CSV is terminated with a new line hence truncating it.
            self.entityLogger = mission_helper.create_log_file(self.entity_details_split[3].rstrip("\n")+".log","entity_details_split[3]")
            self.entityLogger.info("the entity details are"+self.entity_details)
            #Only Ann and HQ are the servers
            if self.entity_details_split[3].rstrip("\n") == 'ann'  :
                self.start_server()
            elif self.entity_details_split[3].rstrip("\n") == 'HQ':
                self.start_server()
            else:
                time.sleep(5)
                self.start_communication()

        def start_communication(self):
            if int(self.is_router) == 1 or int(self.is_router) == 2:
                print("initiating other agent!!",self.entity_details_split[3].rstrip("\n"))
                if self.entity_details_split[3].rstrip("\n") != 'ann':
                        if self.entity_details_split[3].rstrip("\n") != 'HQ':
                            agent =Agent(self.entityLogger,int(self.entity_details_split[1]),
                                     self.entity_details_split[3].rstrip("\n"))
                            agent.start_communication()
            else:
                router = Router()
        def convert_byte_to_object(self,data):
            unpickled_image = pickle.loads(data)
            print("unpickled object",unpickled_image.getSourceID)
