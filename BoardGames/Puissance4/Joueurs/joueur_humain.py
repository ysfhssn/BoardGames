#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(grandparent)
import game
if game.GUI: import pygame

def saisieCoup(jeu):
    col = None

    if not game.GUI:
        print("Coups valides: ", game.getCoupsValides(jeu))

        col = int(input("Votre colonne: "))

        while col not in game.getCoupsValides(jeu):
            col = int(input("Coup invalide !\nVotre colonne: "))

        return col

    else:
        SIZE = game.game.SIZE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    col = x//SIZE
                if col in game.getCoupsValides(jeu):
                    return col
