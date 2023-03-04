import socket
import hashlib
import _thread
from os.path import exists
from Crypto.Cipher import AES


encryption_key = b'8\n\xfd\xc6\xee\xf8\xc6cv\xda\xee\x06-\t\xb0\xd7'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname('localhost'), 12345))
public_dir = "../NetworksAssignmentOne/PublicFiles"


def rec_until_file_done(sock):
    msg_grande = b''
    bytez = 8192
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
        _thread.start_new_thread(process_requests, (client_socket, address))


def process_requests(client_socket, address):
    with client_socket:
        print(f"Connection from {address} has been established :)")
        while True:
            message = rec_until_file_done(client_socket).split(b'WANGO')
            header = message[0].decode().split("-")
            try:  # if there is data attached, put it into data_transfer, if not then ignore.
                data_transfer = message[1]
            except IndexError:
                data_transfer = []
            client_command(client_socket, data_transfer, header)
            if message[0].decode() == "exit":
                break
        client_socket.send(bytes("Ending connection.", "utf-8"))
        client_socket.close()


def client_command(client_socket, data_transfer, header):
    if header[0] == "upload":
        hash_value = data_transfer.split(b'BREAKER')[0].decode()
        message = data_transfer.split(b'BREAKER')[1]   # Splitting message contents into data and nonce for decryption
        nonce = data_transfer.split(b'BREAKER')[2]
        upload(client_socket, header[1], header[2], message, hash_value, nonce)
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
    msg = ""
    msg = msg.encode()
    with open("./Passwords.txt", "r") as files:
        for line in files:
            if line.split()[1] == "na":
                public_files.append(line.split()[0])
    for f in public_files:
        msg += bytes(f"{f}\n", "utf-8")
    
    if len(public_files) == 0:
        client_socket.send(bytes("No public files available", "utf-8"))
    else:
        client_socket.send(msg)


def upload(client_socket, upload_file_name, key, data, incoming_hash, nonce):
    decrypted_data = decrypt(data, encryption_key, nonce)
    server_local_hash = hashlib.blake2s(decrypted_data).hexdigest()
    
    if server_local_hash == incoming_hash:
        with open("./Passwords.txt", "r") as reader:
            if not filename_check(reader, upload_file_name):
                with open(f"./PublicFiles/{upload_file_name}", "wb") as fw:
                    fw.write(decrypted_data)
                    with open("./Passwords.txt", "a") as pw:
                        pw.write(f"{upload_file_name} {key}\n")
                        pw.close()
                client_socket.send(bytes("File upload successful.", "utf-8"))
            else:
                client_socket.send(bytes("Filename already in use. "
                                         "Please rename file and resubmit upload request", "utf-8"))
    else:
        client_socket.send(bytes("File contents corrupt. Please resubmit upload request.", "utf-8"))


def download(client_socket, path, key):
    if exists(f"../NetworksAssignmentOne/PublicFiles/{path}"):
        with open("../NetworksAssignmentOne/Passwords.txt") as passwords_file:
            if password_check(key, passwords_file, path):
                client_socket.send(bytes("password ok", "utf-8"))
                with open(f"../NetworksAssignmentOne/PublicFiles/{path}", "rb") as requested_file:
                    data = requested_file.read()
                    server_outgoing_hash = hashlib.blake2s(data).hexdigest()    # for error checking
                    data, nonce = encrypt(data, encryption_key)     # for encryption
                    message = server_outgoing_hash.encode() + bytes("BREAKER", "utf-8")     # adding hash to msg
                    message += data + bytes("BREAKER", "utf-8") + nonce       # adding data + encryption data to msg
                    client_socket.send(message)
                    requested_file.close()
            else:
                client_socket.send(bytes("Incorrect password, please try again.", "utf-8")) 
    else:
        client_socket.send(bytes("Requested file path does not exist.", "utf-8"))


def password_check(key, passwords_file, path ):
    for line in passwords_file:
        if line.split()[0] == path and line.split()[1] == key:
            return True


def filename_check(passwords_file, path):
    for line in passwords_file:
        if line.split()[0] == path:
            return True


def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CTR)
    cipher_message = cipher.encrypt(message)
    nonce = cipher.nonce  # Creating the initialization vector for the encryption
    return cipher_message, nonce


def decrypt(cipher_message, key, nonce):
    decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return decrypt_cipher.decrypt(cipher_message)


main()

