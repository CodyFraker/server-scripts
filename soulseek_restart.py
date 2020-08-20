# Cody Fraker
# Packages required: ssh2-python
# this script restarts the soulseek docker container.

import socket
import time
from ssh2.session import Session

# Host Credentials
host = "HOSTNAME OR IP"
user = "USERNAME"
port = 22
password = "NO SSH KEYS ARE USED HERE"

# Intialize IPV4 socket stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initate connection
sock.connect((host, port))
session = Session()
session.handshake(sock)
session.userauth_password(user, password)
channel = session.open_session()
channel.shell()

# Execute command function
def Execute(command):
    channel.write(command + "\n")
    data = channel.read()
    print(data.decode())


# Check for docker container, if no container exists this script will fail.
Execute("docker container ls | grep Soulseek")

# tell docker to restart Soulseek
Execute("docker container restart Soulseek")

# Give docker engine time to restart the container
time.sleep(5)

# Close connection
channel.close()
print("Restarted Soulseek")


