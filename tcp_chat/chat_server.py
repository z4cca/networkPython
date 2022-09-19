# Import required libraries
import threading
import socket

# Set server configuration
host = '127.0.0.1' # Localhost
port = 55666 

# Creates ipv4, TCP connection socket and start listening for incoming clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Empty lists for storage of clients connections and nicknames
clients = []
nicknames = []

# Broadcast message for every client on server
def broadcast(message):
    for client in clients:
        client.send(message)

# Client connection handle function
def handle(client):
    # While server can receive message from client, broadcast to all
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        # If not, remove client from list of clients and closes its connection
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick = nicknames[index]
            broadcast(f'{nick} left the chat.'.encode('ascii'))
            nicknames.remove(nick)
            break

# Receive client function
def receive():
    # Server stays open to new connections, print whenever a client connects
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Asks for client nickname and append to nicknames list
        client.send('nickName'.encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        nicknames.append(nick)
        clients.append(client)

        # Broadcast to chat and sends connection confirmation to client
        print(f'Nickname of client is {nick}')
        broadcast(f'{nick} joined the chat.'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        #Thread handle
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Main function
print("Server is listening...")
receive()
