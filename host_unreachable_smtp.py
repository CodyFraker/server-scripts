# Cody Fraker
# Packages required: ssh2-python
# this script will send an email if a desire host is unreachable

import socket
from ssh2.session import Session
import smtplib
from email.mime.text import MIMEText

# Email Options
emailAddr = 'myadminemail@gmail.com'
# Gmail SSL port
port = 465
emailMsg = MIMEText('Failed to reach destination')
emailMsg['Subject'] = "Failed to reach host"
emailMsg['From'], emailMsg['To'] = emailAddr

# SSH Host Credentials
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

# Execute command, limit numner of packets to X.
channel.execute("ping 192.168.1.222 -c 5")

size, data = channel.read()

while size > 0:
    if "Destination Host Unreachable" in data.decode():
        print("Host unreachable")
        SendEmail()
        break
    else:
        print("Host reachable")
    size, data = channel.read()

def SendEmail():
    with smtplib.SMTP("smtp.gmail.com", port) as server:
        server.login(emailAddr, "passwordGoesHere")
        server.sendmail(emailAddr, emailAddr, emailMsg)
        print("Sent email notification")

# Close connection
channel.close()
print("Connection closed.")