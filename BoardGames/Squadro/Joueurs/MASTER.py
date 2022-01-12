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
DISTANCE_AI     =  1.00
DISTANCE_OP     =  1.00
SCORE_AI        =  1.00
SCORE_OP        =  1.00
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

#WEIGHTS = [DISTANCE_AI, DISTANCE_OP, SCORE_AI, SCORE_OP]
WEIGHTS = [0.5423951311022498, 0.279653976578467, 0.7472380135785962, 0.901115667929279]

PLIES = 7
NB_NOEUDS = 0

############################################################################

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.getJoueur(jeu)
    OPPONENT = AI_PLAYER%2 + 1

    return decision(jeu, -INFINITY, INFINITY)

def decision(jeu, alpha, beta):
    vmax = -INFINITY
    bestCoup = None

    for coup in game.getCoupsValides(jeu):
        global NB_NOEUDS
        NB_NOEUDS += 1
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)

        v = minimax(j, PLIES-1, False, alpha, beta)
        if v > vmax:
            vmax = v
            bestCoup = coup
        if v > alpha:
            alpha = v

    return bestCoup

def minimax(jeu, plies, maximizingPlayer, alpha, beta):
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

            v = minimax(j, plies-1, False, alpha, beta)
            if v > vmax: vmax = v
            if v >= beta: return v # beta cutoff
            if v > alpha: alpha = v

        return vmax

    else:
        vmin = INFINITY
        for coup in game.getCoupsValides(jeu):
            NB_NOEUDS += 1
            j = game.getCopieJeu(jeu)
            game.joueCoup(j, coup)

            v = minimax(j, plies-1, True, alpha, beta)
            if v < vmin: vmin = v
            if v <= alpha: return v # alpha cutoff
            if v < beta: beta = v

        return vmin

############################################################################

def getInputs(jeu):
    return [distance(jeu, AI_PLAYER), distance(jeu, OPPONENT), score(jeu, AI_PLAYER), score(jeu, OPPONENT)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def distance(jeu, player):
    cpt_j = 0
    cpt_r = 0
    plateau = jeu[0]

    for i in range(1, 6):
        empty = True
        for j in range(7):
            if plateau[i][j][0] == "j":
                empty = False
                if plateau[i][j][1] == "+":
                    cpt_j = cpt_j + j
                else:
                    cpt_j = cpt_j + 12-j
                break
        if empty:
            cpt_j += 12

    for j in range(1, 6):
        empty = True
        for i in range(7):
            if plateau[i][j][0] == "r":
                empty = False
                if plateau[i][j][1] == "+":
                    cpt_r = cpt_r + 6-i
                else:
                    cpt_r = cpt_r + 6+i
                break
        if empty:
            cpt_r += 12

    s = [cpt_j, cpt_r][player-1]
    return s if player == AI_PLAYER else -s

def score(jeu, player):
    cpt = 100 * game.getScore(jeu, player)
    return cpt if player == AI_PLAYER else -cpt
