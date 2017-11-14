import socket
'''
Reads the data from the current socket and sends an appropriate message.
'''
def read_data_and_send_response(socket_curr):
    while True:
        #Define the bytes of data to be received each time.
        #TODO: Make this buffer size configurable via properties file or console.
        recieved_data = socket_curr.recv(20)
        print("The data recieved is"+ recieved_data)

'''
 Adds the current user to be a server.
 :return:
'''
def add_user():
    hostname = input("Enter host name eg:localhost or the ip")
    port = int(input("Enter the port for the agent"))
    #setting up socket stream.
    agent_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #binding the port to the hostname.Since bind accepts only one param we need to create tuple for the host and port.
    server_details = (hostname, port)
    agent_socket.bind(server_details)
    #Server mode on and accepts upto 5 connections,before ignoring the incoming request.
    #TODO : Make the number of connections configurable.
    agent_socket.listen(5)
    print("Started on port ",port,"and hostname: ",hostname)
    #accept connections infinitely until interrupted.
    while True:
        #Rerurns the new socket for the connection and the host connected to.
        try:
            current_socket,host = agent_socket.accept()
            read_data_and_send_response(current_socket)
        finally:
            current_socket.close()

if __name__ == "__main__":
    add_user()
