#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
if game.GUI: import pygame

N = 4
ROWS = 6
COLS = 7

if game.GUI:
    import pygame
    pygame.init()
    SIZE = 90
    OFFSET = SIZE + 2
    HEIGHT = ROWS * SIZE + OFFSET
    WIDTH = COLS * SIZE
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4")

    RED = (255,0,0)
    YELLOW = (255,255,0)
    WHITE = (255,255,255)
    BLUE = (0,0,255)
    BLACK = (0,0,0)

def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    plateau = [[0 for j in range(COLS)] for i in range(ROWS)]
    return [plateau, 1, None, [], [0,0]]

def getCoupsValides(jeu):
    if jeu[2] is None:
        plateau = jeu[0]
        res = []
        for col in range(COLS):
            if plateau[0][col] == 0:
                res.append(col)
        jeu[2] = res
    return jeu[2]

def finJeu(jeu):
    board = jeu[0]
    # Check horizontal locations for win
    for c in range(COLS-(N-1)):
        for r in range(ROWS):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r][c+i] for i in range(N)]
            if line.count(joueur) == N:
                jeu[4][joueur-1] = 1
                return True

	# Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-(N-1)):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r+i][c] for i in range(N)]
            if line.count(joueur) == N:
                jeu[4][joueur-1] = 1
                return True

	# Check negatively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(ROWS-(N-1)):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r+i][c+i] for i in range(N)]
            if line.count(joueur) == N:
                jeu[4][joueur-1] = 1
                return True

	# Check positively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(N-1, ROWS):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r-i][c+i] for i in range(N)]
            if line.count(joueur) == N:
                jeu[4][joueur-1] = 1
                return True

    # Check if board is full
    if all(board[0]): return True

    return False

def drop_piece(jeu, coup):
    plateau = jeu[0]
    res = -1
    for r in range(ROWS):
        if plateau[r][coup] != 0:
            res = r
            break

    if res != -1:
        plateau[res-1][coup] = jeu[1]
    else:
        plateau[ROWS-1][coup] = jeu[1]

def joueCoup(jeu, coup):
    drop_piece(jeu, coup)

    game.changeJoueur(jeu)
    jeu[2] = None
    jeu[3].append(coup)

def printPlateau(jeu):
	plateau = jeu[0]

	for i in range(COLS):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*8)

	for i in range(ROWS):
		print("%3s  |" %(i), end="")
		for j in range(COLS):
			if plateau[i][j] == 0:
				print("%5s|" %(""), end="")
			else:
				print("%3s  |" %(plateau[i][j]), end="")

		print("\n", "-"*6*8)

def affiche(jeu):
	""" jeu -> void
        Affiche l'etat du jeu de la maniere suivante :
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

def draw_board(jeu, update=True):
    board = jeu[0]

    WIN.fill(BLUE)
    pygame.draw.rect(WIN, BLACK, (0,0,WIDTH,OFFSET))
    joueurs = pygame.font.SysFont("couriernew", 16).render(f"{game.joueur1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.joueur2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, WHITE)
    WIN.blit(joueurs, (WIDTH - joueurs.get_width(),0))

    if finJeu(jeu):
        gagnant = game.getGagnant(jeu)
        text_str = "RED WINS" if gagnant == 1 else "YELLOW WINS" if gagnant == 2 else "DRAW"
        color = RED if gagnant == 1 else YELLOW if gagnant == 2 else WHITE
        text = pygame.font.SysFont("couriernew", 42).render(text_str, False, color)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, OFFSET//2 - text.get_height()//2))

    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == 0:
                pygame.draw.circle(WIN, WHITE, (j*SIZE+SIZE//2, i*SIZE+SIZE//2 + OFFSET), SIZE//2 - 2)
            elif board[i][j] == 1:
                pygame.draw.circle(WIN, RED, (j*SIZE+SIZE//2, i*SIZE+SIZE//2 + OFFSET), SIZE//2 - 2)
            else:
                pygame.draw.circle(WIN, YELLOW, (j*SIZE+SIZE//2, i*SIZE+SIZE//2 + OFFSET), SIZE//2 - 2)

    if update:
        pygame.display.update()
