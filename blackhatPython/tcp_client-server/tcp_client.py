# import required libraries
import socket

# Set server configurations
server_ip = "127.0.0.1"
server_port = 'Insert port here'

# Create a ipv4, TCP connection socket object and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Send data bytes
client.send(b"GET / HTTP/1.1\r\nlocalhost\r\n\r\n")

# Receive and print data
response = client.recv(4096)
print(response.decode())

# Close connection
client.close()
