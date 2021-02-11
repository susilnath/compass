import sys
import select
import time

#connection
import socket

#initialize
port=8080
soc_list_input=[]
soc_list_output=[]
msg_queue={}
alive={}
data={}

#binding
def server():
    soc=socket.socket()
    soc.setblocking(0)
    soc.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    host=socket.gethostname()
    print("[+] Server will start on host: "+host)

    soc.bind((host,port))
    print("[+] Socket binded sucessfully")
    print("[-] Waiting for connections...")

    soc.listen(10)
    soc_list_input.append(soc)

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

            else:
                conn_name=list(alive.keys())[list(alive.values()).index(conn)]
                data_rec=conn.recv(4096).decode()
                if data_rec:
                    print(">>> "+conn_name+" : "+data_rec)
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
    data[owner]=''
    soc_list_output.remove(conn)



server()