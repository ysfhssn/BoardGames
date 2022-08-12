import game
if game.GUI: import pygame

####### WEIGHTS #######
DISTANCE_AI     =  1.00
DISTANCE_OP     =  1.00
SCORE_AI        =  1.00
SCORE_OP        =  1.00
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

WEIGHTS = [DISTANCE_AI, DISTANCE_OP, SCORE_AI, SCORE_OP]

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
    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None

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
    return [distance(jeu, AI_PLAYER), distance(jeu, OPPONENT), score_ai(jeu), score_op(jeu)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def distance(jeu, player):
    cpt = 0
    plateau = jeu[0]

    if player == 1:
        for i in range(1, 6):
            empty = True
            for j in range(7):
                if plateau[i][j][0] == "j":
                    empty = False
                    if plateau[i][j][1] == "+":
                        cpt = cpt + j
                    else:
                        cpt = cpt + 12-j
                    break
            if empty:
                cpt += 12

    else:
        for j in range(1, 6):
            empty = True
            for i in range(7):
                if plateau[i][j][0] == "r":
                    empty = False
                    if plateau[i][j][1] == "+":
                        cpt = cpt + 6-i
                    else:
                        cpt = cpt + 6+i
                    break
            if empty:
                cpt += 12

    return cpt if player == AI_PLAYER else -cpt

def score_ai(jeu):
    return 100 * game.getScore(jeu, AI_PLAYER)

def score_op(jeu):
    return -100 * game.getScore(jeu, OPPONENT)
