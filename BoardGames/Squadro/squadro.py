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


def init():
    """ void -> game_info
        Initialise le game_info (nouveau board, liste des played moves vide, liste des valid moves None, scores a 0 et player = 1)
    """
    board = [
        ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+1", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+3", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+2", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+3", "   ", "   ", "   ", "   ", "   ", "   "],
        ["j+1", "   ", "   ", "   ", "   ", "   ", "   "],
        ["   ", "r+3", "r+1", "r+2", "r+1", "r+3", "   "]
    ]
    return [board, 1, None, [], [0,0]]

def get_valid_moves(game_info):
    if game_info[2] is None:
        board = game_info[0]
        res = []
        if game_info[1] == 1:
            for i in range(1, 6):
                for j in range(0, 7):
                    if board[i][j][0] == "j":
                        res.append((i, j))
        else:
            for i in range(0, 7):
                for j in range(1, 6):
                    if board[i][j][0] == "r":
                        res.append((i, j))

        game_info[2] = res

    return game_info[2]

def is_game_over(game_info):
    return game_info[4][0] == 4 or game_info[4][1] == 4

def play_move(game_info, move):
    board = game_info[0]
    row = move[0]
    col = move[1]

    vit = board[row][col][2]
    nbPas = int(vit)
    dir = board[row][col][1]

    board[row][col] = " " * 3

    if game_info[1] == 1:
        while nbPas > 0:
            nbPas -= 1
            col = col + 1 if dir == "+" else col - 1

            if board[row][col][0] == "r":
                #retour case depart + saute par dessus
                while board[row][col][0] == "r":
                    if board[row][col][1] == "+":
                        board[6][col] = board[row][col]
                    else:
                        board[0][col] = board[row][col]
                    board[row][col] = " " * 3
                    col = col + 1 if dir == "+" else col - 1
                    if col == 0: break
                    if col == 6: break
                break

            if col == 6: break
            if col == 0: break

        if col == 0:
            board[row][col] = " " * 3
            game_info[4][0] += 1
        elif col == 6:
            board[row][col] = "j-" + str(4 - int(vit))
        else:
            board[row][col] = "j" + dir + vit

    else:
        while nbPas > 0:
            nbPas -= 1
            row = row - 1 if dir == "+" else row + 1

            if board[row][col][0] == "j":
                #retour case depart + saute par dessus
                while board[row][col][0] == "j":
                    if board[row][col][1] == "+":
                        board[row][0] = board[row][col]
                    else:
                        board[row][6] = board[row][col]
                    board[row][col] = " " * 3
                    row = row - 1 if dir == "+" else row + 1
                    if row == 0: break
                    if row == 6: break
                break

            if row == 0: break
            if row == 6: break

        if row == 0:
            board[row][col] = "r-" + str(4 - int(vit))
        elif row == 6:
            board[row][col] = " " * 3
            game_info[4][1] += 1
        else:
            board[row][col] = "r" + dir + vit

    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)

def print_board(game_info):
	board = game_info[0]

	for i in range(len(board[0])):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*8)

	for i in range(len(board)):
		print("%3s  |" %(i), end="")
		for j in range(len(board[i])):
			print(" %s |" %(board[i][j]), end="")

		print("\n", "-"*6*8)

def print_game(game_info):
	""" game_info -> void
        Affiche l"etat du game_info de la maniere suivante :
                Last move = <dernier move>
                Scores = <score 1>, <score 2>
                Board : ...

                Player <player>, it's your turn
        Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
	print("Last played move =", "None" if not game_info[3] else game_info[3][-1])
	print(f"Scores = {game_info[4]}")
	print("Board:")
	print_board(game_info)
	print(f"Player {game_info[1]}, it's your turn\n")

def draw_board(game_info):
    ROWS = 7
    COLS = 7
    board = game_info[0]
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

    if is_game_over(game_info):
        winner = game.get_winner(game_info)
        color = (255,180,0) if winner == 1 else (140,0,0)
        text_str = f"GAGNANT: J{game.get_winner(game_info)}"
    else:
        color = (255,180,0) if game_info[1] == 1 else (140,0,0)
        text_str = f"Au player {game_info[1]}"
    text = FONT.render(text_str, False, color)
    score = FONT.render(f"{game_info[4]}", False, (255,255,255))
    players = pygame.font.SysFont("couriernew", 12).render(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, (255,255,255))
    WIN.blit(text, (0, 0))
    WIN.blit(score, (text.get_width()//4, 20))
    WIN.blit(players, (0, 40))

    pygame.display.update()
