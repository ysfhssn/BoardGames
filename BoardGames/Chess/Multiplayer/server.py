#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(parent)
sys.path.append(grandparent)
sys.path.append(os.path.join(parent, 'Joueurs'))
import game
game.GUI = False
import chess
game.game = chess
import socket, pickle
from _thread import *


server = socket.socket()
IP_ADDR = socket.gethostbyname(socket.gethostname())
print("IP_ADDR: " + IP_ADDR)
server.bind((IP_ADDR, 2000))
server.listen(2)

clients=[]
jeu = game.initialiseJeu()

def client_thread(conn):
    global jeu
    player = b"1" if len(clients)%2 == 1 else b"2"
    conn.send(player)
    print("\tPLAYER " + conn.recv(8).decode())
    conn.send(pickle.dumps(jeu))
    while True:
        try:
            data = conn.recv(2048)
            jeu = pickle.loads(data)
            if jeu:
                broadcast(pickle.dumps(jeu), conn)
            else:
                disconnect_client(conn)
                break
        except:
            disconnect_client(conn)
            break

def broadcast(jeu, client):
    for c in clients:
        if c != client:
            try: c.send(jeu)
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
