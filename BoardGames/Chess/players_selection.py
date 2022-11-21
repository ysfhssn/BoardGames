#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
from Chess.Players import human, master, mcts, sfish
import game
if not game.GUI:
    print("GUI mode is off.")
    sys.exit(1)
import pygame
from Chess.main import main


def selection():
    pygame.init()
    from button import Button

    ##############################################################################################
    buttons = [
        Button(100, 50, "Human v Human", (human, human)),
        Button(350, 50, "Human v AB", (human, master)),
        Button(100, 150, "AB v Human", (master, human)),
        Button(350, 150, "Human v sfish", (human, sfish)),
        Button(100, 250, "sfish v Human", (sfish, human)),
        Button(350, 250, "AB v AB", (master, master)),
        Button(100, 350, "sfish v sfish", (sfish, sfish)),
        Button(350, 350, "AB v sfish", (master, sfish)),
        Button(100, 450, "sfish v AB", (sfish, master)),
        Button(350, 450, "AB v mcts", (master, mcts)),
        Button(100, 550, "mcts v AB", (mcts, master)),
        Button(350, 550, "mcts v sfish", (mcts, sfish)),
        Button(100, 650, "sfish v mcts", (sfish, mcts)),
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
                game.player1 = button.modules[0]
                game.player2 = button.modules[1]
                main()
                WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Chess")

        pygame.display.update()


if __name__ == "__main__":
	selection()
