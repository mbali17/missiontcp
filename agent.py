import socket ;


def add_user():
    hostname = input("Enter host name eg:localhost or the ip")
    port = int(input("Enter the port for the agent"))
    agent_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    agent_socket.bind((hostname, port))
    agent_socket.listen(5)

if __name__ == "__main__":
    add_user()
