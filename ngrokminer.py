#!/usr/bin/env python3

from threading import Thread
from mcstatus import JavaServer
from colorama import Fore
from prettytable import PrettyTable
import minecraftinfo as mcinfo
import socket
import config
import signal

banner = Fore.GREEN+"""
███╗░░██╗░██████╗░██████╗░░█████╗░██╗░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░
████╗░██║██╔════╝░██╔══██╗██╔══██╗██║░██╔╝░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗
██╔██╗██║██║░░██╗░██████╔╝██║░░██║█████═╝░█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝
██║╚████║██║░░╚██╗██╔══██╗██║░░██║██╔═██╗░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗
██║░╚███║╚██████╔╝██║░░██║╚█████╔╝██║░╚██╗░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║
╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝ v0.1
"""+Fore.YELLOW+"""A tool for finding minecraft servers that use ngrok.

"""+Fore.RED+"""~ Author: """+Fore.GREEN+"""unix_xorg
"""+Fore.RED+"""~ GitHub: """+Fore.GREEN+"""https://github.com/unix-xorg
"""+Fore.RED+"""~ License: """+Fore.GREEN+"""BSD 3-Clause"""+Fore.WHITE+"""

+------------------["""+Fore.RED+"""!!!WARNING!!!"""+Fore.WHITE+"""]------------------+
|"""+Fore.GREEN+"""THE DEVELOPER IS NOT RESPONSIBLE FOR ANY MISUSE"""+Fore.WHITE+"""    |
|"""+Fore.GREEN+"""OR DAMAGE CAUSED BY THIS SCRIPT!!! THIS SCRIPT WAS"""+Fore.WHITE+""" |
|"""+Fore.GREEN+"""WRITTEN TO DEMONSTRATE VULNERABILITY."""+Fore.WHITE+"""              |
+---------------------------------------------------+
"""

print(banner)
input(Fore.CYAN+"\n[PRESS ENTER TO START]"+Fore.WHITE)

host = f"{config.first_count}.tcp.eu.ngrok.io"

# find and connect to a server
def brute_force(host):
    for port in range(10000, 20000):
        # retrieving information about the minecraft server
        def check_connection(host, port):
            try:
                con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                con.settimeout(config.connection_time)
                con.connect((host, port))
                con.close()
                
                server = JavaServer.lookup(f"{host}:{port}")
                table = PrettyTable()
                table.field_names = ("Server:", f"{host}:{port}")
                table.add_rows(
                    [
                        ["Ping:", f"{int(server.ping())} ms"],
                        ["Player(s) online:", f"{server.status().players.online}"],
                        ["Version:", mcinfo.mcje_server(host, port).version],
                    ]
                )

                print(table)
            except Exception:
                pass
                
        thread2 = Thread(target = check_connection, args = (host, port))
        thread2.start()

if (__name__ == "__main__"):
    brute_force(host)