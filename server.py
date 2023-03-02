import socket
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 12345))
public_dir = "../NetworksAssignmentOne/PublicFiles"


def main():
    while True:
        s.listen(5)
        client_socket, address = s.accept()
        with client_socket:
            print(f"Connection from {address} has been established :)")
            while True:
                client_socket.send(get_ui())
                command = str(client_socket.recv(2048).decode()).split('-')
                client_command(client_socket, command)
                if command[0] == "exit":
                    break
            client_socket.send(bytes("Ending connection.", "utf-8"))
            client_socket.close()


def get_ui():
    public_files = []
    with open("./Passwords.txt", "r") as files:
        for line in files:
            if line.split()[1] == "na":
                public_files.append(line.split()[0])
    msg = bytes("Available services - Command format: "
                "\n-------------------------------------"
                "\nUpload file - upload-filename-key(\"na\" if public)"
                "\nDownload file - download-filename-key(\"na\" if public)"
                "\nExit - exit"
                "\n\nPublic files:\n---------------\n", "utf-8")
    for f in public_files:
        msg += bytes(f"{f}\n", "utf-8")
    return msg


def client_command(client_socket, command):
    string = command[0]
    if string == "upload":
        upload(client_socket, command[1], command[2], command[3])
    elif string == "download":
        download(client_socket, command[1], command[2])
    elif string == "exit":
        pass
    else:
        client_socket.send(bytes("Unknown command. Please try again.", "utf-8"))


def upload(client_socket, upload_file_name, key, file_contents):
    with open(f"./PublicFiles/{upload_file_name}", "w") as fw:
        if not file_contents:
            exit(1)
        fw.write(file_contents)
    with open("./Passwords.txt", "a") as pw:
        pw.write(f"{upload_file_name} {key}\n")
    client_socket.send(bytes("File upload complete.", "utf-8"))


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

