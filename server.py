import sys

#connection
import socket

import time

port=8080
soc_list=[]
#initialize


#binding
def server():
    soc=socket.socket()
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    host=socket.gethostname()
    print("[+] Server will start on host: "+host)

    soc.bind((host,port))
    print("[+] Socket binded sucessfully")
    print("[-] Waiting for connections...")

    soc.listen(10)
    soc_list.append(soc)
    #incoming connection
    connection,address=soc.accept()
    print("[*] Connection made from ",address)

    while 1:
        inp=input(">>")
        inp=inp.encode()
        connection.send(inp)
        print("[+] Message sent!")

        received=connection.recv(1024)
        received=received.decode()
        print("[+] Received: "+received)
