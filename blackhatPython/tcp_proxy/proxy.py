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
# Set connection to remote host
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connecct((remote_host, remote_port))
    
    # Check if it's necessary to initiate connection and request data before the main loop 
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    # Get receive_from response and pass it through response_handler function, then send received buffer to local client.
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost..." % len(remote_buffer))
        client_socket.send(remote_buffer)

    # Enters main loop, to read, proccess and send data to remote client..
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)
            
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[<==] Sent to remote.")
        
        # Read, process and send data back to local client
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[==>] Received %d bytes from remote" % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        # If no more data, close connection on both ends.
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break
        
# Server loop: set up and manage the connection
# It starts creating a socket, binding to local host and starts to listen
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    # If error, print:
    except Exception as e:
        print('[!!] Problem on bind: %r' % e)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening socket or correct permissions")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    
    # Pass new connections request to proxy_handler in a new thread
    while True:
        client_socket, addr = server.accept()
        # Print local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # Start thread to talk to remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

# Main function
def main():
    # Prints usage syntax to user
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit()
    # Receive arguments and starts listening loop for connections
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]
    
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()