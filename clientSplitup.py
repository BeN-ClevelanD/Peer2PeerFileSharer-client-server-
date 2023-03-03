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

def printout_user_UI():
    print("User abilities: - (Use the format specified on the right hand side of the dash!): "
                "\n--------------------------------------"
                "\n->><<---->><<----<<>>---->><<---->><<-"
                "\nUpload file - upload-filename-key(\"na\" if public)"
                "\nDownload file - download-filename-key(\"na\" if public)"
                "\nView available public files - display public files"
                "\nExit - exit"
                "\n--------------------------------------"
                "\n->><<---->><<----<<>>---->><<---->><<-")






def main():
    alive = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 12345))  # Reaching out to server
    msg = bytes(1)
    prev_msg = bytes(0)
    full_msg = ""
    print("Welcome to the File uploader/downloader interface\n"
          "<---|><|---|><|---|><|---|><|---|><|---|><|--->")
    printout_user_UI()
    
    response = ""
    command = input("Enter a command: ")
    while True:
     


        
        if(command == "exit"):
            server_socket.send(command.encode())
            print("Signing off")
            exit(1)
        elif command == "display public files":
            server_socket.send(command.encode())
            recieve_public_files(server_socket)
                
        
        elif command.split('-')[0] == "upload":
            uploader(command, server_socket)
        
        elif command.split('-')[0] == "download":
            
            server_socket.send(command.encode())
            
     
            downloader(command, server_socket)
        
   

        command = input("Enter a command: ")
        


def recieve_public_files(server_socket):
    print("\nFiles publicly available for download:\n")
    response = server_socket.recv(2046).decode()
    print(response)
    print("\n---------------------------------")
    printout_user_UI()
    


def uploader(command, server_socket):

    msg = "WANGO"
           
    command += msg

    commander = command.encode()
    
    
    with open(f"./{command.split('-')[1]}", "rb") as file:
                
        messaage = file.read()
                
        commander += messaage

        file.close()
    
    server_socket.send(commander)
    response = server_socket.recv(2046).decode()
    print(response)
    printout_user_UI()

    
    



def downloader(command, server_socket):
    response = server_socket.recv(2046).decode()
    #print(response)
   
    
    if command.split("-")[0] == "download" and response == "password ok":
        
        downloadContent = rec_until_file_done(server_socket)
        filename = command.split("-")[1]
        file = open(f"{filename}", "wb")
        #print(len(downloadContent))
        if not downloadContent:
            exit(1)
        file.write(downloadContent)
        file.close()
        print("Download successful")
        printout_user_UI()
        
    else:
        print(response)
        printout_user_UI()
        


main()