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
D_SCORE         = 1.00
D_GRAINS        = 0.00
AI_WEAK_PITS    = 0.00
OP_WEAK_PITS    = 0.00
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

WEIGHTS = [D_SCORE, D_GRAINS, AI_WEAK_PITS, OP_WEAK_PITS]

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

    return decision(jeu, -INFINITY, INFINITY)

def decision(jeu, alpha, beta):
    vmax = -INFINITY
    bestCoup = None

    for coup in game.getCoupsValides(jeu):
        global NB_NOEUDS
        NB_NOEUDS += 1
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)

        v = -negamax(j, PLIES-1, -1, -beta, -alpha)
        if v > vmax:
            vmax = v
            bestCoup = coup
        if v > alpha:
            alpha = v

    return bestCoup

def negamax(jeu, plies, color, alpha, beta):
    ####### GOAL STATE EVALUATION #######
    if game.finJeu(jeu):
        winner = game.getGagnant(jeu)
        if winner == AI_PLAYER:
            return color * (10000 - plies) # winning A$AP
        elif winner == 0:
            return 0
        else:
            return color * (plies - 10000)
    ####################################

    if plies == 0:
        return color * heuristic(jeu)

    global NB_NOEUDS
    vmax = -INFINITY
    for coup in game.getCoupsValides(jeu):
        NB_NOEUDS += 1
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)

        v = -negamax(j, plies-1, -color, -beta, -alpha)
        vmax = max(vmax, v)
        alpha = max(alpha, vmax)
        if alpha >= beta:
            break

    return vmax


############################################################################

def getInputs(jeu):
    return [d_scores(jeu), d_grains(jeu), ai_wk_pits(jeu), op_wk_pits(jeu)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))


def d_scores(jeu):
    return game.getScore(jeu, AI_PLAYER) - game.getScore(jeu, OPPONENT)

def d_grains(jeu):
    return sum(jeu[0][AI_PLAYER-1]) - sum(jeu[0][OPPONENT-1])

def ai_wk_pits(jeu):
    cpt = 0
    for grains in jeu[0][AI_PLAYER-1]:
        if grains <= 2:
            cpt += 1
    return -cpt

def op_wk_pits(jeu):
    cpt = 0
    for grains in jeu[0][OPPONENT-1]:
        if grains <= 2:
            cpt += 1
    return cpt