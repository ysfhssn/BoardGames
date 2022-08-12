#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game

""""
	NOMENCLATURE A RESPECTER
	coup = (int, int)
	jeu = List[...] :
		0: plateau      	List[List[int]]
		1: joueur       	int (1 ou 2)
		2: coups valides	List[(int, int)]
		3: coups joues  	List[(int, int)]
		4: scores       	List[int, int]
"""

if game.GUI:
    import pygame
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont("couriernew", 16)
    HEIGHT = 700
    WIDTH = 700
    SIZE = WIDTH // 6
    PIECE_LENGTH = 75
    PIECE_WIDTH = 25
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Squadro")

    bg = pygame.image.load(os.path.join(dirname, 'Images/board.png')).convert_alpha()
    yf = pygame.image.load(os.path.join(dirname, 'Images/yForward.png')).convert_alpha()
    yb = pygame.image.load(os.path.join(dirname, 'Images/yBackward.png')).convert_alpha()
    rf = pygame.image.load(os.path.join(dirname, 'Images/rForward.png')).convert_alpha()
    rb = pygame.image.load(os.path.join(dirname, 'Images/rBackward.png')).convert_alpha()

    IMAGES = {"bg": bg, "yf": yf, "yb": yb, "rf": rf, "rb": rb}
    RECTS = {"yf": [yf.get_rect() for _ in range(5)], "yb": [yb.get_rect() for _ in range(5)],
             "rf": [rf.get_rect() for _ in range(5)], "rb": [rb.get_rect() for _ in range(5)]}


def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    plateau = [
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+1", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+3", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+2", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+3", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+1", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "r+3", "r+1", "r+2", "r+1", "r+3", "   "]
    ]
    return [plateau, 1, None, [], [0,0]]

def getCoupsValides(jeu):
    if jeu[2] is None:
        plateau = jeu[0]
        res = []
        if jeu[1] == 1:
            for i in range(1, 6):
                for j in range(0, 7):
                    if plateau[i][j][0] == "j":
                        res.append((i, j))
        else:
            for i in range(0, 7):
                for j in range(1, 6):
                    if plateau[i][j][0] == "r":
                        res.append((i, j))

        jeu[2] = res

    return jeu[2]

def finJeu(jeu):
    return jeu[4][0] == 4 or jeu[4][1] == 4

def joueCoup(jeu, coup):
    plateau = jeu[0]
    row = coup[0]
    col = coup[1]

    vit = plateau[row][col][2]
    nbPas = int(vit)
    dir = plateau[row][col][1]

    plateau[row][col] = " " * 3

    if jeu[1] == 1:
        while nbPas > 0:
            nbPas -= 1
            col = col + 1 if dir == "+" else col - 1

            if plateau[row][col][0] == "r":
                #retour case depart + saute par dessus
                while plateau[row][col][0] == "r":
                    if plateau[row][col][1] == "+":
                        plateau[6][col] = plateau[row][col]
                    else:
                        plateau[0][col] = plateau[row][col]
                    plateau[row][col] = " " * 3
                    col = col + 1 if dir == "+" else col - 1
                    if col == 0: break
                    if col == 6: break
                break

            if col == 6: break
            if col == 0: break

        if col == 0:
            plateau[row][col] = " " * 3
            jeu[4][0] += 1
        elif col == 6:
            plateau[row][col] = "j-" + str(4 - int(vit))
        else:
            plateau[row][col] = "j" + dir + vit

    else:
        while nbPas > 0:
            nbPas -= 1
            row = row - 1 if dir == "+" else row + 1

            if plateau[row][col][0] == "j":
                #retour case depart + saute par dessus
                while plateau[row][col][0] == "j":
                    if plateau[row][col][1] == "+":
                        plateau[row][0] = plateau[row][col]
                    else:
                        plateau[row][6] = plateau[row][col]
                    plateau[row][col] = " " * 3
                    row = row - 1 if dir == "+" else row + 1
                    if row == 0: break
                    if row == 6: break
                break

            if row == 0: break
            if row == 6: break

        if row == 0:
            plateau[row][col] = "r-" + str(4 - int(vit))
        elif row == 6:
            plateau[row][col] = " " * 3
            jeu[4][1] += 1
        else:
            plateau[row][col] = "r" + dir + vit

    game.changeJoueur(jeu)
    jeu[2] = None
    jeu[3].append(coup)

