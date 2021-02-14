#connection
import socket

import sys,select,os
import time
import signal
import random

#initialisation
port=int(sys.argv[1])

def sighandler(signum,frame):
    print(bcolors.fail+"\r[-] Ending Session"+bcolors.endc)
    sys.exit()

signal.signal(signal.SIGINT, sighandler)

#background colors
class bcolors:
    fail='\033[91m'
    green='\033[92m'
    yellow='\033[93m'
    blue='\033[94m'
    magenta='\u001b[95m'
    cyan='\033[96m'

    lfail='\033[31m'
    lgreen='\033[32m'
    lyellow='\033[33m'
    lblue='\033[34m'
    lmagenta='\u001b[35m'
    lcyan='\033[36m'

    bold='\033[1m'
    underline='\033[4m'
    endc='\033[0m'
class banners:
    banner=[]
    banner.append('''
              ____  ____  _   _  ___      _     ___   ___
             |     |    || \ / ||   |    / \   |     | 
             |     |    ||  -  ||___|   /===\   ---   ---
             |     |    ||     ||      |     |     |     |
              ====  ==== |     ||      |     |  ===   ===  ''')
    banner.append('''
                (                                      
                )\           )              )          
                (((_)   (     (     `  )   ( /(  (   (   
                )\___   )\    )\  ' /(/(   )(_)) )\  )\  
                ((/ __| ((_) _((_)) ((_)_\ ((_)_ ((_)((_) 
                | (__ / _ \| '  \()| '_ \)/ _` |(_-<(_-< 
                \___|\___/|_|_|_| | .__/ \__,_|/__//__/ 
                                    |_|      ''')
    banner.append('''
            ______     ______     __    __     ______   ______     ______     ______    
            /\  ___\   /\  __ \   /\ "-./  \   /\  == \ /\  __ \   /\  ___\   /\  ___\   
            \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  _-/ \ \  __ \  \ \___  \  \ \___  \  
            \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_\    \ \_\ \_\  \/\_____\  \/\_____\ 
            \/_____/   \/_____/   \/_/  \/_/   \/_/     \/_/\/_/   \/_____/   \/_____/''')
    banner.append('''
            ▄████▄   ▒█████   ███▄ ▄███▓ ██▓███   ▄▄▄        ██████   ██████ 
            ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓██░  ██▒▒████▄    ▒██    ▒ ▒██    ▒ 
            ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▓██░ ██▓▒▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   
            ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒██▄█▓▒ ▒░██▄▄▄▄██   ▒   ██▒  ▒   ██▒
            ▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒▒██▒ ░  ░ ▓█   ▓██▒▒██████▒▒▒██████▒▒
            ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░▒▓▒░ ░  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
            ░  ▒     ░ ▒ ▒░ ░  ░      ░░▒ ░       ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░
            ░        ░ ░ ░ ▒  ░      ░   ░░         ░   ▒   ░  ░  ░  ░  ░  ░  
            ░ ░          ░ ░         ░                  ░  ░      ░        ░  
            ░ ''')
    banner.append('''
            .oPYo.                                            
            8    8                                            
            8      .oPYo. ooYoYo. .oPYo. .oPYo. .oPYo. .oPYo. 
            8      8    8 8' 8  8 8    8 .oooo8 Yb..   Yb..   
            8    8 8    8 8  8  8 8    8 8    8   'Yb.   'Yb. 
            `YooP' `YooP' 8  8  8 8YooP' `YooP8 `YooP' `YooP' 
            :.....::.....:..:..:..8 ....::.....::.....::.....:
            ::::::::::::::::::::::8 ::::::::::::::::::::::::::
            ::::::::::::::::::::::..::::::::::::::::::::::::::
''')
    bannercol=[]
    bannercol.append(bcolors.yellow)
    bannercol.append(bcolors.fail)
    bannercol.append(bcolors.green)
    bannercol.append(bcolors.blue)
    bannercol.append(bcolors.cyan)

members={}
colors=['\033[92m','\033[93m','\033[94m','\033[95m','\033[96m','\033[31m','\033[32m','\033[33m','\033[34m','\033[35m','\033[36m']


def client():
    soc=socket.socket()
    os.system('clear')

    print(banners.bannercol[random.randrange(0,5)]+banners.banner[random.randrange(0,5)]+bcolors.endc)
    name=input(bcolors.bold+" -> Enter username: "+bcolors.endc)
    host=input(bcolors.bold+" -> Enter the hostname: "+bcolors.endc)
    soc.connect((host,port))
    print(bcolors.underline+"*** Connected to COMPASS server ***"+bcolors.endc)
    soc.send(name.encode())
    members["Me"]=colors[random.randrange(0,11)]

    sys.stdout.write(members["Me"]+'[Me :] '+ "\033[0m");sys.stdout.flush()
    while 1:

        readc,writec,exceptc=select.select([sys.stdin,soc],[],[])
        for conn in readc:
            if conn==soc:

                data=conn.recv(4096).decode()
                if data:
                    try:
                        endc=data.index(']')
                        owner=data[:(endc+1)]
                        if owner not in members:
                            members[owner]=colors[random.randrange(0,11)]
                        print_color=members[owner]
                        print("\r"+print_color+data+bcolors.endc)
                    except:
                        print("\r"+bcolors.cyan+data+bcolors.endc)
                    sys.stdout.write(members["Me"]+'[Me :] '+ "\033[0m");sys.stdout.flush()
                else:
                    print("\r"+bcolors.fail+"[-] Disconnected from server."+bcolors.endc)
                    print("\r"+bcolors.yellow+"[>] Quitting.....bye!!!"+bcolors.endc)
                    sys.exit()
            else:
                inp=input(members["Me"]+'[Me :] '+ "\033[0m")
                soc.send(inp.encode())

client()