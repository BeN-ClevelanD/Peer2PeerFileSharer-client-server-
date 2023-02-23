import socket
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 1234))
public_dir = "../NetworksAssignmentOne/PublicFiles"


def main():
    s.listen(5)
    while True:
        client_socket, address = s.accept()
        print(f"Connection from {address} has been established :)")
        show_ui(client_socket)
        command = str(client_socket.recv(2048).decode()).split()
        client_command(client_socket, command)
        client_socket.close()


def show_ui(client_socket):
    public_files = [f for f in listdir(public_dir) if isfile(join(public_dir, f))]
    private_folders = [f for f in listdir(public_dir) if isdir(join(public_dir, f))]
    client_socket.send(bytes("Available services - Command format: "
                             "\n-------------------------------------"
                             "\nUpload file - upload open/protected destination key(if protected)"
                             "\nDownload file - download filename"
                             "\nAccess private folder - access filename key"
                             "\nCreate private folder - mkdir filename key"
                             "\nExit - exit"
                             "\n\nPublic files:\n---------------\n"
                             , "utf-8"))
    for f in public_files:
        client_socket.send(bytes(f"{f}\n", "utf-8"))
    client_socket.send(bytes("\nPrivate folders:\n-----------------\n", "utf-8"))
    for f in private_folders:
        client_socket.send(bytes(f"{f}\n", "utf-8"))


def client_command(client_socket, command):
    string = command[0]

    if string == "exit":
        client_socket.send(bytes("Ending connection.", "utf-8"))
        client_socket.close()
    elif string == "access":
        access(client_socket, command[1], command[2])
    elif string == "upload":
        pass
    elif string == "download":
        pass
    elif string == "mkdir":
        mkdir(client_socket, command[1], command[2])


def access(client_socket, path, key):
    if exists(f"../NetworksAssignmentOne/{path}"):
        with open(f"../NetworksAssignmentOne/{path}") as file:
            for line in file:
                if line.split()[0] == path and line.split()[1] == key:
                    for f in listdir(f"../NetworksAssignmentOne/{path}"):
                        client_socket.send(bytes(f"{f}\n", "utf-8"))
    else:
        client_socket.send(bytes("File given does not exist.", "utf-8"))


def mkdir(client_socket, path, key):
    mkdir(f"../NetworksAssignmentOne/{path}")
    file = open ("../NetworksAssignmentOne/Passwords.txt", "a")
    file.write(f"{path} {key}")
    show_ui(client_socket)


main()

