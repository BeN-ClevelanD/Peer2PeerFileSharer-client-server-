import socket
import hashlib
from Crypto.Cipher import AES

encryption_key = b'8\n\xfd\xc6\xee\xf8\xc6cv\xda\xee\x06-\t\xb0\xd7'



# This function serves to execute the main functionality of the client-server architecture


def rec_until_file_done(connection):
    
    msg_grande = b''

    bytez= 8192
    while True:
        msg_small = connection.recv(bytez)
        
        msg_grande += msg_small
        if bytez > len(msg_small):
            
            break
    return msg_grande

def printout_user_UI():
    print("User abilities: - Use the format specified on the right hand side of the dash: "
                "\n--------------------------------------"
                "\n->><<---->><<----<<>>---->><<---->><<-"
                "\nUpload file - upload-filename-key(\"na\" if public)"
                "\nDownload file - download-filename-key(\"na\" if public)"
                "\nView available public files - display public files"
                "\nExit - exit"
                "\n--------------------------------------"
                "\n->><<---->><<----<<>>---->><<---->><<-")






def main():
    
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
        else:
            print("Uknown command. Please try again...")
        
   

        command = input("Enter a command: ")
        


def recieve_public_files(server_socket):


    print("\nFiles publicly available for download:\n")
    response = server_socket.recv(2046).decode()
    if(response == "No public files available"):
        print("There are no publicly available files at the moment :(")
    else:
        
        print(response)
        print("\n---------------------------------")
        printout_user_UI()
    


def uploader(command, server_socket):

    headerSplitter  = "WANGO"
           
    command += headerSplitter

    commander = command.encode()
    
    try:
        with open(f"./{command.split('-')[1]}", "rb") as file:
                
            messaage = file.read()
            verification_hash = hashlib.blake2s(messaage).hexdigest()
            messaage, encr_key = encrypt(messaage, encryption_key)


            commander+= verification_hash.encode() + bytes("BREAKER", "utf-8") + messaage  + bytes("BREAKER", "utf-8") + encr_key
        
        
            file.close()
    
        server_socket.send(commander)
        response = server_socket.recv(2046).decode()
        print("\n")
        print(response)
        print("\n")
        printout_user_UI()
    except FileNotFoundError:
        print("The file you are trying to upload does not exist in this directory.")

    
    



def downloader(command, server_socket):
    response = server_socket.recv(2046).decode()
   
   
    
    if command.split("-")[0] == "download" and response == "password ok":
        
        downloadContent = rec_until_file_done(server_socket).split(b'BREAKER')
        incoming_hash = downloadContent[0].decode()
        fileContent = downloadContent[1]
        decr_key = downloadContent[2]

        decrypted_file = decrypt(fileContent, encryption_key, decr_key)
        
        local_hash = hashlib.blake2s(decrypted_file).hexdigest()
        
        if(incoming_hash == local_hash):
            
            filename = command.split("-")[1]
            file = open(f"{filename}", "wb")
    
            if not decrypted_file:
                exit(1)
            file.write(decrypted_file)
            file.close()
            print("\n")
            print("Download successful")
            print("\n")
            printout_user_UI()

        else:
            print("File contents corrupt or tampered with. Please resubmit download request.")
        
    else:
        print("\n")
        print(response)
        print("\n")
        printout_user_UI()
        

def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CTR)
    cipher_message = cipher.encrypt(message)
    nonce = cipher.nonce  # Creating the initialization vector for the encryption
    return cipher_message, nonce


def decrypt(cipher_message, key, nonce):
    decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return decrypt_cipher.decrypt(cipher_message)

main()