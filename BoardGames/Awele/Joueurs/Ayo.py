#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(grandparent)
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
NB_NOEUDS = 0

############################################################################

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.getJoueur(jeu)
    OPPONENT = AI_PLAYER%2 + 1

    return decision(jeu)

def decision(jeu):
    vmax = -INFINITY
    bestCoup = None

    for coup in game.getCoupsValides(jeu):
        global NB_NOEUDS
        NB_NOEUDS += 1
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)

        v = minimax(j, PLIES-1, False)
        if v > vmax:
            vmax = v
            bestCoup = coup

    return bestCoup

def minimax(jeu, plies, maximizingPlayer):
	####### GOAL STATE EVALUATION #######
    if game.finJeu(jeu):
        winner = game.getGagnant(jeu)
        if winner == AI_PLAYER:
            return 10000 - plies # winning A$AP
        elif winner == 0:
            return 0
        else:
            return plies - 10000
	####################################

    if plies == 0:
        return heuristic(jeu)

    global NB_NOEUDS
    if maximizingPlayer:
        vmax = -INFINITY
        for coup in game.getCoupsValides(jeu):
            NB_NOEUDS += 1
            j = game.getCopieJeu(jeu)
            game.joueCoup(j, coup)

            v = minimax(j, plies-1, False)
            if v > vmax:
                vmax = v

        return vmax

    else:
        vmin = INFINITY
        for coup in game.getCoupsValides(jeu):
            NB_NOEUDS += 1
            j = game.getCopieJeu(jeu)
            game.joueCoup(j, coup)

            v = minimax(j, plies-1, True)
            if v < vmin:
                vmin = v

        return vmin

############################################################################

def getInputs(jeu):
    return [h1(jeu), h2(jeu), h3(jeu), h4(jeu), h5(jeu), h6(jeu),
            h7(jeu), h8(jeu), h9(jeu), h10(jeu), h11(jeu), h12(jeu)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def h1(jeu):
    """ The number of pits that the opponent can use to capture 2 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            if case != coup:
                grains -= 1
        if case[0] != coup[0] and jeu[0][case[0]][case[1]] == 1:
            cpt += 1

    return -cpt

def h2(jeu):
    """ The number of pits that the opponent can use to capture 3 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            if case != coup:
                grains -= 1
        if case[0] != coup[0] and jeu[0][case[0]][case[1]] == 2:
            cpt += 1

    return -cpt

def h3(jeu):
    """ The number of pits that Ayo can use to capture 2 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            if case != coup:
                grains -= 1
        if case[0] != coup[0] and jeu[0][case[0]][case[1]] == 1:
            cpt += 1

    return cpt

def h4(jeu):
    """ The number of pits that Ayo can use to capture 3 seeds.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            if case != coup:
                grains -= 1
        if case[0] != coup[0] and jeu[0][case[0]][case[1]] == 2:
            cpt += 1

    return cpt

def h5(jeu):
    """ The number of pits on the opponent’s side with enough seeds to reach to Ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            grains -= 1
            if case[0] != coup[0]:
                cpt += 1
                break

    return -cpt

def h6(jeu):
    """ The number of pits on Ayo’s side with enough seeds to reach the opponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            continue
        case = (row, col)
        coup = (row, col)
        while grains > 0:
            case = game.game.nextCase(case[0], case[1])
            grains -= 1
            if case[0] != coup[0]:
                cpt += 1
                break

    return cpt

def h7(jeu):
    """ The number of pits with more than 12 seeds on the opponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains > 12:
            cpt += 1

    return -cpt

def h8(jeu):
    """ The number of pits with more than 12 seeds on Ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains > 12:
            cpt += 1

    return cpt

def h9(jeu):
    """ The current score of the opponent.
        Range: 0 – 48.
    """
    return -game.getScore(jeu, OPPONENT)

def h10(jeu):
    """ The current score of Ayo.
        Range: 0 – 48.
    """
    return game.getScore(jeu, AI_PLAYER)

def h11(jeu):
    """ The number of empty pits on the oponent’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = OPPONENT - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            cpt += 1

    return cpt

def h12(jeu):
    """ The number of empty pits on Ayo’s side.
        Range: 0 – 6.
    """
    cpt = 0
    row = AI_PLAYER - 1
    for col in range(6):
        grains = game.getCaseVal(jeu, row, col)
        if grains == 0:
            cpt += 1

    return -cpt

