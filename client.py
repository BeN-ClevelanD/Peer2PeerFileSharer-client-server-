import socket

key = b'8\n\xfd\xc6\xee\xf8\xc6cv\xda\xee\x06-\t\xb0\xd7'

# This function serves to execute the main functionality of the client-server architecture
def main():
    alive = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((socket.gethostbyname('localhost'), 12345))  # Reaching out to server
    while alive:
        msg = bytes(1)
        prev_msg = bytes(0)
        full_msg = ""

        while msg != prev_msg:
            msg = server_socket.recv(1024)  # Initial UI is sent from the server
            full_msg += msg.decode()
            prev_msg = msg
        print(full_msg)

        command = input("Enter a command: ")  # Command is given by client

        if command.split('-')[0] == "upload":
            with open(f"./{command.split('-')[1]}", "r") as file:
                msg = "-"
                for line in file:
                    msg += line
                command += msg
                # print(command)
        elif command == "exit":
            alive = False

        server_socket.send(bytes(command, "utf-8"))
        response = server_socket.recv(1024).decode()

        if command.split()[0] == "download" and response == "password ok":
            file = open(f"{command.split()[1]}", "a")
            file.write(server_socket.recv(4092).decode())
            file = open(f"{command.split()[1]}", "r")
            print(file.read())
            file.close()
        else:
            print(response)

    server_socket.close()


def encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CTR)
    cipher_message = cipher.encrypt(message)
    nonce = cipher.nonce  # Creating the initialization vector for the encryption
    return cipher_message, nonce


def decrypt(cipher_message, key, nonce):
    decrypt_cipher = AES.new(key, AES.MODE_CBC, nonce=nonce)
    return decrypt_cipher.decrypt(cipher_message)


main()