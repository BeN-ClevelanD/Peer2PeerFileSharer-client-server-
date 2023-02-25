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
        msg = server_socket.recv(4092) # Command response
        returnedPhraser = msg.decode()
        returnedPhrase = str(returnedPhraser)
        print(returnedPhrase)
        print(type(returnedPhrase))
        shouldGet = "ok"
        print(returnedPhrase == shouldGet)
        print(type(shouldGet))
        if shouldGet.__eq__(returnedPhrase):
            print('s1 and s2 are equal.')
        else:
            print("NOPE")
        #if(returnedPhrase == "Upload command has been received... awaiting data transfer \n" + "Please note: no white space is permitted in access key or file name"):
        if(returnedPhrase):
            print("YESSSSS")
            uploadFileName = input("Enter file name:\n")
            protectedStatus = input("Enter protected status of file:\n")
            if(protectedStatus == "private"):
                key = input("Enter private key:\n")
            elif(protectedStatus == "public"):
                key = "na"
            else:
                print("Please enter valid protected status: \"public\" or \"private\"")
            

            with open(uploadFileName, mode= "rb") as rf:
                read_words = rf.read(2046)
                if not read_words:
                    break

            textContent = read_words.decode()

            dataPackage = uploadFileName + " " + protectedStatus + " " + key + " " + textContent

            server_socket.send(bytes(dataPackage, "utf-8"))

        
            server_socket.close()


main()

