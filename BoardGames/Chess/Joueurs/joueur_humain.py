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
        Retourne un coup a jouer (int, int, int, int)
    """
    i = None
    j = None
    di = None
    dj = None

    if not game.GUI:
        print("Coups valides: ", game.getCoupsValides(jeu))
        i = int(input("Votre ligne: "))
        j = int(input("Votre colonne: "))
        di = int(input("Votre ligne de deplacement: "))
        dj = int(input("Votre colonne de deplacement: "))
        while (i, j, di, dj) not in game.getCoupsValides(jeu):
            print("Coup invalide !")
            i = int(input("Votre ligne: "))
            j = int(input("Votre colonne: "))
            di = int(input("Votre ligne de deplacement: "))
            dj = int(input("Votre colonne de deplacement: "))
        return (i, j, di, dj)

    else:
        WIN = game.game.WIN
        SIZE = game.game.SIZE
        IMAGES = game.game.IMAGES
        draw_board = game.game.draw_board
        getCoupsValidesPiece = game.game.getCoupsValidesPiece

        snd_loop = False
        while not game.game.finJeu(jeu):
            draw_board(jeu)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    snd_loop = True
                    i, j = y//SIZE, x//SIZE
                    if i < 0 or i >= len(jeu[0]): continue
                    if j < 0 or j >= len(jeu[0][0]): continue

                    piece = jeu[0][i][j]
                    if piece[0] == " ": continue
                    pygame.draw.rect(WIN, (129,150,105), (j*SIZE,i*SIZE,SIZE,SIZE))
                    if piece[0] == "b":
                        key = "b" + piece[1]
                        WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))
                    else:
                        key = "w" + piece[1]
                        WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))

                    for ii, jj, dii, djj in getCoupsValidesPiece(jeu, jeu[0][i][j], i, j):
                        #print(jeu[0][i][j], getCoupsValidesPiece(jeu, jeu[0][i][j], i, j))
                        if ((jeu[1] == 1 and jeu[0][i][j][0] == "w") or (jeu[1] == 2 and jeu[0][i][j][0] == "b")):
                            color = (129,150,105)
                        else:
                            color = (196,180,162)
                            pygame.draw.circle(WIN, color, (djj*SIZE+SIZE//2, dii*SIZE+SIZE//2), SIZE//7)
                            pygame.display.update()
                        if (ii, jj, dii, djj) in game.getCoupsValides(jeu):
                            pygame.draw.circle(WIN, color, (djj*SIZE+SIZE//2, dii*SIZE+SIZE//2), SIZE//7)
                            pygame.display.update()

                    while snd_loop:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                            x, y = pygame.mouse.get_pos()
                            if pygame.mouse.get_pressed()[0]:
                                di, dj = y//SIZE, x//SIZE
                                if (i, j, di, dj) in game.getCoupsValides(jeu):
                                    return (i, j, di, dj)
                                else:
                                    snd_loop = False
