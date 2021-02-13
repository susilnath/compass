#start of relay branch in git

import select
import os

import socket

port=8081
members=[]

def server():
    sock=socket.socket()
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    host=socket.gethostname()

    sock.bind((host,port))
    print("[+] Server will start on host: "+host)

    sock.listen(10)
    members.append(sock)

    while 1:
        readc,writec,exceptc=select.select(members,[],[])
        
        for conn in readc:
            if conn==sock:
                connection,address=conn.accept()
                members.append(connection)
                connection.setblocking(0)
                print("[+] Adding "+str(address)+" to relay node")
            else:
                data=conn.recv(1024)
                if data:
                    broadcast(sock,conn,data) 
                else:
                    members.remove(conn)
                    print("[+] Server Disconnected!")

def broadcast(sock,conn,to_send):
    for i in members:
        if conn==i:
            continue
        if i==sock:
            continue
        i.send(to_send)

server()

