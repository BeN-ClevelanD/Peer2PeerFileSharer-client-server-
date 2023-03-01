import socket
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 1235))
public_dir = "../NetworksAssignmentOne/PublicFiles"


# global variable that assumes the value of command given by user
command = ""
# global variable that assumes the value of the filename supplied by a user whilst uploading a file
upload_file_name = ""
# global variable that assumes the value of the filename supplied by a user whilst downloading a file
download_file_name = ""
# global variable that assumes the value of the key supplied by a user whilst uploading a protected file
key = ""
# global variable that assumes the value of the protected status of a user-uploaded file
protected_status = ""
# global variable that assumes the value of the contents of a file that is uploaded by a user
file_contents = ""


def main():
    s.listen(5)
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established :)")
    with client_socket:
       print(f"Connection from {address} has been established :)")

       while True:
            show_ui(client_socket)
            command = str(client_socket.recv(2048).decode()).split()
            while(command[0] != "exit"):
                client_command(client_socket, command)
                command = str(client_socket.recv(2048).decode()).split()

            client_socket.send(bytes("Ending connection.", "utf-8"))
            client_socket.close()
            client_socket, address = s.accept()


def show_ui(client_socket):
    public_files = []
    with open("./Passwords.txt", "r") as files:
        for line in files:
            if line.split()[1] == "na":
                public_files.append(line.split()[0])
    msg = (bytes("Available services - Command format: "
                 "\n-------------------------------------"
                 "\nUpload file - upload open/protected destination key(if protected)"
                 "\nDownload file - download filename"
                 "\nAccess private folder - access filename key"
                 "\nCreate private folder - mkdir filename key"
                 "\nExit - exit"
                 "\n\nPublic files:\n---------------\n"
                 , "utf-8"))
    for f in public_files:
        msg += (bytes(f"{f}\n", "utf-8"))
    # msg += (bytes("\nPrivate folders:\n-----------------\n", "utf-8"))
    # for f in private_folders:
    #     msg += (bytes(f"{f}\n", "utf-8"))
    client_socket.send(msg)

def client_command(client_socket, command):
    string = command[0]

    if string == "exit":
        client_socket.send(bytes("Ending connection.", "utf-8"))
        client_socket.close()
    # elif string == "access":
    #     access(client_socket, command[1], command[2])
    elif string == "upload":
        upload(client_socket)

        #command = str(client_socket.recv(2048).decode()).split()
        #client_command(client_socket, command)
        #client_socket.close()
    elif string == "download":
        download(client_socket, command[1], command[2])
    # elif string == "mkdir":
    #     make_dir(client_socket, command[1], command[2])

#/NetworksAssignmentOne/PublicFiles'
# def access(client_socket, path, key):
#     if exists(f"../NetworksAssignmentOne/{path}"):
#         with open(f"../NetworksAssignmentOne/{path}") as file:
#             for line in file:
#                 if line.split()[0] == path and line.split()[1] == key:
#                     for f in listdir(f"../NetworksAssignmentOne/{path}"):
#                         client_socket.send(bytes(f"{f}\n", "utf-8"))
#     else:
#         client_socket.send(bytes("File given does not exist.", "utf-8"))
#
#
# def make_dir(client_socket, path, key):
#     mkdir(f"../NetworksAssignmentOne/PublicFiles/{path}")
#     file = open ("../NetworksAssignmentOne/Passwords.txt", "a")
#     file.write(f"{path} {key}\n")
#     show_ui(client_socket)
#

def upload (client_socket ):


    client_socket.send(bytes("ok", "utf-8"))

    dataTransfer =  str(client_socket.recv(2048).decode()).split()

    upload_file_name = dataTransfer[0]
    protected_status = dataTransfer[1]
    key = dataTransfer[2]
    file_contents = dataTransfer[3]

    client_socket.send(bytes("File upload complete.", "utf-8"))

    print(upload_file_name)
    print(protected_status)
    print(key)
    print(file_contents)


    #client_socket.send(bytes("Ending connection.", "utf-8"))
    #command = str(client_socket.recv(2048).decode()).split()

def download(client_socket, path, key):
    if exists(f"../NetworksAssignmentOne/PublicFiles/{path}"):
        with open("../NetworksAssignmentOne/Passwords.txt") as passwords_file:
            for line in passwords_file:
                if line.split()[0] == path and line.split()[1] == key:
                    with open(f"../NetworksAssignmentOne/PublicFiles/{path}") as requested_file:
                        msg = ""
                        client_socket.send(bytes("password ok", "utf-8"))
                        for requested_line in requested_file:
                            msg += requested_line
                        client_socket.send(bytes(msg, "utf-8"))
                        break
                else:
                    client_socket.send(bytes("Incorrect password, please try again.", "utf-8"))
    else:
        client_socket.send(bytes("Requested file path does not exist.", "utf-8"))


main()

