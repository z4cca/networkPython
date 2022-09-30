# Import required libraries
import os
import paramiko
import socket
import sys
import threading

# Creates authentication with SSH_Key included in Paramiko demo files
CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

# Set SSH configurations for clients authentication
class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'sessions':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'user') and (password == 'pass123'):
            return paramiko.AUTH_SUCCESSFUL

# Defines main function with server IP and Port
if __name__ == '__main__':
    server = '127.0.0.1'
    ssh_port = 'Insert Port here'

    # Creates a socket listening for new client connections, print return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[*] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[*] Listening failed: ' + str(e))
        sys.exit(1)
    else:
        print('[*] Connection acceepted from ', client, addr)
    
    # Configure authentication methods
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)
    chan  = bhSession.accept(20)
    if chan is None:
        print('*** No channel.')
        sys.exit(1)

    # If Client authenticates, take commands and send through connection returning output
    print('[*] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcome! (by bhPython)')
    try:
        while True:
            command = input('[~] $:  ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('Exiting...')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
