#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
import math
INFINITY = math.inf

""""
    NOMENCLATURE A RESPECTER
    move = (int, int)
    game_info = List[...] :
        0: board          List[List[int]]
        1: player           int (1 ou 2)
        2: valid moves    List[(int, int, int, int)]
        3: played moves      List[(int, int, int, int)]
        4: scores           List[int, int]
        5: king first move  List[bool, bool]
"""

if game.GUI:
    import pygame
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont("couriernew", 22)
    OFFSET = 100
    HEIGHT = 640 + OFFSET
    WIDTH = 640
    SIZE = WIDTH // 8
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    bg = pygame.image.load(os.path.join(dirname, "./Images/board.png")).convert_alpha()
    bP = pygame.image.load(os.path.join(dirname, "./Images/bP.png")).convert_alpha()
    bR = pygame.image.load(os.path.join(dirname, "./Images/bR.png")).convert_alpha()
    bN = pygame.image.load(os.path.join(dirname, "./Images/bN.png")).convert_alpha()
    bB = pygame.image.load(os.path.join(dirname, "./Images/bB.png")).convert_alpha()
    bQ = pygame.image.load(os.path.join(dirname, "./Images/bQ.png")).convert_alpha()
    bK = pygame.image.load(os.path.join(dirname, "./Images/bK.png")).convert_alpha()
    wP = pygame.image.load(os.path.join(dirname, "./Images/wP.png")).convert_alpha()
    wR = pygame.image.load(os.path.join(dirname, "./Images/wR.png")).convert_alpha()
    wN = pygame.image.load(os.path.join(dirname, "./Images/wN.png")).convert_alpha()
    wB = pygame.image.load(os.path.join(dirname, "./Images/wB.png")).convert_alpha()
    wQ = pygame.image.load(os.path.join(dirname, "./Images/wQ.png")).convert_alpha()
    wK = pygame.image.load(os.path.join(dirname, "./Images/wK.png")).convert_alpha()

    IMAGES = {"bg": bg, "bP": bP, "bR": bR, "bN": bN, "bB": bB, "bQ": bQ, "bK": bK,
                        "wP": wP, "wR": wR, "wN": wN, "wB": wB, "wQ": wQ, "wK": wK}


def init():
    """ void -> game_info
        Initialise le game_info (nouveau board, liste des played moves vide, liste des valid moves None, scores a 0 et player = 1)
    """
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]
    return [board, 1, None, [], [0,0,0,0], [[True,True], [True,True]]]

