#!/usr/bin/env python
# -*- coding: utf-8 -*-
import game
if game.GUI: import pygame

####### WEIGHTS #######
SCORE_AI        =  1.00
SCORE_OP        =  1.00
PAWN_AI         =  1.00
KNIGHT_AI       =  1.00
BISHOP_AI       =  1.00
ROOK_AI         =  1.00
QUEEN_AI        =  1.00
KING_AI         =  1.00
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

WEIGHTS = [SCORE_AI, SCORE_OP, PAWN_AI, KNIGHT_AI, BISHOP_AI, ROOK_AI, QUEEN_AI, KING_AI]

PLIES = 3
NUM_NODES = 0

CACHE = {}
NUM_NODES_CACHE = 0
############################################################################

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    global AI_PLAYER, OPPONENT, NUM_NODES, NUM_NODES_CACHE
    AI_PLAYER = game.get_player(game_info)
    OPPONENT = AI_PLAYER%2 + 1
    NUM_NODES = 0
    NUM_NODES_CACHE = 0

    return decision(game_info, -INFINITY, INFINITY)

def order_moves(game_info, movesPossibles, reverse):
    ranked_moves = []
    for move in movesPossibles:
        game0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
        game4_tmp = game_info[4][:] ; game5_tmp0 = game_info[5][0][:] ; game5_tmp1 = game_info[5][1][:]
        game.play_move(game_info, move)
        score = heuristic(game_info)
        ranked_moves.append((score, move))
        game_info[0] = game0_tmp ; game_info[1] = AI_PLAYER ; game_info[3].pop()
        game_info[4] = game4_tmp ; game_info[5][0] = game5_tmp0 ; game_info[5][1] = game5_tmp1
    ranked_moves.sort(reverse=reverse)
    return [rc[1] for rc in ranked_moves]

def decision(game_info, alpha, beta):
    vmax = -INFINITY
    bestMove = None

    for move in order_moves(game_info, game.get_valid_moves(game_info), True):
        global NUM_NODES
        NUM_NODES += 1
        game0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
        game4_tmp = game_info[4][:] ; game5_tmp0 = game_info[5][0][:] ; game5_tmp1 = game_info[5][1][:]
        game.play_move(game_info, move)

        v = minimax(game_info, PLIES-1, False, alpha, beta)
        game_info[0] = game0_tmp ; game_info[1] = AI_PLAYER ; game_info[3].pop()
        game_info[4] = game4_tmp ; game_info[5][0] = game5_tmp0 ; game_info[5][1] = game5_tmp1
        if v > vmax:
            vmax = v
            bestMove = move
        if v > alpha:
            alpha = v

    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None

    return bestMove

def minimax(game_info, plies, maximizingPlayer, alpha, beta):
	####### GOAL STATE EVALUATION #######
    if game.is_game_over(game_info):
        winner = game.get_winner(game_info)
        if winner == AI_PLAYER:
            return 1000000 - plies # winning A$AP
        elif winner == 0:
            return 0
        else:
            return plies - 1000000
	####################################

    if plies == 0:
        global NUM_NODES_CACHE
        str_board = str(game_info[0])
        if str_board in CACHE:
            NUM_NODES_CACHE += 1
            return CACHE[str_board]
        else:
            h = heuristic(game_info)
            CACHE[str_board] = h
            return h

    global NUM_NODES
    if maximizingPlayer:
        vmax = -INFINITY
        for move in game.get_valid_moves(game_info):
            NUM_NODES += 1
            game0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
            game4_tmp = game_info[4][:] ; game5_tmp0 = game_info[5][0][:] ; game5_tmp1 = game_info[5][1][:]
            game.play_move(game_info, move)

            v = minimax(game_info, plies-1, False, alpha, beta)
            game_info[0] = game0_tmp ; game_info[1] = AI_PLAYER ; game_info[3].pop()
            game_info[4] = game4_tmp ; game_info[5][0] = game5_tmp0 ; game_info[5][1] = game5_tmp1
            if v > vmax: vmax = v
            if v >= beta: return v # beta cutoff
            if v > alpha: alpha = v

        return vmax

    else:
        vmin = INFINITY
        for move in game.get_valid_moves(game_info):
            NUM_NODES += 1
            game0_tmp = [game_info[0][i][:] for i in range(len(game_info[0]))]
            game4_tmp = game_info[4][:] ; game5_tmp0 = game_info[5][0][:] ; game5_tmp1 = game_info[5][1][:]
            game.play_move(game_info, move)

            v = minimax(game_info, plies-1, True, alpha, beta)
            game_info[0] = game0_tmp ; game_info[1] = AI_PLAYER ; game_info[3].pop()
            game_info[4] = game4_tmp ; game_info[5][0] = game5_tmp0 ; game_info[5][1] = game5_tmp1
            if v < vmin: vmin = v
            if v <= alpha: return v # alpha cutoff
            if v < beta: beta = v

        return vmin

