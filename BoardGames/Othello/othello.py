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

def init():
    """ void -> game_info
        Initialise le game_info (nouveau board, liste des played moves vide, liste des valid moves None, scores a 0 et player = 1)
    """
    board = [[0 for j in range(8)] for i in range(8)]
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    return [board, 1, None, [], [2,2]]

def init_test(key=0):
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

def empty_positions_around_opponent(game_info):
    adv = game_info[1]%2 + 1
    sets_list = [empty_positions_around_position(game_info, l, c) for l in range(8) for c in range(8) if game_info[0][l][c] == adv]
    res = set()
    for s in sets_list:
        res |= s
    return res

def empty_positions_around_position(game_info, l, c):
    return { (l+i, c+j) for i in [-1,0,1] for j in [-1,0,1] if (c+j <= 7) and (c+j >= 0)
                                                           and (l+i <= 7) and (l+i >= 0)
                                                           and game_info[0][l+i][c+j] == 0 }

def get_valid_moves(game_info):
    if game_info[2] is None:
        cases = empty_positions_around_opponent(game_info)
        game_info[2] = [c for c in cases if get_valid_moves_offsets(game_info, c, False)]
    return game_info[2]

def get_valid_moves_offsets(game_info, move, all=True):
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if check_valid_move_by_offset(game_info, move, i, j):
                res.append((i,j))
                if not all:
                    break
    return res

def check_valid_move_by_offset(game_info, move, i, j):
    board = game_info[0]
    res = False
    l, c = move
    while True:
        l += i
        c += j
        if l > 7 or l < 0 or c > 7 or c < 0:
            return False
        if board[l][c] == 0:
            return False
        if board[l][c] == game_info[1]:
            return res
        res = True

def play_move(game_info, move):
    game_info[0][move[0]][move[1]] = game_info[1]
    game_info[4][game.get_player(game_info)-1] += 1

    directions = get_valid_moves_offsets(game_info, move)
    for d in directions:
        turn_pieces(game_info, move, d)

    game_info[3].append(move)
    game_info[2] = None
    game_info[1] = game_info[1]%2 +1

def turn_pieces(game_info, move, d):
    player = game.get_player(game_info)
    board = game_info[0]

    while board[move[0]+d[0]][move[1]+d[1]] == player%2 + 1:
        board[move[0]+d[0]][move[1]+d[1]] = player

        game_info[4][player-1] += 1
        game_info[4][player%2] -= 1

        move = (move[0]+d[0], move[1]+d[1])

def is_game_over(game_info):
    if game_info[4][0] == 0 or game_info[4][1] == 0:
        return True
    if game_info[4][0] + game_info[4][1] == 64:
        return True
    if not game.get_valid_moves(game_info):
        return True

    return False



def print_game(game_info):
    print("Last played move =", "None" if not game_info[3] else game_info[3][-1])
    print(f"Scores = {game_info[4]}")

    if game.GUI:
        print(f"Player {game_info[1]}, it's your turn\n")
        return

    print("Board: ")
    board = game_info[0]
    for x in range(len(board[0])):
        if x == 0:
            print("%5s|" %(""), end="")
        print("%3s  |" %(x), end="")
    print()
    print("--------------------------------------------------------------")

    for i in range(len(board)):
        print(" ", i, " |", end="")
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print("%5s|" %(""), end="")
            elif board[i][j] == 1:
                print("%3s  |" %("W"), end="")
            else:
                print("%3s  |" %("B"), end="")
        print()
        print("--------------------------------------------------------------")

    print(f"Player {game_info[1]}, it's your turn\n")

def draw_board(game_info):
    ROWS = 8
    COLS = 8
    board = game_info[0]
    WIN.fill((34,139,34))
    for i in range(ROWS):
        if i != 0: pygame.draw.line(WIN, (0,0,0), (0,i*SIZE), (WIDTH,i*SIZE))
        for j in range(COLS):
            if j != 0: pygame.draw.line(WIN, (0,0,0), (j*SIZE, 0), (j*SIZE, WIDTH))
            if board[i][j] == 1:
                pygame.draw.circle(WIN, (255,255,255), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2 - 2)
            elif board[i][j] == 2:
                pygame.draw.circle(WIN, (0,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//2 - 2)

    for i, j in game.get_valid_moves(game_info):
        pygame.draw.circle(WIN, (255,0,0), (j*SIZE+SIZE//2, i*SIZE+SIZE//2), SIZE//10)

    text = FONT.render(f'WHITE: {game_info[4][0]} BLACK: {game_info[4][1]}', False, (0,0,0))
    text_w = text.get_width()
    text_h = text.get_height()
    WIN.blit(text, (WIDTH//2-text_w//2,WIDTH+text_h//2))

    pygame.display.update()