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

def order_coups(jeu, coupsPossibles, reverse):
    ranked_coups = []
    for coup in coupsPossibles:
        copyJeu = game.getCopieJeu(jeu)
        game.joueCoup(copyJeu, coup)
        d_score = game.getScore(copyJeu, AI_PLAYER) - game.getScore(copyJeu, OPPONENT)
        ranked_coups.append((d_score, coup))
    ranked_coups.sort(reverse=reverse)
    return [rc[1] for rc in ranked_coups]

def decision(jeu, alpha, beta):
    vmax = -INFINITY
    bestCoup = None

    for coup in order_coups(jeu, game.getCoupsValides(jeu), True):
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

def minimax(jeu, plies, maximizingPlayer, alpha, beta):    ####### GOAL STATE EVALUATION #######
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

"""
        10 PARTIES
    TEMPS TOTAL (en secondes)
TRI_PLIE_1      : 23.13
NO_TRI          : 28.2s
TRI_ALL_PLIES   : 41.13

"""