def init_test(key):
    game_info = init()
    try:
        plats = {
            # Test castling
            "CASTLING": [
                ["bR", "  ", "  ", "  ", "bK", "  ", "  ", "bR"],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["wR", "  ", "  ", "  ", "wK", "  ", "  ", "wR"],
            ],
            # Test pat or checkmate
            "ENDGAME": [
                ["bK", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "wQ", "wK", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ],
            # Test en passant
            "EN PASSANT": [
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["bP", "  ", "bP", "  ", "  ", "  ", "bK", "bP"],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "wP", "  ", "  ", "  ", "  ", "wP", "  "],
                ["  ", "  ", "bP", "  ", "bP", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "wP", "  ", "  ", "  ", "  "],
                ["wK", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ],
        }
        game_info[0] = plats[key]
    except: pass
    return game_info

"""
For heuristic
    P = 100
    N = 320
    B = 330
    R = 500
    Q = 900
    K = 20000
"""
def get_piece_value(p):
    if p == "P":
        return 100
    elif p == "R":
        return 500
    elif p == "N":
        return 320
    elif p == "B":
        return 330
    elif p == "Q":
        return 900
    elif p == "K":
        return 20000

def get_valid_moves(game_info):
    if game_info[2] is None:
        board = game_info[0]
        res = []
        filtered_res = []
        if game_info[1] == 1:
            for i in range(8):
                for j in range(8):
                    if board[i][j][0] == "w":
                        res += get_valid_moves_of_piece(game_info, board[i][j], i, j)
        else:
            for i in range(8):
                for j in range(8):
                    if board[i][j][0] == "b":
                        res += get_valid_moves_of_piece(game_info, board[i][j], i, j)

        for cv in res:
            jeu0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
            jeu4_tmp = game_info[4][:] ; jeu5_tmp0 = game_info[5][0][:] ; jeu5_tmp1 = game_info[5][1][:]
            game.play_move(game_info, cv)
            if not is_checked(game_info, game_info[1]%2+1):
                filtered_res.append(cv)
            game_info[0] = jeu0_tmp ; game_info[1] = game_info[1]%2 + 1 ; game_info[3].pop()
            game_info[4] = jeu4_tmp ; game_info[5][0] = jeu5_tmp0 ; game_info[5][1] = jeu5_tmp1

        game_info[2] = filtered_res

    return game_info[2]

def get_valid_moves_of_piece(game_info, piece, i, j):
    """ piece is a string of len = 2 """
    board = game_info[0]
    res = []

    # Pawn
    if piece[1] == "P":
        # EN PASSANT
        if game_info[3]:
            row, col, d_row, _ = game_info[3][-1]
            if abs(d_row - row) == 2:
                if piece[0] == "w":
                    if col + 1 < 8 and board[d_row][col+1] == "wP": res.append((d_row, col+1, d_row-1, col))
                    if col - 1 >= 0 and board[d_row][col-1] == "wP": res.append((d_row, col-1, d_row-1, col))
                else:
                    if col + 1 < 8 and board[d_row][col+1] == "bP": res.append((d_row, col+1, d_row+1, col))
                    if col - 1 >= 0 and board[d_row][col-1] == "bP": res.append((d_row, col-1, d_row+1, col))

        if piece[0] == "w":
            if i-1 >= 0 and board[i-1][j] == "  ":
                res.append((i, j, i-1, j))
                if i == 6 and board[i-2][j] == "  ": res.append((i, j, i-2, j))
            if j+1 < 8 and board[i-1][j+1][0] == "b": res.append((i, j, i-1, j+1))
            if j-1 >= 0 and board[i-1][j-1][0] == "b": res.append((i, j, i-1, j-1))
        else:
            if i+1 < 8 and board[i+1][j] == "  ":
                res.append((i, j, i+1, j))
                if i == 1 and board[i+2][j] == "  ": res.append((i, j, i+2, j))
            if j+1 < 8 and board[i+1][j+1][0] == "w": res.append((i, j, i+1, j+1))
            if j-1 >= 0 and board[i+1][j-1][0] == "w": res.append((i, j, i+1, j-1))

    # Rook
    elif piece[1] == "R":
        for ii in range(i+1, 8):
            if board[ii][j] != "  ":
                if board[ii][j][0] != piece[0]:
                    res.append((i, j, ii, j))
                break
            res.append((i, j, ii, j))
        for ii in range(i-1, -1, -1):
            if board[ii][j] != "  ":
                if board[ii][j][0] != piece[0]:
                    res.append((i, j, ii, j))
                break
            res.append((i, j, ii, j))
        for jj in range(j+1, 8):
            if board[i][jj] != "  ":
                if board[i][jj][0] != piece[0]:
                    res.append((i, j, i, jj))
                break
            res.append((i, j, i, jj))
        for jj in range(j-1, -1, -1):
            if board[i][jj] != "  ":
                if board[i][jj][0] != piece[0]:
                    res.append((i, j, i, jj))
                break
            res.append((i, j, i, jj))

    # Knight
    elif piece[1] == "N":
        if i-2 >= 0 and j+1 < 8 and board[i-2][j+1][0] != piece[0]: res.append((i, j, i-2, j+1))
        if i-2 >= 0 and j-1 >= 0 and board[i-2][j-1][0] != piece[0]: res.append((i, j, i-2, j-1))
        if i+2 < 8 and j+1 < 8 and board[i+2][j+1][0] != piece[0]: res.append((i, j, i+2, j+1))
        if i+2 < 8 and j-1 < 8 and board[i+2][j-1][0] != piece[0]: res.append((i, j, i+2, j-1))
        if j-2 >= 0 and i+1 < 8 and board[i+1][j-2][0] != piece[0]: res.append((i, j, i+1, j-2))
        if j-2 >= 0 and i-1 >= 0 and board[i-1][j-2][0] != piece[0]: res.append((i, j, i-1, j-2))
        if j+2 < 8 and i+1 < 8 and board[i+1][j+2][0] != piece[0]: res.append((i, j, i+1, j+2))
        if j+2 < 8 and i-1 >= 0 and board[i-1][j+2][0] != piece[0]: res.append((i, j, i-1, j+2))

    # Bishop
    elif piece[1] == "B":
        # bottom right
        for e, ii in enumerate(range(i+1, 8)):
            if j+e+1 >= 8: break
            elif board[ii][j+e+1] != "  ":
                if board[ii][j+e+1][0] != piece[0]:
                    res.append((i, j, ii, j+e+1))
                break
            else: res.append((i, j, ii, j+e+1))
        # bottom left
        for e, ii in enumerate(range(i+1, 8)):
            if j-e-1 < 0: break
            elif board[ii][j-e-1] != "  ":
                if board[ii][j-e-1][0] != piece[0]:
                    res.append((i, j, ii, j-e-1))
                break
            else: res.append((i, j, ii, j-e-1))
        # top left
        for e, ii in enumerate(range(i-1, -1, -1)):
            if j-e-1 < 0: break
            if board[ii][j-e-1] != "  ":
                if board[ii][j-e-1][0] != piece[0]:
                    res.append((i, j, ii, j-e-1))
                break
            else: res.append((i, j, ii, j-e-1))
        # top right
        for e, ii in enumerate(range(i-1, -1, -1)):
            if j+e+1 >= 8: break
            if board[ii][j+e+1] != "  ":
                if board[ii][j+e+1][0] != piece[0]:
                    res.append((i, j, ii, j+e+1))
                break
            else: res.append((i, j, ii, j+e+1))

    # Queen
    elif piece[1] == "Q":
        # Rook + Bishop movements
        res = get_valid_moves_of_piece(game_info, piece[0]+"R", i, j) + get_valid_moves_of_piece(game_info, piece[0]+"B", i, j)

    # King
    elif piece[1] == "K":
        if i-1 >= 0 and board[i-1][j][0] != piece[0]: res.append((i, j, i-1, j))
        if j-1 >= 0 and board[i][j-1][0] != piece[0]: res.append((i, j, i, j-1))
        if i+1 < 8 and board[i+1][j][0] != piece[0]: res.append((i, j, i+1, j))
        if j+1 < 8 and board[i][j+1][0] != piece[0]: res.append((i, j, i, j+1))
        if i-1 >= 0 and j-1 >= 0 and board[i-1][j-1][0] != piece[0]: res.append((i, j, i-1, j-1))
        if i-1 >= 0 and j+1 < 8 and board[i-1][j+1][0] != piece[0]: res.append((i, j, i-1, j+1))
        if i+1 < 8 and j+1 < 8 and board[i+1][j+1][0] != piece[0]: res.append((i, j, i+1, j+1))
        if i+1 < 8 and j-1 >= 0 and board[i+1][j-1][0] != piece[0]: res.append((i, j, i+1, j-1))
        # CASTLING
        N = 8 - 1
        if piece[0] == "b" and any(game_info[5][1]) and (i, j) == (0, 4):
            if board[i][j+1] == "  " and board[i][j+2] == "  " and board[0][N] == "bR" and game_info[5][1][1]: res.append((i, j, i, j+2))
            if board[i][j-1] == "  " and board[i][j-2] == "  " and board[i][j-3] == "  " and board[0][0] == "bR" and game_info[5][1][0]: res.append((i, j, i, j-2))
        elif piece[0] == "w" and any(game_info[5][0]) and (i, j) == (N, 4):
            if board[i][j+1] == "  " and board[i][j+2] == "  " and board[N][N] == "wR" and game_info[5][0][1]: res.append((i, j, i, j+2))
            if board[i][j-1] == "  " and board[i][j-2] == "  " and board[N][j-3] == "  " and board[N][0] == "wR" and game_info[5][0][0]: res.append((i, j, i, j-2))

    return res

def is_game_over(game_info):
    cv = get_valid_moves(game_info)
    # CHECKMATE
    if is_checked(game_info) and not cv:
        if game_info[1] == 1:
            game_info[4][1] = INFINITY
        else:
            game_info[4][0] = INFINITY
        return True
    # PAT
    elif not cv:
        game_info[4][0] = 0
        game_info[4][1] = 0
        return True

    return False

def is_checked(game_info, player=None):
    board = game_info[0]
    if player is None or player == 1:
        king_pos = get_king_pos(game_info, "w")
        for i in range(8):
            for j in range(8):
                if board[i][j][0] == "b":
                    cvp = get_valid_moves_of_piece(game_info, board[i][j], i, j)
                    for _, _, di, dj in cvp:
                        if (di, dj) == king_pos:
                            return True
    if player is None or player == 2:
        king_pos = get_king_pos(game_info, "b")
        for i in range(8):
            for j in range(8):
                if board[i][j][0] == "w":
                    cvp = get_valid_moves_of_piece(game_info, board[i][j], i, j)
                    for _, _, di, dj in cvp:
                        if (di, dj) == king_pos:
                            return True
    return False

def get_king_pos(game_info, color):
    board = game_info[0]
    if color == "b":
        for i in range(8):
            for j in range(8):
                if board[i][j] == "bK":
                    return (i, j)
    else:
        for i in reversed(range(8)):
            for j in range(8):
                if board[i][j] == "wK":
                    return (i, j)

def play_move(game_info, move):
    board = game_info[0]
    row = move[0]
    col = move[1]
    d_row = move[2]
    d_col = move[3]

    piece = board[row][col]
    board[row][col] = "  "
    if board[d_row][d_col][0] != " " and board[d_row][d_col][0] != piece[0]:
        if piece[0] == "w":
            game_info[4][0] += get_piece_value(board[d_row][d_col][1]) // 100
            game_info[4][2] += get_piece_value(board[d_row][d_col][1])
        else:
            game_info[4][1] += get_piece_value(board[d_row][d_col][1]) // 100
            game_info[4][3] += get_piece_value(board[d_row][d_col][1])
    board[d_row][d_col] = piece

    # PROMOTION
    if game_info[1] == 1:
        for j in range(8):
            if board[0][j][1] == "P":
                board[0][j] = "wQ"
    else:
        for j in range(8):
            if board[8-1][j][1] == "P":
                board[8-1][j] = "bQ"

    # CASTLING
    N = 8 - 1
    if any(game_info[5][0]):
        if piece == "wR" and (row, col) == (N, 0): game_info[5][0][0] = False
        elif piece == "wR" and (row, col) == (N, N): game_info[5][0][1] = False
        elif piece == "wK":
            if game_info[5][0][1] and d_col == col+2:
                board[N][N] = "  "
                board[N][col+1] = "wR"
            elif game_info[5][0][0] and d_col == col-2:
                board[N][0] = "  "
                board[N][col-1] = "wR"
            game_info[5][0] = [False, False]
    if any(game_info[5][1]):
        if piece == "bR" and (row, col) == (0, 0): game_info[5][1][0] = False
        elif piece == "bR" and (row, col) == (0, N): game_info[5][1][1] = False
        elif piece == "bK":
            if game_info[5][1][1] and d_col == col+2:
                board[0][N] = "  "
                board[0][col+1] = "bR"
            elif game_info[5][1][0] and d_col == col-2:
                board[0][0] = "  "
                board[0][col-1] = "bR"
            game_info[5][1] = [False, False]

    # EN PASSANT
    if piece == "wP" and row == 3 and board[row][d_col] == "bP": board[row][d_col] = "  "
    elif piece == "bP" and row == 4 and board[row][d_col] == "wP": board[row][d_col] = "  "


    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)

