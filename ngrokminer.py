#!/usr/bin/env python3

import threading
from threading import Thread
from mcstatus import JavaServer
from colorama import Fore
from prettytable import PrettyTable
import minecraftinfo as mcinfo
import socket
import config
import signal
import json


class Counter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

    def decrement(self):
        with self.lock:
            self.count -= 1

    def get_count(self):
        with self.lock:
            return self.count

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
    counter = Counter()
    fails = Counter()

    for port in range(10000, 20000):
        # retrieving information about the minecraft server
        def check_connection(host, port, counter, fails):
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
                        ["Version:", server.status().version.name],
                        ["MOTD:", server.status().motd.to_plain()],
                    ]
                )

                print(table)
                counter.increment()
            except Exception:
                fails.increment()

        last_thread = Thread(target = check_connection, args = (host, port, counter, fails))
        last_thread.start()
    
    while not threading.active_count() == 1:
        pass
    print("Done! Found {} hosts, failed {} times.".format(counter.get_count(), fails.get_count()))

if (__name__ == "__main__"):
    brute_force(host)