# Cody Fraker
# Packages required: ssh2-python
# this script cleans up the Soulseek downloads folder.

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

# Execute command function
def Execute(command):
    channel.execute(command)
    size, data = channel.read()
    print(data.decode())


# Delete the files on disk2. Its possible that these files could go to another disk in the array but ideally this script is ran on a daily basis to prevent this.
Execute("rm -r /mnt/disk2/appdata/soulseek/Downloads/complete/*")

# Close connection
channel.close()
print("Cleaned up Downloads folder.")