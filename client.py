import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((socket.gethostbyname('localhost'), 1234))

full_msg = ''
while True:
    msg = server_socket.recv(4092)
    if len(msg) <= 0:
        break
    print(msg.decode())
    command = input("Enter a command: ")
    server_socket.send(bytes(command, "utf-8"))
    msg = server_socket.recv(2048)
    print (msg.decode())
