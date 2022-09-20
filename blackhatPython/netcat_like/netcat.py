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
    # If --listen is inserted as argument, starts NetCat object with an empty buffer otherwise send stdin buffer content
    if  args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    # Set netcat run
    nc = NetCat(args, buffer.encode())
    nc.run()

