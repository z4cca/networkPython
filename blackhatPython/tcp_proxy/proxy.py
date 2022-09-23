# import required libraries
import sys
import socket
import threading

# Hex_FILTER print the character, if possible. else prints a dot '.'
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

# Define hexdump function that takes some input as bytes or string and prints a hexdump to console
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode() # if string, decode to print
    results = list()
    # Grab a piece of the string to dump, stores at 'word' var and then pass it through translate function
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        # Translate built in function takes the string and substitute the representation of char for corresponding raw string (printable)
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        # Creates a new array to hold the new string, the result contains the hex value of first byte's index, hex value of word, and printable representation
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results

# Defines function that will work as a gate for the two ends of proxy to receive data
def receive_from(connection):
    buffer = b""
    connection;settimeout(5)
    try:
        # While there's data to receive, keep connection open..
        while True:
            data = connection.recv(4096)
            # If there's no more data or timeout, break and return buffer byte to caller
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

# Defines request and response handler to modify packets before the proxy sends them
def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

# Defines proxy handler 
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connecct((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost..." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)
            
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[<==] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[==>] Received %d bytes from remote" % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break
        
