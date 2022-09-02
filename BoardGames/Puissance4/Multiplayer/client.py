#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(parent)
sys.path.append(grandparent)

import game
import puissance4
if game.GUI: import pygame
import Puissance4.Players.human
import socket, pickle


game.game = puissance4
game.player1 = Puissance4.Players.human
game.player2 = Puissance4.Players.human


client = socket.socket()
try: client.connect(("<SERVER_IP_ADDR>", 2000))
except socket.error as e: print(str(e))

data = client.recv(2048)
PLAYER = int(data.decode())
print(f"PLAYER {PLAYER}")
client.send(data)

data = client.recv(2048)
game_info = pickle.loads(data)
game.game.draw_board(game_info) if game.GUI else game.print_game(game_info)

client.setblocking(0)

while not game.is_game_over(game_info):
    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    if game_info[1] == PLAYER:
        move = game.get_move(game_info)
        game.play_move(game_info, move)
        client.send(pickle.dumps(game_info))
    else:
        try:
            data = client.recv(2048)
            game_info = pickle.loads(data)
            print("The opponent has played")
        except: pass
    game.game.draw_board(game_info) if game.GUI else game.print_game(game_info)

client.close()
