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

def init():
    """ void -> game_info
        Initialise le game_info (nouveau board, liste des played moves vide, liste des valid moves None, scores a 0 et player = 1)
    """
    board = [[0 for j in range(COLS)] for i in range(ROWS)]
    return [board, 1, None, [], [0,0]]

def get_valid_moves(game_info):
    if game_info[2] is None:
        board = game_info[0]
        res = []
        for col in range(COLS):
            if board[0][col] == 0:
                res.append(col)
        game_info[2] = res
    return game_info[2]

def is_game_over(game_info):
    board = game_info[0]
    # Check horizontal positions for win
    for c in range(COLS-(N-1)):
        for r in range(ROWS):
            player = board[r][c]
            if player == 0: continue
            line = [board[r][c+i] for i in range(N)]
            if line.count(player) == N:
                game_info[4][player-1] = 1
                return True

	# Check vertical positions for win
    for c in range(COLS):
        for r in range(ROWS-(N-1)):
            player = board[r][c]
            if player == 0: continue
            line = [board[r+i][c] for i in range(N)]
            if line.count(player) == N:
                game_info[4][player-1] = 1
                return True

	# Check negatively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(ROWS-(N-1)):
            player = board[r][c]
            if player == 0: continue
            line = [board[r+i][c+i] for i in range(N)]
            if line.count(player) == N:
                game_info[4][player-1] = 1
                return True

	# Check positively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(N-1, ROWS):
            player = board[r][c]
            if player == 0: continue
            line = [board[r-i][c+i] for i in range(N)]
            if line.count(player) == N:
                game_info[4][player-1] = 1
                return True

    # Check if board is full
    if all(board[0]): return True

    return False

def drop_piece(game_info, move):
    board = game_info[0]
    res = -1
    for r in range(ROWS):
        if board[r][move] != 0:
            res = r
            break

    if res != -1:
        board[res-1][move] = game_info[1]
    else:
        board[ROWS-1][move] = game_info[1]

def play_move(game_info, move):
    drop_piece(game_info, move)

    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)

def print_board(game_info):
	board = game_info[0]

	for i in range(COLS):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*8)

	for i in range(ROWS):
		print("%3s  |" %(i), end="")
		for j in range(COLS):
			if board[i][j] == 0:
				print("%5s|" %(""), end="")
			else:
				print("%3s  |" %(board[i][j]), end="")

		print("\n", "-"*6*8)

def print_game(game_info):
	""" game_info -> void
        Affiche l'etat du game_info de la maniere suivante :
                Coup joue = <dernier move>
                Scores = <score 1>, <score 2>
                Board : ...

                Joueur <player>, a vous de jouer
        Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
	print("Last played move =", "None" if not game_info[3] else game_info[3][-1])
	print(f"Scores = {game_info[4]}")
	print("Plateau:")
	print_board(game_info)
	print(f"Joueur {game_info[1]}, a vous de jouer\n")

def draw_board(game_info, update=True):
    board = game_info[0]

    WIN.fill(BLUE)
    pygame.draw.rect(WIN, BLACK, (0,0,WIDTH,OFFSET))
    players = pygame.font.SysFont("couriernew", 16).render(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, WHITE)
    WIN.blit(players, (WIDTH - players.get_width(),0))

    if is_game_over(game_info):
        winner = game.get_winner(game_info)
        text_str = "RED WINS" if winner == 1 else "YELLOW WINS" if winner == 2 else "DRAW"
        color = RED if winner == 1 else YELLOW if winner == 2 else WHITE
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
