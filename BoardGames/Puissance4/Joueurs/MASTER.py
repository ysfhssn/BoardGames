import game
if game.GUI: import pygame
from Puissance4.puissance4 import N, ROWS, COLS

####### WEIGHTS #######
AI_PIECES   = 1
OP_PIECES   = 1
#######################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")

WEIGHTS = [AI_PIECES, OP_PIECES]

PLIES = 6
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
    return [pieces(jeu, AI_PLAYER), pieces(jeu, OPPONENT)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def pieces(jeu, player):
    board = jeu[0]
    cpt = 0

    # Check horizontal locations for win
    for c in range(COLS-(N-1)):
        for r in range(ROWS):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r][c+i] for i in range(N)]
            cpt += line.count(player)

	# Check vertical locations for win
    for c in range(COLS):
        for r in range(ROWS-(N-1)):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r+i][c] for i in range(N)]
            cpt += line.count(player)

	# Check negatively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(ROWS-(N-1)):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r+i][c+i] for i in range(N)]
            cpt += line.count(player)

	# Check positively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(N-1, ROWS):
            joueur = board[r][c]
            if joueur == 0: continue
            line = [board[r-i][c+i] for i in range(N)]
            cpt += line.count(player)

    return cpt if player == AI_PLAYER else -cpt
