#connection
import socket

import sys,select
import time

port=8080

class bcolors:
    blue='\033[94m'
    cyan='\033[96m'
    green='\033[92m'
    warning='\033[93m'
    fail='\033[91m'
    endc='\033[0m'
soc=socket.socket()
name=input("Enter username:")
host=input("Enter the hostname:")
soc.connect((host,port))
print("[+] Connected to COMPASS")
soc.send(name.encode())

sys.stdout.write("\n$ ");sys.stdout.flush()
while 1:
    # inp=soc.recv(1024)
    # inp=inp.decode()
    # print("[>] Server:",inp)

    # message=input(">>")
    # message=message.encode()
    # soc.send(message)
    # print("[+] Message sent!")
    # rec=soc.recv(1024)
    # if rec:
    #     print(rec.decode())
    #     print('\n')

    readc,writec,exceptc=select.select([sys.stdin,soc],[],[])
    for conn in readc:
        if conn==soc:

            data=conn.recv(1024).decode()
            if data:
                print("\r"+bcolors.cyan+data+bcolors.endc)
                sys.stdout.write("\033[34m"+'[Me :] '+ "\033[0m");sys.stdout.flush()
            else:
                time.sleep(1)
                continue
                #sys.exit("[-] Disconnected")
        else:
            inp=input("\033[34m"+'[Me :] '+ "\033[0m")
            soc.send(inp.encode())
            #sys.stdout.write("\033[34m"+'\n[Me :] '+ "\033[0m");sys.stdout.flush()
        