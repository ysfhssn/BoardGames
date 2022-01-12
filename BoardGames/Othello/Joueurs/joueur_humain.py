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
    """ jeu -> coup
        Retourne un coup a jouer
    """
    l = None
    c = None
    if not game.GUI:
        print("Coups valides: ", game.getCoupsValides(jeu))
        l = int(input("Votre ligne: "))
        c = int(input("Votre colonne: "))
        while (l, c) not in game.getCoupsValides(jeu):
            print("Coup invalide !")
            l = int(input("Votre ligne: "))
            c = int(input("Votre colonne: "))
        return (l, c)

    else:
        SIZE = game.game.SIZE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    l, c = y//SIZE, x//SIZE
                if (l, c) in game.getCoupsValides(jeu):
                    return (l, c)