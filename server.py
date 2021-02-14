import sys
import select
import time

#connection
import socket
import pickle #to serialise data

#initialize
port=int(sys.argv[1])
soc_list_input=[]
soc_list_output=[]
msg_queue={}
alive={}
data={}
dup_relay=[]
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
                    data[name]=[]
                    print("[+] "+name+" joined")
                    for i in alive.keys():
                        if i==name:
                            connection.send(str("ME and you are alive").encode())
                            continue
                        connection.send(str(i+", ").encode())

            elif conn == rel_soc:
                rel_data_rec=conn.recv(4096)
                try:
                    sync(conn,1,rel_data_rec)
                except Exception:
                    print("[-] Raised Exception")

            else:
                conn_name=list(alive.keys())[list(alive.values()).index(conn)]
                data_rec=conn.recv(4096).decode()
                if data_rec:
                    print(">>> "+conn_name+" : "+data_rec)

                    #rel_soc=con_relay_temp()
                    try:
                        if '_relay_chain' in data_rec[:13]:
                        
                            info=data_rec.split()
                            rel_soc.send(str("_relay_chain "+info[1]+" "+info[2]).encode())
                            continue

                        if '_relay_control' in data_rec[:15]:
                            info=data_rec.split()
                            rel_soc.send(data_rec.encode())
                            continue

                        if '_relay' in data_rec[:7]:
                            info=data_rec.split()
                            rel_soc=con_relay(info[1],info[2])
                            sync(rel_soc,2)
                            continue

                    except:
                        print("[-] Command incomplete")


                    data[conn_name].append(data_rec)
                    soc_list_output.append(conn)
                else:
                    soc_list_input.remove(conn) #close socket if no data is read
                    alive.pop(conn_name)
                    data.pop(conn_name)
                    print("[-] Closed connection!")

        for conn in writec:
            conn_name=list(alive.keys())[list(alive.values()).index(conn)]#find the name from connection

            broadcast(conn)
            soc_list_output.remove(conn)

        continue

def dict_dup(alive_dict):
    rev_alive={}
    dup_names=[]

    for key,values in alive_dict.items():
        if values not in rev_alive:
            rev_alive[values]=1
        else:
            dup_names.append(key)
    return dup_names

def broadcast(conn):
    if conn != rel_soc and rel_soc != 0:
        sync(rel_soc,2)
    for name,msg_list in data.items():
        if not msg_list:
            continue
        else:
            for send_name,send_conn in alive.items():
                if name==send_name:
                    continue
                if send_conn==rel_soc:
                    continue
                else:
                    for to_send in msg_list:
                        send_conn.send(str("["+name+" :] "+to_send).encode())
            data[name]=[]



def con_relay(host,rport):
    if host!=0 and port!=0:
        relay_addr=host
        relay_port=int(rport)
    else:
        print("[-] Wrong host/port")
        return 0
    sock=socket.socket()
    sock.connect((relay_addr,relay_port))

    print("[#] Connected to relay - "+relay_addr+" : "+str(relay_port))
    soc_list_input.append(sock)

    return sock

def serialise(syn_alive,syn_data):
    ser_alive=pickle.dumps(syn_alive)
    ser_data=pickle.dumps(data)

    alive_length=str(len(ser_alive)).rjust(4,'0')
    alive_length=alive_length.encode()

    return alive_length+ser_alive+ser_data

def unserialise(rec_data):
    alive_len=int(rec_data[:4].decode())
    ser_alive=rec_data[4:][:alive_len]
    ser_data=rec_data[4+alive_len:]

    unser_alive=pickle.loads(ser_alive)
    unser_data=pickle.loads(ser_data)

    return unser_alive,unser_data

def sync(sock,mode,rel_data=0):
    #sync alive and data dicts across servers
    if mode==1:#receive
        print("[#] Received from relay!")
        rel_alive,rel_data=unserialise(rel_data)
        for i in rel_alive:
            if i in alive:
                continue
            alive[i]=sock
        dup_relay=dict_dup(alive)
        for name,value in rel_data.items():
            if name not in data:
                data[name]=value
                continue
            data[name].extend(value)
        soc_list_output.append(sock)


    if mode==2:#send
        ser_send=serialise(list(alive.keys()),data)
        sock.send(ser_send)
        print("[#] Sent to relay successfully!")

server()