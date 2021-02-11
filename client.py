#connection
import socket

import sys,select,os
import time
import signal
import random

#initialisation
port=8080

def sighandler(signum,frame):
    print(bcolors.fail+"\r[-] Ending Session"+bcolors.endc)
    sys.exit()

signal.signal(signal.SIGINT, sighandler)

#background colors
class bcolors:
    blue='\033[94m'
    cyan='\033[96m'
    green='\033[92m'
    warning='\033[93m'
    fail='\033[91m'
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
    bannercol.append(bcolors.warning)
    bannercol.append(bcolors.fail)
    bannercol.append(bcolors.green)
    bannercol.append(bcolors.blue)
    bannercol.append(bcolors.cyan)

def client():
    soc=socket.socket()
    os.system('clear')

    print(banners.bannercol[random.randrange(0,5)]+banners.banner[random.randrange(0,5)]+bcolors.endc)
    name=input(bcolors.bold+" -> Enter username: "+bcolors.endc)
    host=input(bcolors.bold+" -> Enter the hostname: "+bcolors.endc)
    soc.connect((host,port))
    print(bcolors.underline+"[+] Connected to COMPASS"+bcolors.endc)
    soc.send(name.encode())

    sys.stdout.write("\033[34m"+'[Me :] '+ "\033[0m");sys.stdout.flush()
    while 1:

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
            else:
                inp=input("\033[34m"+'[Me :] '+ "\033[0m")
                soc.send(inp.encode())

client()