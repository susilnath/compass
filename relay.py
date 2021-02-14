#start of relay branch in git

import select
import os,sys

import socket

rel_name="hades"
rel_port=0
port=int(sys.argv[1])
members=[]
relays=[]

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
        
        print(members)
        print(relays)

        for conn in readc:
            if conn==sock:
                connection,address=conn.accept()
                members.append(connection)
                connection.setblocking(0)
                print("[+] Adding "+str(address)+" to relay node")
            else:
                data=conn.recv(4096)
                if data:
                    print(data)
                    try:
                        if "_relay_chain" in data.decode()[:13]:
                            info=data.decode().split()

                            rel_sock=relay_chain(info[1],info[2])
                            members.append(rel_sock)
                            relays.append(rel_sock)
                            print("[+] Connected to another relay")
                            continue

                        if "_relay_control" in data.decode()[:15]:
                            info=data.decode().split()
                            print(info)
                            
                            if len(info)>3:
                                sock_num=int(info[1])
                                to_send=''
                                for i in range(len(info)):
                                    if i==0 or i==1:
                                        continue
                                    print(i)
                                    print(to_send)
                                    to_send=to_send+info[i]+" "
                                print(relays)
                                relays[sock_num].send(to_send.encode())

                    except BaseException as exc:
                        print(exc)
                        print("[+] No command sent!, broadcasting...")
                        broadcast(sock,conn,data) 
                        continue
                else:
                    members.remove(conn)
                    print("[+] A server disconnected!")
                    print(conn)

def broadcast(sock,conn,to_send):
    for i in members:
        if conn==i:
            continue
        if i==sock:
            continue
        i.send(to_send)

def relay_chain(host,rport):
    if host!=0 and rport !=0:
        rel_name=host
        rel_port=int(rport)
    else:
        print("[-] Wrong host/port")
        return 0
    print("[+] Connecting to relay - "+rel_name+" : "+str(rel_port))
    sock=socket.socket()
    sock.connect((rel_name,rel_port))
    return sock
server()

