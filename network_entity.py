'''
This would be a thread class. Which is started for each network entity( agent,router or HQ)
'''
import socket
from threading import Thread

import polling as polling
from agent import Agent
from router import Router
import mission_helper
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
                if not recieved_data: break
                print("The data recieved is", recieved_data)

        #https://pypi.python.org/pypi/polling/0.3.0 -- python polling to know if the file exists
        #TODO : Make the times configurable via a properties file.,
        def poll_if_file_exists(self):
            self.entityLogger.info("Polling to check if the start communication file is created")
            #Check if the file exists every 30 seconds for 2 minutes this is the flag to start communication
            file_handle = polling.poll(
                lambda: open('start_communication.txt'),
                        ignore_exceptions=(IOError),
                        timeout=120,
                        step=60,)
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
            self.poll_if_file_exists()
            self.entityLogger.info("Starting  communication"+self.entity_details_split[3].rstrip("\n"))
            #accept connections infinitely until interrupted.
            self.listen_to_connections(entity_socket)

        def listen_to_connections(self, entity_socket):
            while True:
                self.entityLogger.info("accepting connection")
                # Rerurns the new socket for the connection and the host connected to.
                if  not self.is_filefound :
                    self.is_filefound=True
                    self.start_communication()
                current_socket, host = entity_socket.accept()
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
            self.start_server()


        def start_communication(self):
            if int(self.is_router) == 1 or int(self.is_router) == 2:
                agent =Agent(self.entityLogger,int(self.entity_details_split[1]))
                agent.start_communication()
            else:
                router = Router()

