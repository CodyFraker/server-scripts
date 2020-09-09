# BoothBayer & Cody Fraker
# Packages required: CODY fill me in pls
# this script uploads files to google drive

#imports
import socket
import sys
import time
from ssh2.session import Session

# Host Credentials
host = "HOSTNAME OR IP"
user = "USERNAME"
port = 22
password = "NO SSH KEYS ARE USED HERE"

# Initialize IPV4 Socket Stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initate connection
sock.connect((host, port))
session = Session()
session.handshake(sock)
session.userauth_password(user, password)
channel = session.open_session()
channel.pty() #THIS IS REQUIRED. I don't know why, but it fixed the issue of responses not coming in from the system.

# Execute command function
def Execute(command):
	print('UPLOADING - This may take some time')
	channel.execute("{0}\n".format(command))
	size = 1
	while size > 0:
		size, data = channel.read()
		print(data.decode())
	print(data.decode())

#Set parameters #my source info: https://www.howtogeek.com/451262/how-to-use-rclone-to-back-up-to-google-drive-on-linux/
rcloneLocation = "/usr/bin/rclone" #Location of rclone program
transfers = 30 #Sets number of files to copy in parallel
checkers = 8 #how many checkers to run in parallel. They monitor in progress transfers.
contimeout = 60 #Connection timeout
timeout = 300 #timeout for broken connections
retries = 3 #maximum amount of errors before restarting
llr = 10 #max amount of retries for one failing operating
uploadFiles = "/directory/to/files/" #folder to be backedup
uploadDestination = "remoteStorage:folderName" #location... I found that you need to use the format of remoteStorage:FOLDERNAME where remoteStorage is whatever you named your rclone thing, and if I didn't specify :FOLDER it would just make a folder in the directory I ran this rather than on the google drive.

#----Build-then-Execute----
executeString = "{0} copy --verbose --update --transfers {1} --checkers {2} --contimeout {3}s --timeout {4}s --retries {5} --low-level-retries {6} '{7}' '{8}'".format(rcloneLocation, transfers, checkers, contimeout, timeout, retries, llr, uploadFiles, uploadDestination)

Execute(executeString)

# Close connection
channel.close()
print("Rclone Upload")
