#!/usr/bin/env python
# -*- coding: utf-8 -*-
import game

####### WEIGHTS #######
W1  = 0.06 #OP_2SEEDS
W2  = 0.20 #OP_3SEEDS
W3  = 0.93 #AI_2SEEDS
W4  = 0.93 #AI_3SEEDS
W5  = 0.13 #OP_REACH
W6  = 0.87 #AI_REACH
W7  = 0.06 #OP_KROOS
W8  = 0.93 #AI_KROOS
W9  = 0.13 #OP_SCORE
W10 = 0.60 #AI_SCORE
W11 = 1.00 #OP_EMPTY
W12 = 0.67 #AI_EMPTY
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

# WEIGHTS FOR PLIES=3
WEIGHTS = [W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12]

# WEIGHTS FOR PLIES=5
# WEIGHTS = [0.80,1.00,0.06,0.00,0.87,0.60,0.00,0.20,0.73,0.93,0.00,0.80]

PLIES = 3
NUM_NODES = 0

############################################################################

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.get_player(game_info)
    OPPONENT = AI_PLAYER%2 + 1

    return decision(game_info)

def decision(game_info):
    vmax = -INFINITY
    bestCoup = None

    for move in game.get_valid_moves(game_info):
        global NUM_NODES
        NUM_NODES += 1
        j = game.get_game_copy(game_info)
        game.play_move(j, move)

        v = minimax(j, PLIES-1, False)
        if v > vmax:
            vmax = v
            bestCoup = move

    return bestCoup

def minimax(game_info, plies, maximizingPlayer):
	####### GOAL STATE EVALUATION #######
    if game.is_game_over(game_info):
        winner = game.get_winner(game_info)
        if winner == AI_PLAYER:
            return 10000 - plies # winning A$AP
        elif winner == 0:
            return 0
        else:
            return plies - 10000
	####################################

    if plies == 0:
        return heuristic(game_info)

    global NUM_NODES
    if maximizingPlayer:
        vmax = -INFINITY
        for move in game.get_valid_moves(game_info):
            NUM_NODES += 1
            j = game.get_game_copy(game_info)
            game.play_move(j, move)

            v = minimax(j, plies-1, False)
            if v > vmax:
                vmax = v

        return vmax

    else:
        vmin = INFINITY
        for move in game.get_valid_moves(game_info):
            NUM_NODES += 1
            j = game.get_game_copy(game_info)
            game.play_move(j, move)

            v = minimax(j, plies-1, True)
            if v < vmin:
                vmin = v

        return vmin

############################################################################

def getInputs(game_info):
    return [h1(game_info), h2(game_info), h3(game_info), h4(game_info), h5(game_info), h6(game_info),
            h7(game_info), h8(game_info), h9(game_info), h10(game_info), h11(game_info), h12(game_info)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(game_info)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def h1(game_info):
    """ The number of pits that the opponent can use to capture 2 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            if case != move:
                seeds -= 1
        if case[0] != move[0] and game_info[0][case[0]][case[1]] == 1:
            cpt += 1

    return -cpt

def h2(game_info):
    """ The number of pits that the opponent can use to capture 3 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            if case != move:
                seeds -= 1
        if case[0] != move[0] and game_info[0][case[0]][case[1]] == 2:
            cpt += 1

    return -cpt

def h3(game_info):
    """ The number of pits that ayo can use to capture 2 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            if case != move:
                seeds -= 1
        if case[0] != move[0] and game_info[0][case[0]][case[1]] == 1:
            cpt += 1

    return cpt

def h4(game_info):
    """ The number of pits that ayo can use to capture 3 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            if case != move:
                seeds -= 1
        if case[0] != move[0] and game_info[0][case[0]][case[1]] == 2:
            cpt += 1

    return cpt

def h5(game_info):
    """ The number of pits on the opponent’s side with enough seeds to reach to ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            seeds -= 1
            if case[0] != move[0]:
                cpt += 1
                break

    return -cpt

def h6(game_info):
    """ The number of pits on ayo’s side with enough seeds to reach the opponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            continue
        case = (row, col)
        move = (row, col)
        while seeds > 0:
            case = game.game.next_pit(case[0], case[1])
            seeds -= 1
            if case[0] != move[0]:
                cpt += 1
                break

    return cpt

def h7(game_info):
    """ The number of pits with more than 12 seeds on the opponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds > 12:
            cpt += 1

    return -cpt

def h8(game_info):
    """ The number of pits with more than 12 seeds on ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds > 12:
            cpt += 1

    return cpt

def h9(game_info):
    """ The current score of the opponent.
        Range: 0 – 48.
    """
    return -game.get_score(game_info, OPPONENT)

def h10(game_info):
    """ The current score of ayo.
        Range: 0 – 48.
    """
    return game.get_score(game_info, AI_PLAYER)

def h11(game_info):
    """ The number of empty pits on the oponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            cpt += 1

    return cpt

def h12(game_info):
    """ The number of empty pits on ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        seeds = game.get_position_value(game_info, row, col)
        if seeds == 0:
            cpt += 1

    return -cpt
