#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
import time
from threading import Thread, Event

INFINITY = float("inf")

""""
    NOMENCLATURE A RESPECTER
    move = (int, int)
    game_info = List[...] :
        0: board                        List[List[int]]
        1: player                       int (1 ou 2)
        2: valid moves                  List[(int, int, int, int)]
        3: played moves                 List[(int, int, int, int)]
        4: scores                       List[(int, int)]
        5: king first move              List[bool, bool]
        6: promotion moves indexes      Set[int]
        7: timers                       List[int, int]
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

N = 8 - 1

stop_event = Event()

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
    game_info = [board, 1, None, [], [(0,0)], [[True,True], [True,True]], set(), [0,0]]
    stop_event.clear()
    Thread(target=update_timers, args=(game_info,), daemon=True).start()
    return game_info

def init_test(key):
    game_info = init()
    from Chess.Players import human
    game.player1 = human
    game.player2 = human
    try:
        plats = {
            "CASTLING": [
                ["bR", "  ", "  ", "  ", "bK", "  ", "  ", "bR"],
                ["  ", "  ", "  ", "  ", "wN", "  ", "  ", "  "],
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
            "PROMOTION": [
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "wK", "  ", "bK", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
            ],
        }
        game_info[0] = plats[key]
    except: pass
    return game_info

def get_piece_value(piece):
    if piece[-1] == "P":
        return 1
    elif piece[-1] == "N":
        return 3.2
    elif piece[-1] == "B":
        return 3.33
    elif piece[-1] == "R":
        return 5.1
    elif piece[-1] == "Q":
        return 8.8
    elif piece[-1] == "K":
        return INFINITY

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
            game0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
            game4_tmp = game_info[4][:] ; game5_tmp0 = game_info[5][0][:] ; game5_tmp1 = game_info[5][1][:] ; game6_tmp = game_info[6].copy()
            play_move(game_info, cv)
            if not is_checked(game_info, game_info[1]%2+1):
                filtered_res.append(cv)
            game_info[0] = game0_tmp ; game_info[1] = game_info[1]%2 + 1 ; game_info[3].pop()
            game_info[4] = game4_tmp ; game_info[5][0] = game5_tmp0 ; game_info[5][1] = game5_tmp1 ; game_info[6] = game6_tmp

        game_info[2] = list(set(filtered_res))

    return game_info[2]

def get_valid_moves_of_pawn(game_info, piece, i, j):
    board = game_info[0]
    res = []

    # EN PASSANT
    if game_info[3]:
        last_row, last_col, last_d_row, last_d_col = game_info[3][-1]
        if is_en_passant(game_info):
            if piece[0] == "w":
                if last_col + 1 < 8 and board[last_d_row][last_col+1] == "wP": res.append((last_d_row, last_col+1, last_d_row-1, last_col))
                if last_col - 1 >= 0 and board[last_d_row][last_col-1] == "wP": res.append((last_d_row, last_col-1, last_d_row-1, last_col))
            else:
                if last_col + 1 < 8 and board[last_d_row][last_col+1] == "bP": res.append((last_d_row, last_col+1, last_d_row+1, last_col))
                if last_col - 1 >= 0 and board[last_d_row][last_col-1] == "bP": res.append((last_d_row, last_col-1, last_d_row+1, last_col))

    if piece[0] == "w":
        if i-1 >= 0 and board[i-1][j] == "  ":
            res.append((i, j, i-1, j))
            if i == 6 and board[i-2][j] == "  ": res.append((i, j, i-2, j))
        if j+1 < 8 and i-1 >= 0 and board[i-1][j+1][0] == "b": res.append((i, j, i-1, j+1))
        if j-1 >= 0 and i-1 >= 0 and board[i-1][j-1][0] == "b": res.append((i, j, i-1, j-1))
    else:
        if i+1 < 8 and board[i+1][j] == "  ":
            res.append((i, j, i+1, j))
            if i == 1 and board[i+2][j] == "  ": res.append((i, j, i+2, j))
        if j+1 < 8 and i+1 < 8 and board[i+1][j+1][0] == "w": res.append((i, j, i+1, j+1))
        if j-1 >= 0 and i+1 < 8 and board[i+1][j-1][0] == "w": res.append((i, j, i+1, j-1))

    return res

def get_valid_moves_of_rook(game_info, piece, i, j):
    board = game_info[0]
    res = []

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

    return res

def get_valid_moves_of_knight(game_info, piece, i, j):
    board = game_info[0]
    res = []

    if i-2 >= 0 and j+1 < 8 and board[i-2][j+1][0] != piece[0]: res.append((i, j, i-2, j+1))
    if i-2 >= 0 and j-1 >= 0 and board[i-2][j-1][0] != piece[0]: res.append((i, j, i-2, j-1))
    if i+2 < 8 and j+1 < 8 and board[i+2][j+1][0] != piece[0]: res.append((i, j, i+2, j+1))
    if i+2 < 8 and j-1 >= 0 and board[i+2][j-1][0] != piece[0]: res.append((i, j, i+2, j-1))
    if j-2 >= 0 and i+1 < 8 and board[i+1][j-2][0] != piece[0]: res.append((i, j, i+1, j-2))
    if j-2 >= 0 and i-1 >= 0 and board[i-1][j-2][0] != piece[0]: res.append((i, j, i-1, j-2))
    if j+2 < 8 and i+1 < 8 and board[i+1][j+2][0] != piece[0]: res.append((i, j, i+1, j+2))
    if j+2 < 8 and i-1 >= 0 and board[i-1][j+2][0] != piece[0]: res.append((i, j, i-1, j+2))

    return res

def get_valid_moves_of_bishop(game_info, piece, i, j):
    board = game_info[0]
    res = []

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

    return res

def get_valid_moves_of_queen(game_info, piece, i, j):
    # Rook + Bishop movements
    return get_valid_moves_of_piece(game_info, piece[0]+"R", i, j) + get_valid_moves_of_piece(game_info, piece[0]+"B", i, j)

def get_valid_moves_of_king(game_info, piece, i, j):
    board = game_info[0]
    res = []

    if i-1 >= 0 and board[i-1][j][0] != piece[0]: res.append((i, j, i-1, j))
    if j-1 >= 0 and board[i][j-1][0] != piece[0]: res.append((i, j, i, j-1))
    if i+1 < 8 and board[i+1][j][0] != piece[0]: res.append((i, j, i+1, j))
    if j+1 < 8 and board[i][j+1][0] != piece[0]: res.append((i, j, i, j+1))
    if i-1 >= 0 and j-1 >= 0 and board[i-1][j-1][0] != piece[0]: res.append((i, j, i-1, j-1))
    if i-1 >= 0 and j+1 < 8 and board[i-1][j+1][0] != piece[0]: res.append((i, j, i-1, j+1))
    if i+1 < 8 and j+1 < 8 and board[i+1][j+1][0] != piece[0]: res.append((i, j, i+1, j+1))
    if i+1 < 8 and j-1 >= 0 and board[i+1][j-1][0] != piece[0]: res.append((i, j, i+1, j-1))
    # CASTLING
    if piece[0] == "b" and any(game_info[5][1]) and (i, j) == (0, 4):
        if board[i][j+1] == "  " and board[i][j+2] == "  " and board[0][N] == "bR" and game_info[5][1][1]: res.append((i, j, i, j+2))
        if board[i][j-1] == "  " and board[i][j-2] == "  " and board[i][j-3] == "  " and board[0][0] == "bR" and game_info[5][1][0]: res.append((i, j, i, j-2))
    elif piece[0] == "w" and any(game_info[5][0]) and (i, j) == (N, 4):
        if board[i][j+1] == "  " and board[i][j+2] == "  " and board[N][N] == "wR" and game_info[5][0][1]: res.append((i, j, i, j+2))
        if board[i][j-1] == "  " and board[i][j-2] == "  " and board[N][j-3] == "  " and board[N][0] == "wR" and game_info[5][0][0]: res.append((i, j, i, j-2))

    return res

def get_valid_moves_of_piece(game_info, piece, i, j):
    """ piece is a string of len = 2 """
    switcher = {
        "P": get_valid_moves_of_pawn,
        "R": get_valid_moves_of_rook,
        "N": get_valid_moves_of_knight,
        "B": get_valid_moves_of_bishop,
        "Q": get_valid_moves_of_queen,
        "K": get_valid_moves_of_king,
    }
    return switcher[piece[1]](game_info, piece, i, j)

def is_en_passant(game_info):
    if not game_info[3]: return False
    last_row, last_col, last_d_row, last_d_col = game_info[3][-1]
    return last_col == last_d_col and game_info[0][last_d_row][last_d_col][-1] == "P" and last_row in [1, 6] and abs(last_d_row - last_row) == 2

def is_game_over(game_info):
    cv = get_valid_moves(game_info)

    def update_winner_score(game_info):
        if game_info[1] == 1:
            game_info[4].append((game_info[4][-1][0], INFINITY))
        else:
            game_info[4].append((INFINITY, game_info[4][-1][1]))

    # CHECKMATE
    if is_checked(game_info) and not cv:
        update_winner_score(game_info)
        return True
    # PAT
    elif not cv:
        return True
    # No more king
    if not get_king_pos(game_info, "b") or not get_king_pos(game_info, "w"):
        update_winner_score(game_info)
        return True
    # 50/75-move rule
    if len(game_info[3]) >= 50:
        last_scores = game_info[4][-50:]
        return last_scores.count(last_scores[0]) == len(last_scores)

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
    return None

def play_move(game_info, move):
    board = game_info[0]
    row, col, d_row, d_col = move

    piece = board[row][col]
    board[row][col] = "  "
    new_score = game_info[4][-1]

    if board[d_row][d_col][0] != " " and board[d_row][d_col][0] != piece[0]:
        new_score = get_new_score(game_info, board[d_row][d_col])

    if piece[1] == "P":
        # EN PASSANT
        if is_en_passant(game_info):
            if piece == "wP" and row == 3 and board[row][d_col] == "bP":
                new_score = get_new_score(game_info, "bP")
                board[row][d_col] = "  "
            elif piece == "bP" and row == 4 and board[row][d_col] == "wP":
                new_score = get_new_score(game_info, "wP")
                board[row][d_col] = "  "

        # PROMOTION
        if piece == "wP" and row == 1 and d_row == 0:
            piece = promotion_choice(game_info)
            if piece is None: return 'quit'
            new_score = (game_info[4][-1][0] + get_piece_value(piece), game_info[4][-1][1])
            game_info[6].add(len(game_info[3]))
        elif piece == "bP" and row == 6 and d_row == 7:
            piece = promotion_choice(game_info)
            if piece is None: return 'quit'
            new_score = (game_info[4][-1][0], game_info[4][-1][1] + get_piece_value(piece))
            game_info[6].add(len(game_info[3]))

    elif piece[1] in ["K", "R"]:
        # CASTLING
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

    board[d_row][d_col] = piece
    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)
    game_info[4].append(new_score)

def promotion_choice(game_info):
    color = 'w' if game_info[1] == 1 else 'b'
    choices = { "Rook": 'R', "Knight": 'N', "Bishop": 'B', "Queen": 'Q' }
    piece = None

    if sys._getframe(2).f_code.co_name == 'get_valid_moves': return color + 'Q'
    if game.GUI:
        from button import Button
        buttons = [
            Button(2.5*SIZE, HEIGHT//2 - 2*SIZE, 'Rook'),
            Button(2.5*SIZE, HEIGHT//2 - SIZE, 'Knight'),
            Button(2.5*SIZE, HEIGHT//2, 'Bishop'),
            Button(2.5*SIZE, HEIGHT//2 + SIZE, 'Queen'),
        ]
        while piece is None:
            draw_timers(game_info)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return

            for button in buttons:
                if button.draw_button(WIN):
                    piece = choices[button.text]

            pygame.display.update()
    else:
        while piece is None:
            piece = input('Choose a piece (r, k, b, q)').upper()
            if piece not in choices.values(): piece = None

    return color + piece

def get_new_score(game_info, taken_piece):
    if taken_piece[0] == "b":
        return (game_info[4][-1][0] + get_piece_value(taken_piece), game_info[4][-1][1])
    else:
        return (game_info[4][-1][0], game_info[4][-1][1] + get_piece_value(taken_piece))

def update_timers(game_info):
    while not stop_event.is_set():
        if len(game_info[3]) > 0:
            if game_info[1] == 1: game_info[7][0] += 1
            else: game_info[7][1] += 1
            time.sleep(1)

def print_board(game_info):
    board = game_info[0]

    for i in range(8):
        if i == 0:
            print("%5s|" %(""), end="")
        print("%3s |" %(i), end="")

    print("\n", "-"*5*9)

    for i in range(8):
        print("%3s  |" %(i), end="")
        for j in range(8):
            print(" %s |" %(board[i][j]), end="")

        print("\n", "-"*5*9)

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
    print(f"Scores = {game_info[4][-1]}")
    print("Board:")
    print_board(game_info)
    print(f"Player {game_info[1]}, it's your turn\n")

def draw_last_move(game_info):
    if game_info[3]:
        i, j, di, dj = game_info[3][-1]
        pygame.draw.rect(WIN, (205,210,106), (j*SIZE,i*SIZE,SIZE,SIZE))
        pygame.draw.rect(WIN, (205,210,106), (dj*SIZE,di*SIZE,SIZE,SIZE))

def draw_pieces(game_info):
    for i in range(N+1):
        for j in range(N+1):
            piece = game_info[0][i][j]
            if piece[0] == " ": continue
            if piece[0] == "b":
                key = "b" + piece[1]
                WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))
            else:
                key = "w" + piece[1]
                WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))

def draw_is_checked(game_info):
    is_white_checked = is_checked(game_info, 1)
    is_black_checked = is_checked(game_info, 2)
    if is_white_checked or is_black_checked:
        i, j = get_king_pos(game_info, "w") if is_white_checked else get_king_pos(game_info, "b")
        pygame.draw.circle(WIN, (255,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2-2)
        if is_white_checked:
            WIN.blit(IMAGES["wK"], (j*SIZE,i*SIZE))
        else:
            WIN.blit(IMAGES["bK"], (j*SIZE,i*SIZE))

def draw_game_state(game_info):
    if is_game_over(game_info):
        display_text = "WHITE WINS" if game_info[4][-1][0] == INFINITY else "BLACK WINS" if game_info[4][-1][1] == INFINITY else "DRAW"
        color = (255,0,0)
    else:
        display_text = "WHITE'S TURN" if game_info[1] == 1 else "BLACK'S TURN"
        color = (255,255,255)
    display_score = list(map(lambda x: round(x, 2), game_info[4][-1]))
    text = FONT.render(display_text, False, color)
    score = FONT.render(f"{display_score}", False, (255,255,255))
    players = pygame.font.SysFont("couriernew", 22).render(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]}", False, (255,255,255))
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT-OFFSET+5))
    WIN.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT-OFFSET+35))
    WIN.blit(players, (WIDTH//2 - players.get_width()//2, HEIGHT-OFFSET+65))

def draw_timers(game_info):
    time1 = pygame.font.SysFont("couriernew", 42).render(f"{int(game_info[7][0])//60:02}:{int(game_info[7][0])%60:02}", False, (255,255,255))
    time2 = pygame.font.SysFont("couriernew", 42).render(f"{int(game_info[7][1])//60:02}:{int(game_info[7][1])%60:02}", False, (255,255,255))
    time1_pos = (10, HEIGHT-70)
    time2_pos = (WIDTH-time2.get_width()-10, HEIGHT-70)

    WIN.fill((50,50,50), rect=(*time1_pos, 10+time1.get_width(), HEIGHT-70+time1.get_height()))
    WIN.fill((50,50,50), rect=(*time2_pos, WIDTH-10, HEIGHT-70+time2.get_height()))

    WIN.blit(time1, time1_pos)
    WIN.blit(time2, time2_pos)

def draw_board(game_info):
    WIN.fill((50,50,50))
    WIN.blit(IMAGES["bg"], (0,0))

    draw_last_move(game_info)
    draw_pieces(game_info)
    draw_is_checked(game_info)
    draw_game_state(game_info)
    draw_timers(game_info)

    pygame.display.update()
