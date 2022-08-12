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
    coup = (int, int)
    jeu = List[...] :
        0: plateau          List[List[int]]
        1: joueur           int (1 ou 2)
        2: coups valides    List[(int, int, int, int)]
        3: coups joues      List[(int, int, int, int)]
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


def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    plateau = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]
    return [plateau, 1, None, [], [0,0,0,0], [[True,True], [True,True]]]

def initialiseInteressant(key):
    jeu = initialiseJeu()
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
        jeu[0] = plats[key]
    except: pass
    return jeu

"""
For heuristic
    P = 100
    N = 320
    B = 330
    R = 500
    Q = 900
    K = 20000
"""
def getValuePiece(p):
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

def getCoupsValides(jeu):
    if jeu[2] is None:
        plateau = jeu[0]
        res = []
        filtered_res = []
        if jeu[1] == 1:
            for i in range(8):
                for j in range(8):
                    if plateau[i][j][0] == "w":
                        res += getCoupsValidesPiece(jeu, plateau[i][j], i, j)
        else:
            for i in range(8):
                for j in range(8):
                    if plateau[i][j][0] == "b":
                        res += getCoupsValidesPiece(jeu, plateau[i][j], i, j)

        for cv in res:
            jeu0_tmp = [jeu[0][i][:] for i in range(len(jeu[0]))]
            jeu4_tmp = jeu[4][:] ; jeu5_tmp0 = jeu[5][0][:] ; jeu5_tmp1 = jeu[5][1][:]
            game.joueCoup(jeu, cv)
            if not is_checked(jeu, jeu[1]%2+1):
                filtered_res.append(cv)
            jeu[0] = jeu0_tmp ; jeu[1] = jeu[1]%2 + 1 ; jeu[3].pop()
            jeu[4] = jeu4_tmp ; jeu[5][0] = jeu5_tmp0 ; jeu[5][1] = jeu5_tmp1

        jeu[2] = filtered_res

    return jeu[2]