def print_board(game_info):
    board = game_info[0]

    for i in range(8):
        if i == 0:
            print("%5s|" %(""), end="")
        print("%3s  |" %(i), end="")

    print("\n", "-"*6*9)

    for i in range(8):
        print("%3s  |" %(i), end="")
        for j in range(8):
            print(" %s |" %(board[i][j]), end="")

        print("\n", "-"*6*9)

def print_game(game_info):
    """ game_info -> void
        Affiche l"etat du game_info de la maniere suivante :
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

def draw_board(game_info):
    ROWS = 8
    COLS = 8
    board = game_info[0]
    WIN.fill((50,50,50))
    WIN.blit(IMAGES["bg"], (0,0))

    if game_info[3]:
        i, j, di, dj = game_info[3][-1]
        pygame.draw.rect(WIN, (205,210,106), (j*SIZE,i*SIZE,SIZE,SIZE))
        pygame.draw.rect(WIN, (205,210,106), (dj*SIZE,di*SIZE,SIZE,SIZE))

    for i in range(ROWS):
        for j in range(COLS):
            piece = board[i][j]

            if piece[0] == " ": continue
            if piece[0] == "b":
                key = "b" + piece[1]
                WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))
            else:
                key = "w" + piece[1]
                WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))

    if is_checked(game_info):
        i, j = get_king_pos(game_info, "w") if game_info[1] == 1 else get_king_pos(game_info, "b")
        pygame.draw.circle(WIN, (255,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2-2)
        if game_info[1] == 1:
            WIN.blit(IMAGES["wK"], (j*SIZE,i*SIZE))
        else:
            WIN.blit(IMAGES["bK"], (j*SIZE,i*SIZE))

    if is_game_over(game_info):
        text_str = "WHITE WINS" if game_info[4][0] == INFINITY else "BLACK WINS" if game_info[4][1] == INFINITY else "PAT"
        color = (255,0,0)
    else:
        text_str = "WHITE'S TURN" if game_info[1] == 1 else "BLACK'S TURN"
        color = (255,255,255)
    text = FONT.render(text_str, False, color)
    score = FONT.render(f"{game_info[4][:2]}", False, (255,255,255))
    players = pygame.font.SysFont("couriernew", 22).render(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, (255,255,255))
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT-OFFSET+5))
    WIN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT-OFFSET+35))
    WIN.blit(players, (WIDTH//2 - players.get_width()//2, HEIGHT-OFFSET+65))

    pygame.display.update()
