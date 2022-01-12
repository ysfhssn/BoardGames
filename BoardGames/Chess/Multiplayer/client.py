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
import chess
if game.GUI: import pygame
import joueur_humain
import socket, pickle


game.game = chess
game.joueur1 = joueur_humain
game.joueur2 = joueur_humain


client = socket.socket()
try: client.connect(("<SERVER_IP_ADDR>", 2000))
except socket.error as e: print(str(e))

data = client.recv(2048)
PLAYER = int(data.decode())
print(f"PLAYER {PLAYER}")
client.send(data)

data = client.recv(2048)
jeu = pickle.loads(data)
game.game.draw_board(jeu) if game.GUI else game.affiche(jeu)

client.setblocking(0)

while not game.finJeu(jeu):
    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    if jeu[1] == PLAYER:
        coup = game.saisieCoup(jeu)
        game.joueCoup(jeu, coup)
        client.send(pickle.dumps(jeu))
    else:
        try:
            data = client.recv(2048)
            jeu = pickle.loads(data)
            print("The opponent has played")
        except: pass
    game.game.draw_board(jeu) if game.GUI else game.affiche(jeu)

client.close()