def printPlateau(jeu):
	plateau = jeu[0]

	for i in range(len(plateau[0])):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*8)

	for i in range(len(plateau)):
		print("%3s  |" %(i), end="")
		for j in range(len(plateau[i])):
			print(" %s |" %(plateau[i][j]), end="")

		print("\n", "-"*6*8)

def affiche(jeu):
	""" jeu -> void
        Affiche l"etat du jeu de la maniere suivante :
                Coup joue = <dernier coup>
                Scores = <score 1>, <score 2>
                Plateau : ...

                Joueur <joueur>, a vous de jouer
        Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
	print("Last coup joue =", "Aucun" if not jeu[3] else jeu[3][-1])
	print(f"Scores = {jeu[4]}")
	print("Plateau:")
	printPlateau(jeu)
	print(f"Joueur {jeu[1]}, a vous de jouer\n")

def draw_board(jeu):
    ROWS = 7
    COLS = 7
    board = jeu[0]
    WIN.fill((50,50,50))
    WIN.blit(IMAGES["bg"], (0,0))

    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j][0] == "j":
                if board[i][j][1] == "+":
                    rect = RECTS["yf"][i-1]
                    if j == 0:
                        rect.topleft = (0,i*SIZE-10)
                        WIN.blit(IMAGES["yf"], rect)
                    else:
                        rect.topleft = (j*SIZE-SIZE//3+2,i*SIZE-10)
                        WIN.blit(IMAGES["yf"], rect)
                else:
                    rect = RECTS["yb"][i-1]
                    if j == 6:
                        rect.topleft = (WIDTH-SIZE//2-15,i*SIZE-10)
                        WIN.blit(IMAGES["yb"], rect)
                    else:
                        rect.topleft = (j*SIZE-SIZE//2+18,i*SIZE-10)
                        WIN.blit(IMAGES["yb"], rect)
            elif board[i][j][0] == "r":
                if board[i][j][1] == "+":
                    rect = RECTS["rf"][j-1]
                    if i == 6:
                        rect.topleft = (j*SIZE-10,HEIGHT-2*SIZE/3)
                        WIN.blit(IMAGES["rf"], rect)
                    else:
                        rect.topleft = (j*SIZE-10,i*SIZE-SIZE//3)
                        WIN.blit(IMAGES["rf"], rect)
                else:
                    rect = RECTS["rb"][j-1]
                    if i == 0:
                        rect.topleft = (j*SIZE-10,0)
                        WIN.blit(IMAGES["rb"], rect)
                    else:
                        rect.topleft = (j*SIZE-10,i*SIZE-SIZE//3)
                        WIN.blit(IMAGES["rb"], rect)

    if finJeu(jeu):
        gagnant = game.getGagnant(jeu)
        color = (255,180,0) if gagnant == 1 else (140,0,0)
        text_str = f"GAGNANT: J{game.getGagnant(jeu)}"
    else:
        color = (255,180,0) if jeu[1] == 1 else (140,0,0)
        text_str = f"Au joueur {jeu[1]}"
    text = FONT.render(text_str, False, color)
    score = FONT.render(f"{jeu[4]}", False, (255,255,255))
    joueurs = pygame.font.SysFont("couriernew", 12).render(f"{game.joueur1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.joueur2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, (255,255,255))
    WIN.blit(text, (0, 0))
    WIN.blit(score, (text.get_width()//4, 20))
    WIN.blit(joueurs, (0, 40))

    pygame.display.update()