############################################################################

def get_inputs(game_info):
    return [score(game_info, AI_PLAYER), score(game_info, OPPONENT), pawn_score(game_info, AI_PLAYER), knight_score(game_info, AI_PLAYER),
            bishop_score(game_info, AI_PLAYER), rook_score(game_info, AI_PLAYER), queen_score(game_info, AI_PLAYER), king_score(game_info, AI_PLAYER)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = get_inputs(game_info)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def score(game_info, player):
    cpt = game.get_score_player(game_info, player) * 100
    return cpt if player == AI_PLAYER else -cpt


pawn_w_pst = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0 ]
]

pawn_b_pst = [pawn_w_pst[i] for i in reversed(range(8))]

def pawn_score(game_info, player):
    board = game_info[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "P":
                cpt += pawn_w_pst[i][j] if player == 1 else pawn_b_pst[i][j]
    return cpt if player == AI_PLAYER else -cpt

knight_w_pst = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50],
]

knight_b_pst = [knight_w_pst[i] for i in reversed(range(8))]

def knight_score(game_info, player):
    board = game_info[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "N":
                cpt += knight_w_pst[i][j] if player == 1 else knight_b_pst[i][j]
    return cpt if player == AI_PLAYER else -cpt

bishop_w_pst = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20],
]

bishop_b_pst = [bishop_w_pst[i] for i in reversed(range(8))]

def bishop_score(game_info, player):
    board = game_info[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "B":
                cpt += knight_w_pst[i][j] if player == 1 else knight_b_pst[i][j]
    return cpt if player == AI_PLAYER else -cpt

rook_w_pst = [
    [0,   0,  0,  0,  0,  0,  0,  0],
    [5,  10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,   0,  0,  5,  5,  0,  0,  0]
]

rook_b_pst = [rook_w_pst[i] for i in reversed(range(8))]

def rook_score(game_info, player):
    board = game_info[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "R":
                cpt += rook_w_pst[i][j] if player == 1 else rook_b_pst[i][j]
    return cpt if player == AI_PLAYER else -cpt

queen_w_pst = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,   0,  5,  5,  5,  5,  0, -5],
    [ 0,   0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

queen_b_pst = [queen_w_pst[i] for i in reversed(range(8))]

def queen_score(game_info, player):
    board = game_info[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "Q":
                cpt += queen_w_pst[i][j] if player == 1 else queen_b_pst[i][j]
    return cpt if player == AI_PLAYER else -cpt

king_w_pst_opening = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

king_b_pst_opening = [king_w_pst_opening[i] for i in reversed(range(8))]

king_w_pst_ending = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

king_b_pst_ending = [king_w_pst_ending[i] for i in reversed(range(8))]

def king_score(game_info, player):
    board = game_info[0]
    cpt = 0
    opening_phase = game_info[4][-1][0] * 100 <= 2000 and game_info[4][-1][1] * 100 <= 2000
    for i in range(8):
        for j in range(8):
            if board[i][j][1] == "K":
                if opening_phase:
                    cpt += king_w_pst_opening[i][j] if player == 1 else king_b_pst_opening[i][j]
                else:
                    cpt += king_w_pst_ending[i][j] if player == 1 else king_b_pst_ending[i][j]
    return cpt if player == AI_PLAYER else -cpt