def getCoupsValidesPiece(jeu, piece, i, j):
    """ piece is a string of len = 2 """
    plateau = jeu[0]
    res = []

    # Pawn
    if piece[1] == "P":
        # EN PASSANT
        if jeu[3]:
            row, col, d_row, _ = jeu[3][-1]
            if abs(d_row - row) == 2:
                if piece[0] == "w":
                    if col + 1 < 8 and plateau[d_row][col+1] == "wP": res.append((d_row, col+1, d_row-1, col))
                    if col - 1 >= 0 and plateau[d_row][col-1] == "wP": res.append((d_row, col-1, d_row-1, col))
                else:
                    if col + 1 < 8 and plateau[d_row][col+1] == "bP": res.append((d_row, col+1, d_row+1, col))
                    if col - 1 >= 0 and plateau[d_row][col-1] == "bP": res.append((d_row, col-1, d_row+1, col))

        if piece[0] == "w":
            if i-1 >= 0 and plateau[i-1][j] == "  ":
                res.append((i, j, i-1, j))
                if i == 6 and plateau[i-2][j] == "  ": res.append((i, j, i-2, j))
            if j+1 < 8 and plateau[i-1][j+1][0] == "b": res.append((i, j, i-1, j+1))
            if j-1 >= 0 and plateau[i-1][j-1][0] == "b": res.append((i, j, i-1, j-1))
        else:
            if i+1 < 8 and plateau[i+1][j] == "  ":
                res.append((i, j, i+1, j))
                if i == 1 and plateau[i+2][j] == "  ": res.append((i, j, i+2, j))
            if j+1 < 8 and plateau[i+1][j+1][0] == "w": res.append((i, j, i+1, j+1))
            if j-1 >= 0 and plateau[i+1][j-1][0] == "w": res.append((i, j, i+1, j-1))

    # Rook
    elif piece[1] == "R":
        for ii in range(i+1, 8):
            if plateau[ii][j] != "  ":
                if plateau[ii][j][0] != piece[0]:
                    res.append((i, j, ii, j))
                break
            res.append((i, j, ii, j))
        for ii in range(i-1, -1, -1):
            if plateau[ii][j] != "  ":
                if plateau[ii][j][0] != piece[0]:
                    res.append((i, j, ii, j))
                break
            res.append((i, j, ii, j))
        for jj in range(j+1, 8):
            if plateau[i][jj] != "  ":
                if plateau[i][jj][0] != piece[0]:
                    res.append((i, j, i, jj))
                break
            res.append((i, j, i, jj))
        for jj in range(j-1, -1, -1):
            if plateau[i][jj] != "  ":
                if plateau[i][jj][0] != piece[0]:
                    res.append((i, j, i, jj))
                break
            res.append((i, j, i, jj))

    # Knight
    elif piece[1] == "N":
        if i-2 >= 0 and j+1 < 8 and plateau[i-2][j+1][0] != piece[0]: res.append((i, j, i-2, j+1))
        if i-2 >= 0 and j-1 >= 0 and plateau[i-2][j-1][0] != piece[0]: res.append((i, j, i-2, j-1))
        if i+2 < 8 and j+1 < 8 and plateau[i+2][j+1][0] != piece[0]: res.append((i, j, i+2, j+1))
        if i+2 < 8 and j-1 < 8 and plateau[i+2][j-1][0] != piece[0]: res.append((i, j, i+2, j-1))
        if j-2 >= 0 and i+1 < 8 and plateau[i+1][j-2][0] != piece[0]: res.append((i, j, i+1, j-2))
        if j-2 >= 0 and i-1 >= 0 and plateau[i-1][j-2][0] != piece[0]: res.append((i, j, i-1, j-2))
        if j+2 < 8 and i+1 < 8 and plateau[i+1][j+2][0] != piece[0]: res.append((i, j, i+1, j+2))
        if j+2 < 8 and i-1 >= 0 and plateau[i-1][j+2][0] != piece[0]: res.append((i, j, i-1, j+2))

    # Bishop
    elif piece[1] == "B":
        # bottom right
        for e, ii in enumerate(range(i+1, 8)):
            if j+e+1 >= 8: break
            elif plateau[ii][j+e+1] != "  ":
                if plateau[ii][j+e+1][0] != piece[0]:
                    res.append((i, j, ii, j+e+1))
                break
            else: res.append((i, j, ii, j+e+1))
        # bottom left
        for e, ii in enumerate(range(i+1, 8)):
            if j-e-1 < 0: break
            elif plateau[ii][j-e-1] != "  ":
                if plateau[ii][j-e-1][0] != piece[0]:
                    res.append((i, j, ii, j-e-1))
                break
            else: res.append((i, j, ii, j-e-1))
        # top left
        for e, ii in enumerate(range(i-1, -1, -1)):
            if j-e-1 < 0: break
            if plateau[ii][j-e-1] != "  ":
                if plateau[ii][j-e-1][0] != piece[0]:
                    res.append((i, j, ii, j-e-1))
                break
            else: res.append((i, j, ii, j-e-1))
        # top right
        for e, ii in enumerate(range(i-1, -1, -1)):
            if j+e+1 >= 8: break
            if plateau[ii][j+e+1] != "  ":
                if plateau[ii][j+e+1][0] != piece[0]:
                    res.append((i, j, ii, j+e+1))
                break
            else: res.append((i, j, ii, j+e+1))

    # Queen
    elif piece[1] == "Q":
        # Rook + Bishop movements
        res = getCoupsValidesPiece(jeu, piece[0]+"R", i, j) + getCoupsValidesPiece(jeu, piece[0]+"B", i, j)

    # King
    elif piece[1] == "K":
        if i-1 >= 0 and plateau[i-1][j][0] != piece[0]: res.append((i, j, i-1, j))
        if j-1 >= 0 and plateau[i][j-1][0] != piece[0]: res.append((i, j, i, j-1))
        if i+1 < 8 and plateau[i+1][j][0] != piece[0]: res.append((i, j, i+1, j))
        if j+1 < 8 and plateau[i][j+1][0] != piece[0]: res.append((i, j, i, j+1))
        if i-1 >= 0 and j-1 >= 0 and plateau[i-1][j-1][0] != piece[0]: res.append((i, j, i-1, j-1))
        if i-1 >= 0 and j+1 < 8 and plateau[i-1][j+1][0] != piece[0]: res.append((i, j, i-1, j+1))
        if i+1 < 8 and j+1 < 8 and plateau[i+1][j+1][0] != piece[0]: res.append((i, j, i+1, j+1))
        if i+1 < 8 and j-1 >= 0 and plateau[i+1][j-1][0] != piece[0]: res.append((i, j, i+1, j-1))
        # CASTLING
        N = 8 - 1
        if piece[0] == "b" and any(jeu[5][1]) and (i, j) == (0, 4):
            if plateau[i][j+1] == "  " and plateau[i][j+2] == "  " and plateau[0][N] == "bR" and jeu[5][1][1]: res.append((i, j, i, j+2))
            if plateau[i][j-1] == "  " and plateau[i][j-2] == "  " and plateau[i][j-3] == "  " and plateau[0][0] == "bR" and jeu[5][1][0]: res.append((i, j, i, j-2))
        elif piece[0] == "w" and any(jeu[5][0]) and (i, j) == (N, 4):
            if plateau[i][j+1] == "  " and plateau[i][j+2] == "  " and plateau[N][N] == "wR" and jeu[5][0][1]: res.append((i, j, i, j+2))
            if plateau[i][j-1] == "  " and plateau[i][j-2] == "  " and plateau[N][j-3] == "  " and plateau[N][0] == "wR" and jeu[5][0][0]: res.append((i, j, i, j-2))

    return res

