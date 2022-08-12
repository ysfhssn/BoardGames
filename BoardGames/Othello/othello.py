#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game

if game.GUI:
    import pygame
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont('couriernew', 20)
    SIZE = 70
    OFFSET = 35
    WIDTH = 8 * SIZE
    HEIGHT = WIDTH + OFFSET
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Othello")

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    plateau = [[0 for j in range(8)] for i in range(8)]
    plateau[3][3] = 1
    plateau[3][4] = 2
    plateau[4][3] = 2
    plateau[4][4] = 1
    return [plateau, 1, None, [], [2,2]]

def initialiseInteressant(key=0):
    d = {
        0: [[1,2,2,2,2,2,2,0],
            [0,0,0,0,0,0,2,2],
            [0,0,0,0,0,2,0,2],
            [0,0,0,0,2,0,0,2],
            [0,0,0,2,0,0,0,2],
            [0,0,2,0,0,0,0,2],
            [0,2,0,0,0,0,0,2],
            [1,0,0,0,0,0,0,1]]
    }
    return [d[key], 1, None, [], [1000, 1000]]

def casesVidesAutourAdv(jeu):
    """ jeu -> set
        retourne l'ensemble des cases vides autour des cases de l'adversaire
    """
    adv = jeu[1]%2 + 1
    sets_list = [entourageVide(jeu, l, c) for l in range(8) for c in range(8) if jeu[0][l][c] == adv]
    res = set()
    for s in sets_list:
        res |= s
    return res

def entourageVide(jeu, l, c):
    """ jeu, l, c, -> set
        retourne l'ensemble des cases vides autour la case l, c
    """
    return { (l+i, c+j) for i in [-1,0,1] for j in [-1,0,1] if (c+j <= 7) and (c+j >= 0)
                                                           and (l+i <= 7) and (l+i >= 0)
                                                           and jeu[0][l+i][c+j] == 0 }

def getCoupsValides(jeu):
    if jeu[2] is None:
        cases = casesVidesAutourAdv(jeu)
        jeu[2] = [c for c in cases if getEncadrementsDirections(jeu, c, False)]
    return jeu[2]

def getEncadrementsDirections(jeu, c, all=True):
    """ jeu -> list
        retourne la liste des directions
        all: if true, retourne tous les directions possibles du coup c
             if false, retourne au plus une direction
    """
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if checkEncadrementDirection(jeu, c, i, j):
                res.append((i,j))
                if not all:
                    break
    return res

def checkEncadrementDirection(jeu, coup, i, j):
    plateau = jeu[0]
    res = False
    l, c = coup
    while True:
        l += i
        c += j
        if l>7 or l<0 or c>7 or c<0:
            return False
        if plateau[l][c] == 0:
            return False
        if plateau[l][c] == jeu[1]:
            return res
        res = True

def joueCoup(jeu, coup):
    jeu[0][coup[0]][coup[1]] = jeu[1]
    jeu[4][game.getJoueur(jeu)-1] += 1

    directions = getEncadrementsDirections(jeu, coup)
    for d in directions:
        retournerPions(jeu, coup, d)

    jeu[3].append(coup)
    jeu[2] = None
    jeu[1] = jeu[1]%2 +1

def retournerPions(jeu, coup, d):
    """ jeu -> void
        retourne les pions dans la direction d
    """
    joueur = game.getJoueur(jeu)
    plateau = jeu[0]

    while plateau[coup[0]+d[0]][coup[1]+d[1]] == joueur%2 + 1:
        plateau[coup[0]+d[0]][coup[1]+d[1]] = joueur

        jeu[4][joueur-1] += 1
        jeu[4][joueur%2] -= 1

        coup = (coup[0]+d[0], coup[1]+d[1])

def finJeu(jeu):
    if jeu[4][0] == 0 or jeu[4][1] == 0:
        return True
    if jeu[4][0] + jeu[4][1] == 64:
        return True
    if not game.getCoupsValides(jeu):
        return True

    return False



def affiche(jeu):
    """ jeu -> void
        Affiche l'etat du jeu de la maniere suivante :
                 Coup joue = <dernier coup>
                 Scores = <score 1>, <score 2>
                 Plateau :

                         |       0     |     1       |      2     |      ...
                    ------------------------------------------------
                      0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                    ------------------------------------------------
                      1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                    ------------------------------------------------
                    ...       ...          ...            ...
                 Joueur <joueur>, a vous de jouer

         Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """

    print("Last coup joue =", "Aucun" if not jeu[3] else jeu[3][-1])
    print(f"Scores = {jeu[4]}")

    if game.GUI:
        print(f"Joueur {jeu[1]}, a vous de jouer\n")
        return

    print("Plateau: ")
    plateau = jeu[0]
    for x in range(len(plateau[0])):
        if x == 0:
            print("%5s|" %(""), end="")
        print("%3s  |" %(x), end="")
    print()
    print("--------------------------------------------------------------")

    for i in range(len(plateau)):
        print(" ", i, " |", end="")
        for j in range(len(plateau[i])):
            if plateau[i][j] == 0:
                print("%5s|" %(""), end="")
            elif plateau[i][j] == 1:
                print("%3s  |" %("W"), end="")
            else:
                print("%3s  |" %("B"), end="")
        print()
        print("--------------------------------------------------------------")

    print(f"Joueur {jeu[1]}, a vous de jouer\n")

def draw_board(jeu):
    ROWS = 8
    COLS = 8
    board = jeu[0]
    WIN.fill((34,139,34))
    for i in range(ROWS):
        if i != 0: pygame.draw.line(WIN, (0,0,0), (0,i*SIZE), (WIDTH,i*SIZE))
        for j in range(COLS):
            if j != 0: pygame.draw.line(WIN, (0,0,0), (j*SIZE, 0), (j*SIZE, WIDTH))
            if board[i][j] == 1:
                pygame.draw.circle(WIN, (255,255,255), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2 - 2)
            elif board[i][j] == 2:
                pygame.draw.circle(WIN, (0,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2 - 2)

    for i, j in game.getCoupsValides(jeu):
        pygame.draw.circle(WIN, (255,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//10)

    text = FONT.render(f'WHITE: {jeu[4][0]} BLACK: {jeu[4][1]}', False, (0,0,0))
    text_w = text.get_width()
    text_h = text.get_height()
    WIN.blit(text, (WIDTH//2-text_w//2,WIDTH+text_h//2))

    pygame.display.update()