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
    """
    This function sevres to provide buffering to the data stream. It returns the entire data
    stream conglomerated into a single object.
    Parameters:
    :param sock -- this is the client socket from which the data is received.
    """
    msg_grande = b''
    bytez = 8192
    while True:
        msg_small = sock.recv(bytez)
        msg_grande += msg_small
        if len(msg_small) != bytez:
            break
    return msg_grande


def main():
    """
    This is the main method of the program. It accepts client requests and creates the threads which
    in turn service them.
    """
    while True:
        s.listen(5)
        client_socket, address = s.accept()
        _thread.start_new_thread(process_requests, (client_socket, address))


def process_requests(client_socket, address):
    """
    This function handles client requests in their respective threads.
    Parameters:
    :param client_socket -- the socket of the client. This is used to send and receive data.
    :param address -- address of the client. This is printed on the server side
    """
    with client_socket:
        print(f"Connection from {address} has been established :)")
        while True:
            message = rec_until_file_done(client_socket).split(b'WANGO')
            # WANGO is an arbitrary term used to split the message into its header and data contents
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
    """
    This function serves to break down a client's request and interpret them.
    Parameters:
    :param client_socket: self-explanatory
    :param data_transfer: this is relevant for the upload function. this includes the data to be written to the
                            server-side disk, the hash_value of the data, and the nonce, which is used for decryption.
    :param header: this provides the requested command of the user, as well as the file name and key if they are
                    uploading/downloading a file
    """
    if header[0] == "upload":
        hash_value = data_transfer.split(b'BREAKER')[0].decode()  # Splitting message contents
        message = data_transfer.split(b'BREAKER')[1]
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
    """
    This function serves to retrieve and send a string representation of the public files available for download.
    Files with a password "na" are considered public.
    Parameters:
    :param client_socket: the client socket that the string is sent to
    """
    public_files = []
    msg = ""
    msg = msg.encode()
    with open("./Passwords.txt", "r") as files:
        # A file in the presence of the passwords textfile with the password "na" will be considered public
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
    """
    This function performs the upload functionality of the server. Uploaded files need to be checked if they clash
    with a name already on disk and if they have been corrupted. They also need to be decrypted using the encryption
    key which the client and server share, as well as the nonce unique to each data transfer.
    Parameters:
    :param client_socket: used to send control statements to the client
    :param upload_file_name: file name to be written on server-side disk
    :param key: password for the file, "na" if public
    :param data: the encrypted data being transferred
    :param incoming_hash: the supposed hash value of the unencrypted data
    :param nonce: the nonce value, used for decryption
    :return:
    """
    decrypted_data = decrypt(data, encryption_key, nonce)  # Decrypting data
    server_local_hash = hashlib.blake2s(decrypted_data).hexdigest()  # Retrieving hash value for decrypted data

    if server_local_hash == incoming_hash:
        if not exists("./PublicFiles/upload_file_name"):
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
    """
    This function achieves the server-side download functionality. To download a file, the file must exist and the
    key provided must be correct.
    Parameters:
    :param client_socket: used for sending control messages and the data itself.
    :param path: the name of the requested file
    :param key: the key value provided by the user, may be correct or incorrect
    :return:
    """
    if exists(f"../NetworksAssignmentOne/PublicFiles/{path}"):
        with open("../NetworksAssignmentOne/Passwords.txt") as passwords_file:
            if password_check(key, passwords_file, path):
                client_socket.send(bytes("password ok", "utf-8"))
                # Control message to let client-side know that data is coming that must be written to disk
                with open(f"../NetworksAssignmentOne/PublicFiles/{path}", "rb") as requested_file:
                    data = requested_file.read()
                    server_outgoing_hash = hashlib.blake2s(data).hexdigest()  # for error checking
                    data, nonce = encrypt(data, encryption_key)  # for encryption
                    message = server_outgoing_hash.encode() + bytes("BREAKER", "utf-8")  # adding hash to msg
                    message += data + bytes("BREAKER", "utf-8") + nonce  # adding data + encryption data to msg
                    client_socket.send(message)
                    requested_file.close()
            else:
                client_socket.send(bytes("Incorrect password, please try again.", "utf-8"))
    else:
        client_socket.send(bytes("Requested file path does not exist.", "utf-8"))


def password_check(key, passwords_file, path):
    """
    This is a helper function which checks if a file has the correct associated password.
    :param key: the user provided password
    :param passwords_file: the file path of the textfile which contains the passwords
    :param path: the path of the requested file
    :return: a Boolean value describing whether the user provided password was correct or not
    """
    for line in passwords_file:
        if line.split()[0] == path and line.split()[1] == key:
            return True


def encrypt(message, key):
    """
    This function performs encryption on data using AES CTR encryption.
    :param message: the data to be encrypted
    :param key: the encryption key
    :return cipher_message: the encrypted message
    :return nonce: a value unique to the encrypted message which is used for decryption.
    """
    cipher = AES.new(key, AES.MODE_CTR)
    cipher_message = cipher.encrypt(message)
    nonce = cipher.nonce  # Creating the initialization vector for the encryption
    return cipher_message, nonce


def decrypt(cipher_message, key, nonce):
    """
    This function performs decryption on data using AES CTR encryption.
    :param cipher_message: the data to be decrypted
    :param key: the decryption key
    :param nonce: a value unique to the encrypted message which is used for decryption.
    :return decrypt_cipher.decrypt(cipher_message): the decrypted data
    """
    decrypt_cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return decrypt_cipher.decrypt(cipher_message)


main()
