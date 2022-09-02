#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(parent)
sys.path.append(grandparent)
sys.path.append(os.path.join(parent, 'Players'))
import game
game.GUI = False
import puissance4
game.game = puissance4
import socket, pickle
from _thread import *


server = socket.socket()
IP_ADDR = socket.gethostbyname(socket.gethostname())
print("IP_ADDR: " + IP_ADDR)
server.bind((IP_ADDR, 2000))
server.listen(2)

clients=[]
game_info = game.init()

def client_thread(conn):
    global game_info
    player = b"1" if len(clients)%2 == 1 else b"2"
    conn.send(player)
    print("\tPLAYER " + conn.recv(8).decode())
    conn.send(pickle.dumps(game_info))
    while True:
        try:
            data = conn.recv(2048)
            game_info = pickle.loads(data)
            if game_info:
                broadcast(pickle.dumps(game_info), conn)
            else:
                disconnect_client(conn)
                break
        except:
            disconnect_client(conn)
            break

def broadcast(game_info, client):
    for c in clients:
        if c != client:
            try: c.send(game_info)
            except: disconnect_client(c)

def disconnect_client(client):
    print(str(client.getpeername()) + " disconnected")
    client.close()
    if client in clients:
        clients.remove(client)

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(str(conn.getpeername()) + " connected")
    start_new_thread(client_thread,(conn, ))

conn.close()
server.close()
