import socket
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 12345))
public_dir = "../NetworksAssignmentOne/PublicFiles"

def rec_until_file_done(sock):
     # 4 KiB
    msg_grande = b''

    bytez= 8192
    while True:
        msg_small = sock.recv(bytez)
       
        msg_grande += msg_small
        if len(msg_small) != bytez:
            
            break
    return msg_grande


def main():
    while True:
        s.listen(5)
        client_socket, address = s.accept()
        client_socket.send(get_ui())
        with client_socket:
            print(f"Connection from {address} has been established :)")
            while True:
                #print("sent ui again")
                #client_socket.send(get_ui())                          
                command = rec_until_file_done(client_socket).split(b'WANGO')
                header = command[0].decode().split("-") 
                client_command(client_socket, command, header)
                if command[0].decode() == "exit":
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


def client_command(client_socket, command, header):
    
    if header[0] == "upload":
        upload(client_socket, header[1], header[2], command[1])
    elif header[0] == "download":
     
        download(client_socket, header[1], header[2])
    elif header[0] == "exit":
        pass
    else:
        client_socket.send(bytes("Unknown command. Please try again.", "utf-8"))


def upload(client_socket, upload_file_name, key, file_contents):
    with open(f"./PublicFiles/{upload_file_name}", "wb") as fw:
        print(len(file_contents))
        if not file_contents:
            exit(1)
        fw.write(file_contents)
    with open("./Passwords.txt", "a") as pw:
        pw.write(f"{upload_file_name} {key}\n")
        pw.close()
    client_socket.send(bytes("File upload complete.", "utf-8"))




def download(client_socket, path, key):
  
    if exists(f"../NetworksAssignmentOne/PublicFiles/{path}"):
        with open("../NetworksAssignmentOne/Passwords.txt") as passwords_file:
           
            if(password_check(key, passwords_file, path)):
                client_socket.send(bytes("password ok", "utf-8"))

               
                foundFile = True
                with open(f"../NetworksAssignmentOne/PublicFiles/{path}", "rb") as requested_file:
                    msg = requested_file.read()
                    print (len(msg))
                        
                        
                    client_socket.send(msg)
                    requested_file.close()
                    
                   
            else:
                client_socket.send(bytes("Incorrect password, please try again.", "utf-8")) 
                                      
    else:
        client_socket.send(bytes("Requested file path does not exist.", "utf-8"))
     



def password_check(key, passwords_file, path ):
    for line in passwords_file:

        if line.split()[0] == path and line.split()[1] == key:
            return True


main()

