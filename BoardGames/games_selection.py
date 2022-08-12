#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
import os
import Awele.players_selection, Chess.players_selection, Othello.players_selection, Puissance4.players_selection, Squadro.players_selection
dirname = os.path.dirname(__file__)


##################################################################################################
##################                      SELECTION DES JEUX                      ##################
##################################################################################################
def selection():
    pygame.init()
    from button import Button

    #games = [f for f in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, f)) and not f.startswith('_')]
    #games.pop(0) # No Awele
    games = ['Chess', 'Othello', 'Puissance4', 'Squadro']

    WIDTH = 700
    HEIGHT = (len(games)//2 + len(games)%2) * 120
    OFFSET_X = 250
    OFFSET_Y = 100

    buttons = []
    for i, game in enumerate(games):
        x = 100 + ((i%2) * OFFSET_X)
        y = 35 + ((i//2) * OFFSET_Y)
        buttons.append(Button(x, y, game))

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Board Games")
    while True:
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)

        for button in buttons:
            if button.draw_button(WIN):
                if button.text == 'Awele':
                    Awele.players_selection.selection()
                elif button.text == 'Chess':
                    Chess.players_selection.selection()
                elif button.text == 'Othello':
                    Othello.players_selection.selection()
                elif button.text == 'Puissance4':
                    Puissance4.players_selection.selection()
                elif button.text == 'Squadro':
                    Squadro.players_selection.selection()
                WIN = pygame.display.set_mode((WIDTH, HEIGHT))
                pygame.display.set_caption("Board Games")

        pygame.display.update()
