# Cody Fraker
# Packages required: ssh2-python
# this script ensures that the grafana docker image is up to date.

import socket
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
Execute("docker pull grafana")
print("Pulling latest grafana image")
Execute("docker stop grafana")
print("Stopping local grafana container")
Execute("docker rm {IMAGE ID}")
print("Removed old grafana iamges")

print("Starting updated grafana container")
Execute("docker run --name grafana -d -p 1234:1234 --network=host grafana/grafana")

# Close connection
channel.close()
print("Removed old grafana iamges")


