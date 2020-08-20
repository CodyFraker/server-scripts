# Cody Fraker
# Packages required: ssh2-python
# this script ensures that the grafana docker image is up to date.

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

# Navigate to a local repository on a node
channel.write("cd /etc/Proj2/")

# Checkout if there are updates to the master branch on remote
channel.write("git remote show origin\n")
data = channel.read()
# if there are updates to the master branch, pull latest changes.
if "local out of date" in data.decode():
    channel.write("git checkout master\n")
    channe.write("git pull\n")
    # give git a chance to pull the full image before running next command
    time.sleep(10)
    # Run updated script after the new version was pulled.
    channel.write("sh script1.sh")
else:
    print("Branch is up to date")

# Close connection
channel.close()