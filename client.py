#connection
import socket

import sys
import time

port=8080

soc=socket.socket()
name=input("Enter username:")
host=input("Enter the hostname:")
soc.connect((host,port))
print("[+] Connected to COMPASS")

while 1:
    inp=soc.recv(1024)
    inp=inp.decode()
    print("[>] Server:",inp)
    message=input(">>")
    message=message.encode()
    soc.send(message)
    print("[+] Message sent!")