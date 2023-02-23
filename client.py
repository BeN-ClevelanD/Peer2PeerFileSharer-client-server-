import socket

# This function serves to execute the main functionality of the client-server architecture
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 1234)) # Reaching out to server

    while True:
        msg = server_socket.recv(1024) # Initial UI is sent from the server
        full_msg = 0
        while len(msg) > 0:
            full_msg += msg
        print(full_msg.decode())
        command = input("Enter a command: ") # Command is given by client
        server_socket.send(bytes(command, "utf-8"))
        msg = server_socket.recv(4092) # Command response
        print(msg.decode())
        server_socket.close()


main()

