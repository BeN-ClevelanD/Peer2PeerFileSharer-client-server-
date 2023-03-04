import socket
import hashlib
from os import listdir, mkdir
from os.path import isfile, join, exists, isdir
import _thread
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 12345))
public_dir = "../NetworksAssignmentOne/PublicFiles"

def rec_until_file_done(sock):
  
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
        _thread.start_new_thread ( process_requests, (client_socket, address))
       
        


def process_requests(client_socket, address):
    with client_socket:
        print(f"Connection from {address} has been established :)")
        while True:
                                        
            command = rec_until_file_done(client_socket).split(b'breaker')
            header = command[0].decode().split("-") 
               
            client_command(client_socket, command, header)
            if command[0].decode() == "exit":
                break
        client_socket.send(bytes("Ending connection.", "utf-8"))
        client_socket.close()

def client_command(client_socket, command, header):
    
    if header[0] == "upload":
        upload(client_socket, header[1], header[2], command[2], command[1].decode())
    elif header[0] == "download":
     
        download(client_socket, header[1], header[2])
    elif header[0] == "exit":
        pass
    elif header[0] == "display public files":
        get_public_files(client_socket)
    else:
        client_socket.send(bytes("Unknown command. Please try again.", "utf-8"))

def get_public_files(client_socket):
    public_files = []
    msger = ""
    msg = msger.encode()
    with open("./Passwords.txt", "r") as files:
        for line in files:
            
            if line.split()[1] == "na":
                public_files.append(line.split()[0])
    for f in public_files:
        msg += bytes(f"{f}\n", "utf-8")
    
    if(len(public_files) == 0):
        client_socket.send(bytes("No public files available", "utf-8"))
    else:
        client_socket.send(msg)



def upload(client_socket, upload_file_name, key, file_contents, incoming_hash):
    server_local_hash = hashlib.blake2s(file_contents).hexdigest()
    if(server_local_hash == incoming_hash):

        with open("./Passwords.txt", "r") as reader:
      
            if(not filename_check(reader, upload_file_name)):
          
                with open(f"./PublicFiles/{upload_file_name}", "wb") as fw:
        
                
                    


                    if not file_contents:
                        exit(1)
                    fw.write(file_contents)
                if(not filename_check(reader, upload_file_name)):
                    with open("./Passwords.txt", "a") as pw:
                        pw.write(f"{upload_file_name} {key}\n")
                        pw.close()
                client_socket.send(bytes("File upload complete.", "utf-8"))
            else:
                client_socket.send(bytes("Filename already in use", "utf-8"))
    else:
        client_socket.send(bytes("File contents is corrupt or has been tampered with. Please resubmit upload request.", "utf-8"))


def download(client_socket, path, key):

    breaker = "breaker"
  
    if exists(f"../NetworksAssignmentOne/PublicFiles/{path}"):
        with open("../NetworksAssignmentOne/Passwords.txt") as passwords_file:
           
            if(password_check(key, passwords_file, path)):
                client_socket.send(bytes("password ok", "utf-8"))

               
                foundFile = True
                with open(f"../NetworksAssignmentOne/PublicFiles/{path}", "rb") as requested_file:
                    msg = requested_file.read()

                    server_outgoing_hash = hashlib.blake2s(msg).hexdigest()

                        
                    package = server_outgoing_hash.encode() + breaker.encode() + msg
                    client_socket.send(package)
                    requested_file.close()
                    
                   
            else:
                client_socket.send(bytes("Incorrect password, please try again.", "utf-8")) 
                                      
    else:
        client_socket.send(bytes("Requested file path does not exist.", "utf-8"))
     



def password_check(key, passwords_file, path ):
    for line in passwords_file:
        

        if line.split()[0] == path and line.split()[1] == key:
            return True
        
def filename_check(passwords_file, path ):
    for line in passwords_file:
       

        if line.split()[0] == path:
            return True
        


main()

