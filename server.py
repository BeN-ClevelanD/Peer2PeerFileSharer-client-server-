import socket
from os import listdir
from os.path import isfile, join


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostbyname('localhost'), 1234))
    s.listen(5)
    public_dir = "../NetworksAssignmentOne/PublicFiles"

    while True:
        client_socket, address = s.accept()
        print(f"Connection from {address} has been established :)")
        public_files = [f for f in listdir(public_dir) if isfile(join(public_dir, f))]
        client_socket.send(bytes("Available services - Command format: "
                                 "\nUpload file - upload open/protected destination key(if protected)"
                                 "\nDownload file - download filename"
                                 "\nAccess private folder - access filename key"
                                 "\nCreate private folder - mkdir filename key"
                                 "\nExit - exit"
                                 "\n\nPublic files:\n"
                                 , "utf-8"))
        for f in public_files:
            client_socket.send(bytes(f"{f}\n", "utf-8"))
        client_socket.send(bytes("\nPrivate folders:", "utf-8"))
        command = client_socket.recv(1024)
        client_command(command, client_socket)
        # client_socket.close()


def client_command(command, sckt):
    string = command.decode()
    # for char in string:
    #     index = 0
    #     if char != " ":
    #         index += 1

    if string == "exit":
        sckt.send(bytes("Ending connection.", "utf-8"))
        sckt.close()
# def print_functions():



main()

