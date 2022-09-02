#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
from Othello.Players import human, master, mcts
import game
if not game.GUI:
    print("GUI mode is off.")
    sys.exit(1)
import pygame
from Othello.main import main


##################################################################################################
##################                      SELECTION DES JOUEURS                   ##################
##################################################################################################
def selection():
    pygame.init()
    from button import Button

    ##############################################################################################
    buttons = [
        Button(100, 50, "Human v Human", (human, human)),
        Button(350, 50, "Human v AB", (human, master)),
        Button(100, 150, "AB v Human", (master, human)),
        Button(350, 150, "Human v mcts", (human, mcts)),
        Button(100, 250, "mcts v Human", (mcts, human)),
        Button(350, 250, "mcts v AB", (mcts, master)),
        Button(100, 350, "AB v mcts", (master, mcts)),
        Button(350, 350, "AB v AB", (master, master)),
        Button(100, 450, "mcts v mcts", (mcts, mcts))
    ]
    ###############################################################################################

    WIDTH = 700
    HEIGHT = (len(buttons)//2 + len(buttons)%2) * 110

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")
    while True:
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        for button in buttons:
            if button.draw_button(WIN):
                game.player1 = button.modules[0]
                game.player2 = button.modules[1]
                main.main()
                WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Othello")

        pygame.display.update()


if __name__ == "__main__":
    selection()
