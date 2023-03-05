import socket
import hashlib
from Crypto.Cipher import AES

encryption_key = b'8\n\xfd\xc6\xee\xf8\xc6cv\xda\xee\x06-\t\xb0\xd7'


# This function serves to execute the main functionality of the client-server architecture
def rec_until_file_done(connection):
    msg_grande = b''
    bytez = 2046

    while True:
        msg_small = connection.recv(bytez)
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
    address = input("IP address: ")
    port = int(input("Port number: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if address == 'localhost':
        server_socket.connect((socket.gethostbyname('localhost'), port))  # Reaching out to server
    else:
        server_socket.connect((address, port))
    print("Welcome to the File uploader/downloader interface\n"
          "<---|><|---|><|---|><|---|><|---|><|---|><|--->")
    printout_user_UI()
    command = input("Enter a command: ")
    while True:
        if(command == "exit"):
            server_socket.send(command.encode())
            print("Signing off")
            exit(1)
        elif command == "display":
            server_socket.send(command.encode())
            receive_public_files(server_socket)
        elif command.split('-')[0] == "upload":
            uploader(command, server_socket)
        elif command.split('-')[0] == "download":
            server_socket.send(command.encode())
            downloader(command, server_socket)
        else:
            print("Incorrect command. Please try again.")
        command = input("Enter a command: ")


def receive_public_files(server_socket):
    print("\nFiles publicly available for download:\n")
    response = server_socket.recv(2046).decode()
    if response:
        print(response)
        print("\n---------------------------------")
        printout_user_UI()
    else:
        print("There are no publicly available files at the moment :(")
    

def uploader(command, server_socket):
    header = "WANGO"  # This signifies the start of the data transfer
    message = command + header  # Adding the header to the message
    message = message.encode()
    try:
        with open(f"./{command.split('-')[1]}", "rb") as file:
            data = file.read()
            hash_value = hashlib.blake2s(data).hexdigest()  # for error checking
            data, nonce = encrypt(data, encryption_key) # encrypting the data
            message += hash_value.encode() + bytes("BREAKER", "utf-8")
            message += data + bytes("BREAKER", "utf-8") + nonce
            file.close()
        server_socket.send(message)
        response = server_socket.recv(2046).decode()
        print(response)
        printout_user_UI()
    except FileNotFoundError:
        print("File does not exist. Please try again.")

    
def downloader(command, server_socket):
    response = server_socket.recv(2046).decode()
    if response == "password ok":
        content = rec_until_file_done(server_socket)

        hash_value = content.split(b'BREAKER')[0].decode()
        data = content.split(b'BREAKER')[1]
        nonce = content.split(b'BREAKER')[2]

        decrypted_data = decrypt(data, encryption_key, nonce)
        local_hash = hashlib.blake2s(decrypted_data).hexdigest()

        if local_hash == hash_value:
            filename = command.split("-")[1]
            file = open(f"{filename}", "wb")
            file.write(decrypted_data)
            file.close()
            print("File successfully downloaded.\n")
        else:
            print("File corrupted. File not written to disk.\n")

    else:
        print(response, "\n")

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