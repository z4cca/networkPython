# Import required libraries
import socket
import threading

#Asks for client nickname
nick = input("Insert your nickname: ")

# Create ipv4, TCP connection socket and connects to server (IP, Port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55666))

# Receiving messages from the server
def receive():
    while True:
        try:
            # If asked for nickname, sign in
            message = client.recv(1024).decode('ascii')
            if message == 'nickName':
                client.send(nick.encode('ascii'))
            # Else, print message from server
            else:
                print(message)
        # If not possible to receive message from server, close connection
        except:
            print("An error  occurred, closing connection")
            client.close()
            break

# Writing messages
def write():
    while True:
        message = f'{nick}: {input("")}'
        client.send(message.encode('ascii'))

# Setting Thread target and starts Thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

