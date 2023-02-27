import socket

HEADER_SIZE = 10


# This function serves to execute the main functionality of the client-server architecture
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 1234)) # Reaching out to server

    while True:
        end_msg = False
        full_msg = ''
        print("entering loop")
        while not end_msg:
            msg = server_socket.recv(6)
            full_msg += msg.decode("utf-8")
            print(full_msg[len(full_msg)-7:len(full_msg)])
            if full_msg[len(full_msg)-7:len(full_msg)] == "ENDMSG"):
                print("End msg is true")
                end_msg = True
        print(full_msg)
        command = input("Enter a command: ") # Command is given by client
        server_socket.send(bytes(command, "utf-8"))
        msg = server_socket.recv(4092) # Command response
        print(msg.decode())
        server_socket.close()


main()

