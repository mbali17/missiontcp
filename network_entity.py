'''
This would be a thread class. Which is started for each network entity( agent,router or HQ)
'''
import socket
from threading import Thread
import mission_helper
"""
Spins a new thread for each agent in the file.
"""
class NetworkEnity(Thread):
        def __init__(self,entity_details):
            super(NetworkEnity, self).__init__()
            self.entity_details = entity_details
        def read_data_and_send_response(self):
            while True:
                #Define the bytes of data to be received each time.
                #TODO: Make this buffer size configurable via properties file or console.
                recieved_data = self.socket_curr.recv(20)
                print("The data recieved is"+ recieved_data)

        def start_server(self):
            #setting up socket stream.
            entity_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #binding the port to the hostname.Since bind accepts only one param we need to create tuple for the host and port.
            server_details = (self.entity_details_split[0], int(self.entity_details_split[1]))
            entity_socket.bind(server_details)
            #Server mode on and accepts upto 5 connections,before ignoring the incoming request.
            #TODO : Make the number of connections configurable.
            entity_socket.listen(5)
            #accept connections infinitely until interrupted.
            while True:
                #Rerurns the new socket for the connection and the host connected to.
                try:
                    current_socket,host = entity_socket.accept()
                    self.socket_curr = current_socket
                finally:
                    current_socket.close()
        def run(self):
            self.entity_details_split = self.entity_details.split(",")
            #Line in CSV is terminated with a new line hence truncating it.
            self.entityLogger = mission_helper.create_log_file(self.entity_details_split[3].rstrip("\n")+".log","entity_details_split[3]")
            self.entityLogger.info("the entity details are"+self.entity_details)
            self.start_server()
            #Assing the value of the flag to check if it is router or agent
            self.is_router = self.entity_details_split[2]
