import socket

HEADER_SIZE = 10


# This function serves to execute the main functionality of the client-server architecture
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 1235)) # Reaching out to server

    msg = bytes(1)
    prev_msg = bytes(0)
    full_msg = ""
    while msg != prev_msg:
        msg = server_socket.recv(1024)  # Initial UI is sent from the server
        full_msg += msg.decode()
        prev_msg = msg
    print(full_msg)
    command = input("Enter a command: ") # Command is given by client
    server_socket.send(bytes(command, "utf-8"))
    response = server_socket.recv(1024).decode()
    if command.split()[0] == "download" and response == "password ok":
        file = open(f"{command.split()[1]}", "a")
        file.write(server_socket.recv(4092).decode())
        file = open(f"{command.split()[1]}", "r")
        print(file.read())
        file.close()
    else:
        print(response)
    server_socket.close()

main()

