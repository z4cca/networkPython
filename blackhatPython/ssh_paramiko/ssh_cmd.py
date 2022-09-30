# Import required libraries
import paramiko
import getpass

# ssh_command makes a connection to server and runs a single command
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    # If connection is made, print each line of command output
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('---Output---')
        for line in output:
            print(line.strip())
            
# Getpass explicitly asks user for username and password(not displayed)
if __name__ == '__main__':
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()
    # Get server infos and send to be executed
    ip = input('Server IP: ') or '127.0.0.1'
    port = input('Enter port or <CR>: ') or 6666
    cmd = input('Cmd or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)
