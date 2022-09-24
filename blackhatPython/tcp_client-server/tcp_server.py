# Import required libraries
import socket
import threading

# Set server configurations
IP = '127.0.0.1'
PORT = 'Insert port here'

# Define connection socket and starts listening for income connections
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5) # Store a maximum backlog of 5 connections
    print(f'[*] Listening on {IP}:{PORT}')

    # Receive clients connection info, then, create a new thread object pointing at function to handle clients
    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# Define client handler function, perform recv and send some data to client.
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

# Defines main function and call main()
if __name__ == '__main__':
    main()