import socket

# This function serves to execute the main functionality of the client-server architecture
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 1234)) # Reaching out to server

    while True:
        msg = server_socket.recv(1024) # Initial UI is sent from the server
        full_msg = 0
        #while len(msg) > 0:
         #   full_msg += msg
        print(msg.decode())
        command = input("Enter a command: ") # Command is given by client

        
        server_socket.send(bytes(command, "utf-8"))
        new_msg = server_socket.recv(4092) # Command response
        returnedPhrase = new_msg.decode()
        if(command == "upload"):
            print("uploadTime")
            upload(server_socket, returnedPhrase)
        if(command == "exit"):
             print("exitTime")
             exit(1)
             
             #server_socket.close()
        
        
        
        #if(returnedPhrase == "Upload command has been received... awaiting data transfer \n" + "Please note: no white space is permitted in access key or file name"):
def upload(server_socket, returnedPhrase):
            #print("YESSSSS")
    
    print(returnedPhrase)
    uploadFileName = input("Enter file name:\n")

    with open(uploadFileName, mode= "rb") as rf:
        read_words = rf.read(2046)
        while( not read_words):
            print("Please enter a valid file name")

    protectedStatus = input("Enter protected status of file:\n")
    if(protectedStatus == "private"):
        key = input("Enter private key:\n")
    elif(protectedStatus == "public"):
                key = "na"
    else:
        print("Please enter valid protected status: \"public\" or \"private\"")
            

            

    textContent = read_words.decode()

    dataPackage = uploadFileName + " " + protectedStatus + " " + key + " " + textContent

    server_socket.send(bytes(dataPackage, "utf-8"))

        
            #server_socket.close()


main()

