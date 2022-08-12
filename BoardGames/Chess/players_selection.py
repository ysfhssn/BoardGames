#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
from Chess.Joueurs import joueur_humain, MASTER, MCTS
import game
if not game.GUI:
    print("GUI mode is off.")
    sys.exit(1)
import pygame
from Chess.main import main


##################################################################################################
##################                      SELECTION DES JOUEURS                   ##################
##################################################################################################
def selection():
    pygame.init()
    from button import Button

    ##############################################################################################
    buttons = [
        Button(100, 50, "Human v Human", (joueur_humain, joueur_humain)),
        Button(350, 50, "Human v AB", (joueur_humain, MASTER)),
        Button(100, 150, "AB v Human", (MASTER, joueur_humain)),
        Button(350, 150, "Human v MCTS", (joueur_humain, MCTS)),
        Button(100, 250, "MCTS v Human", (MCTS, joueur_humain)),
        Button(350, 250, "MCTS v AB", (MCTS, MASTER)),
        Button(100, 350, "AB v MCTS", (MASTER, MCTS)),
        Button(350, 350, "AB v AB", (MASTER, MASTER)),
        Button(100, 450, "MCTS v MCTS", (MCTS, MCTS))
    ]
    ###############################################################################################

    WIDTH = 700
    HEIGHT = (len(buttons)//2 + len(buttons)%2) * 110

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    while True:
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

        for button in buttons:
            if button.draw_button(WIN):
                game.joueur1 = button.modules[0]
                game.joueur2 = button.modules[1]
                main()
                WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Chess")

        pygame.display.update()


if __name__ == "__main__":
	selection()
