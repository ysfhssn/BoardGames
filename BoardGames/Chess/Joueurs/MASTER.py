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
    return [score(jeu, AI_PLAYER), score(jeu, OPPONENT), pawn_score(jeu, AI_PLAYER), knight_score(jeu, AI_PLAYER),
            bishop_score(jeu, AI_PLAYER), rook_score(jeu, AI_PLAYER), queen_score(jeu, AI_PLAYER), king_score(jeu, AI_PLAYER)]

def heuristic(jeu):
    """ Linear combination of weights and elementary heuristics """
    inputs = getInputs(jeu)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def score(jeu, player):
    cpt = jeu[4][player-1+2]
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

def pawn_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "P":
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

def knight_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "N":
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

def bishop_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "B":
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

def rook_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "R":
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

def queen_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "Q":
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

def king_score(jeu, player):
    plateau = jeu[0]
    cpt = 0
    opening_phase = jeu[4][2] <= 2000 and jeu[4][3] <= 2000
    for i in range(8):
        for j in range(8):
            if plateau[i][j][1] == "K":
                if opening_phase:
                    cpt += king_w_pst_opening[i][j] if player == 1 else king_b_pst_opening[i][j]
                else:
                    cpt += king_w_pst_ending[i][j] if player == 1 else king_b_pst_ending[i][j]
    return cpt if player == AI_PLAYER else -cpt