def finJeu(jeu):
    cv = getCoupsValides(jeu)
    # CHECKMATE
    if is_checked(jeu) and not cv:
        if jeu[1] == 1:
            jeu[4][1] = INFINITY
        else:
            jeu[4][0] = INFINITY
        return True
    # PAT
    elif not cv:
        jeu[4][0] = 0
        jeu[4][1] = 0
        return True

    return False

def is_checked(jeu, player=None):
    plateau = jeu[0]
    if player is None or player == 1:
        king_pos = get_king_pos(jeu, "w")
        for i in range(8):
            for j in range(8):
                if plateau[i][j][0] == "b":
                    cvp = getCoupsValidesPiece(jeu, plateau[i][j], i, j)
                    for _, _, di, dj in cvp:
                        if (di, dj) == king_pos:
                            return True
    if player is None or player == 2:
        king_pos = get_king_pos(jeu, "b")
        for i in range(8):
            for j in range(8):
                if plateau[i][j][0] == "w":
                    cvp = getCoupsValidesPiece(jeu, plateau[i][j], i, j)
                    for _, _, di, dj in cvp:
                        if (di, dj) == king_pos:
                            return True
    return False

def get_king_pos(jeu, color):
    plateau = jeu[0]
    if color == "b":
        for i in range(8):
            for j in range(8):
                if plateau[i][j] == "bK":
                    return (i, j)
    else:
        for i in reversed(range(8)):
            for j in range(8):
                if plateau[i][j] == "wK":
                    return (i, j)

