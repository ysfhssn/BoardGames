import game
if game.GUI: import pygame

####### WEIGHTS #######
POSITIONAL      = 1.00
D_SCORE         = 0.00
D_MOBILITY      = 0.00
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

WEIGHTS = [POSITIONAL, D_SCORE, D_MOBILITY]

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
    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None

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
    return [positional(jeu), d_scores(jeu), d_mobility(jeu)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))


BOARD_WEIGHTS = [
    [ 100, -10, 11,  6,  6, 11, -10, 100 ],
    [ -10, -20,  1,  2,  2,  1, -20, -10 ],
    [  10,   1,  5,  4,  4,  5,   1,  10 ],
    [   6,   2,  4,  2,  2,  4,   2,   6 ],
    [   6,   2,  4,  2,  2,  4,   2,   6 ],
    [  10,   1,  5,  4,  4,  5,   1,  10 ],
    [ -10, -20,  1,  2,  2,  1, -20, -10 ],
    [ 100, -10, 11,  6,  6, 11, -10, 100 ]
]

def positional(jeu):
    cpt = 0
    board = jeu[0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == AI_PLAYER:
                cpt += BOARD_WEIGHTS[i][j]
            if board[i][j] == OPPONENT:
                cpt -= BOARD_WEIGHTS[i][j]
    return cpt

def d_scores(jeu):
    return game.getScore(jeu, AI_PLAYER) - game.getScore(jeu, OPPONENT)

def d_mobility(jeu):
    j = game.getCopieJeu(jeu)
    j[1] = AI_PLAYER
    m_ai = len(game.getCoupsValides(j))
    j[1] = OPPONENT
    m_op = len(game.getCoupsValides(j))

    c_ai = 0
    c_op = 0
    board = jeu[0]
    for i in [0, 7]:
        for j in [0, 7]:
            if board[i][j] == AI_PLAYER:
                c_ai += 1
            elif board[i][j] == OPPONENT:
                c_op += 1

    return 10 * (c_ai - c_op) + (m_ai - m_op)/(m_ai + m_op)
