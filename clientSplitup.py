import socket

HEADER_SIZE = 10


# This function serves to execute the main functionality of the client-server architecture


def rec_until_file_done(connection):
     # 4 KiB
    msg_grande = b''

    bytez= 2046
    while True:
        msg_small = connection.recv(bytez)
        #print(len(msg_small))
        msg_grande += msg_small
        if bytez > len(msg_small):
            # either 0 or end of data
            break
    return msg_grande







def main():
    alive = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 12345))  # Reaching out to server
    msg = bytes(1)
    prev_msg = bytes(0)
    full_msg = ""
    msg = rec_until_file_done(server_socket)  # Initial UI is sent from the server
    full_msg = msg.decode()
    print(full_msg)
    response = ""
    command = input("Enter a command: ")
    while True:
        #msg = rec_until_file_done(server_socket)  # Initial UI is sent from the server
        #full_msg = msg.decode()
        #print(full_msg)
      


        
        if(command == "exit"):
            server_socket.send(command.encode())
            exit(1)
        
        elif command.split('-')[0] == "upload":
            uploader(command, server_socket)
        
        elif command.split('-')[0] == "download":
            
            server_socket.send(command.encode())
            print("getting response below")
     
            downloader(command, server_socket)
        print("new command time")
   

        command = input("Enter a command: ")
        


        

def uploader(command, server_socket):

    msg = "WANGO"
           
    command += msg

    commander = command.encode()
    print("all ok so far")
    print(type(commander))
    
    with open(f"./{command.split('-')[1]}", "rb") as file:
                
        messaage = file.read()
                
        commander += messaage

        file.close()
    
    server_socket.send(commander)
    response = server_socket.recv(2046).decode()
    print(response)

    
    



def downloader(command, server_socket):
    response = server_socket.recv(2046).decode()
    print(response)
    print("Later response repat")
    print(response)
    if command.split("-")[0] == "download" and response == "password ok":
        print("HAPPY TIMES")
        downloadContent = rec_until_file_done(server_socket)
        filename = command.split("-")[1]
        file = open(f"{filename}", "wb")
        print(len(downloadContent))
        if not downloadContent:
            exit(1)
        file.write(downloadContent)
        file.close()
        
    else:
        print(response)
        


main()