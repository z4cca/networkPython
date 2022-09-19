# Import required libraries
import socket
import threading
from queue import Queue

# Define target and port
target = "192.168.0.1"
# Creates an empty list for scanned ports
queue = Queue()
open_ports = []


# Define connection function
def portscan(port):
    try:
        # Creates connection socket ipv4, TCP and connects to the target
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

# Set function to fill queue for multithreading
def fill_queue(port_list):
    for port in port_list:
        queue.put(port)

# Set worker method for threads use
def worker():
    # while queue not over, scan and print open ports
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print(f"Port {(port)} is open.")
            open_ports.append(port)

# Fill queue with port list range
port_list = range(1,1024)
fill_queue(port_list)

# Creates thread list empty
thread_list = []

# Set threads quantity to increase scan speed
for t in range(500):
    # Pass x threads with worker function (without calling), append open ports to thread list
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# Run thread list
for thread in thread_list:
    thread.start()

# Wait for all threads are done and print 
for thread in thread_list:
    thread.join()

print(f"Open ports are: {(open_ports)}")