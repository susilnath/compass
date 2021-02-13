import sys
import select
import time

#connection
import socket
import pickle #to serialise data

#initialize
port=8080
soc_list_input=[]
soc_list_output=[]
msg_queue={}
alive={}
data={}

rel_soc=0

#binding
def server():
    soc=socket.socket()
    soc.setblocking(0)
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,4096)
    host=socket.gethostname()
    print("[+] Server will start on host: "+host)

    soc.bind((host,port))
    print("[+] Socket binded sucessfully")
    print("[-] Waiting for connections...")

    soc.listen(10)
    soc_list_input.append(soc)

    global rel_soc
    #incoming connection
    while soc_list_input:

        readc,writec,exceptc=select.select(soc_list_input,soc_list_output,soc_list_input)

        for conn in readc:
            if conn is soc:
                connection,address=soc.accept()
                print("[*] Connection made from ",address)
                soc_list_input.append(connection)
                connection.setblocking(0)
                name=connection.recv(1024).decode()
                if name not in alive:
                    alive[name]=connection
                    data[name]=''
                    print("[+] "+name+" joined")
                    for i in alive.keys():
                        if i==name:
                            connection.send(str("ME and you are alive").encode())
                            continue
                        connection.send(str(i+", ").encode())

            elif conn == rel_soc:
                rel_data_rec=conn.recv(4096)
                sync(conn,1,rel_data_rec)

            else:
                conn_name=list(alive.keys())[list(alive.values()).index(conn)]
                data_rec=conn.recv(4096).decode()
                if data_rec:
                    print(">>> "+conn_name+" : "+data_rec)

                    #commands
                    rel_soc=con_relay_temp()

                    data[conn_name]=str(data[conn_name])+str(data_rec)
                    soc_list_output.append(conn)
                else:
                    soc_list_input.remove(conn) #close socket if no data is read
                    alive.pop(conn_name)
                    data.pop(conn_name)
                    print("[-] Closed connection!")

        for conn in writec:
            conn_name=list(alive.keys())[list(alive.values()).index(conn)]#find the name from connection

            to_send=data[conn_name]
            broadcast(conn,to_send,conn_name)

        continue


def broadcast(conn,to_send,owner):
    for name in alive:
        if alive[name]==conn:
            continue
        else:
            send_conn=alive[name]
            send_conn.send(str("["+owner+" :] "+to_send).encode())
    sync(rel_soc,2)
    data[owner]=''
    soc_list_output.remove(conn)

def con_relay():
    relay_addr="hades"
    relay_port=8081
    sock=socket.socket()
    sock.connect((relay_addr,relay_port))

    print("[#] Connected to relay - "+relay_addr+" : "+str(relay_port))
    soc_list_input.append(sock)

    return sock

def serialise(syn_alive,syn_data):
    ser_alive=pickle.dumps(syn_alive)
    ser_data=pickle.dumps(data)

    alive_length=str(sys.getsizeof(ser_alive)).rjust(4,'0')
    alive_length=alive_length.encode()

    return alive_length+ser_alive+ser_data

def unserialise(rec_data):
    alive_len=int(rec_data[:4].decode())
    ser_alive=rec_data[4:][:alive_len]
    ser_data=rec_data[alive_len:]

    unser_alive=pickle.loads(ser_alive)
    unser_data=pickle.loads(ser_data)

    return unser_alive,unser_data

def sync(sock,mode,rel_data=0):
    #sync alive and data dicts across servers
    if mode==1:#receive
        print("[#] Received from relay!")
        print(rel_data)
        #rel_alive,rel_data=unserialise(rel_data)
        #print(rel_alive)
        #print(rel_data)
    
    if mode==2:#send
        ser_send=serialise(list(alive.keys()),data)
        sock.send(ser_send)
        print("[#] Sent to relay successfully!")

def con_relay_temp():
    global a
    if a==1:
        sock=con_relay()
        a=0
        return sock
    else:
        return rel_soc
a=1
server()