def joueCoup(jeu, coup):
    plateau = jeu[0]
    row = coup[0]
    col = coup[1]
    d_row = coup[2]
    d_col = coup[3]

    piece = plateau[row][col]
    plateau[row][col] = "  "
    if plateau[d_row][d_col][0] != " " and plateau[d_row][d_col][0] != piece[0]:
        if piece[0] == "w":
            jeu[4][0] += getValuePiece(plateau[d_row][d_col][1]) // 100
            jeu[4][2] += getValuePiece(plateau[d_row][d_col][1])
        else:
            jeu[4][1] += getValuePiece(plateau[d_row][d_col][1]) // 100
            jeu[4][3] += getValuePiece(plateau[d_row][d_col][1])
    plateau[d_row][d_col] = piece

    # PROMOTION
    if jeu[1] == 1:
        for j in range(8):
            if plateau[0][j][1] == "P":
                plateau[0][j] = "wQ"
    else:
        for j in range(8):
            if plateau[8-1][j][1] == "P":
                plateau[8-1][j] = "bQ"

    # CASTLING
    N = 8 - 1
    if any(jeu[5][0]):
        if piece == "wR" and (row, col) == (N, 0): jeu[5][0][0] = False
        elif piece == "wR" and (row, col) == (N, N): jeu[5][0][1] = False
        elif piece == "wK":
            if jeu[5][0][1] and d_col == col+2:
                plateau[N][N] = "  "
                plateau[N][col+1] = "wR"
            elif jeu[5][0][0] and d_col == col-2:
                plateau[N][0] = "  "
                plateau[N][col-1] = "wR"
            jeu[5][0] = [False, False]
    if any(jeu[5][1]):
        if piece == "bR" and (row, col) == (0, 0): jeu[5][1][0] = False
        elif piece == "bR" and (row, col) == (0, N): jeu[5][1][1] = False
        elif piece == "bK":
            if jeu[5][1][1] and d_col == col+2:
                plateau[0][N] = "  "
                plateau[0][col+1] = "bR"
            elif jeu[5][1][0] and d_col == col-2:
                plateau[0][0] = "  "
                plateau[0][col-1] = "bR"
            jeu[5][1] = [False, False]

    # EN PASSANT
    if piece == "wP" and row == 3 and plateau[row][d_col] == "bP": plateau[row][d_col] = "  "
    elif piece == "bP" and row == 4 and plateau[row][d_col] == "wP": plateau[row][d_col] = "  "


    game.changeJoueur(jeu)
    jeu[2] = None
    jeu[3].append(coup)

def printPlateau(jeu):
    plateau = jeu[0]

    for i in range(8):
        if i == 0:
            print("%5s|" %(""), end="")
        print("%3s  |" %(i), end="")

    print("\n", "-"*6*9)

    for i in range(8):
        print("%3s  |" %(i), end="")
        for j in range(8):
            print(" %s |" %(plateau[i][j]), end="")

        print("\n", "-"*6*9)

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
    ROWS = 8
    COLS = 8
    board = jeu[0]
    WIN.fill((50,50,50))
    WIN.blit(IMAGES["bg"], (0,0))

    if jeu[3]:
        i, j, di, dj = jeu[3][-1]
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

    if is_checked(jeu):
        i, j = get_king_pos(jeu, "w") if jeu[1] == 1 else get_king_pos(jeu, "b")
        pygame.draw.circle(WIN, (255,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2-2)
        if jeu[1] == 1:
            WIN.blit(IMAGES["wK"], (j*SIZE,i*SIZE))
        else:
            WIN.blit(IMAGES["bK"], (j*SIZE,i*SIZE))

    if finJeu(jeu):
        text_str = "WHITE WINS" if jeu[4][0] == INFINITY else "BLACK WINS" if jeu[4][1] == INFINITY else "PAT"
        color = (255,0,0)
    else:
        text_str = "WHITE'S TURN" if jeu[1] == 1 else "BLACK'S TURN"
        color = (255,255,255)
    text = FONT.render(text_str, False, color)
    score = FONT.render(f"{jeu[4][:2]}", False, (255,255,255))
    joueurs = pygame.font.SysFont("couriernew", 22).render(f"{game.joueur1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.joueur2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, (255,255,255))
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT-OFFSET+5))
    WIN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT-OFFSET+35))
    WIN.blit(joueurs, (WIDTH//2 - joueurs.get_width()//2, HEIGHT-OFFSET+65))

    pygame.display.update()
