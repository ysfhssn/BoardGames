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
NUM_NODES = 0

############################################################################

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.get_player(game_info)
    OPPONENT = AI_PLAYER%2 + 1

    return decision(game_info, -INFINITY, INFINITY)

def decision(game_info, alpha, beta):
    vmax = -INFINITY
    bestMove = None

    for move in game.get_valid_moves(game_info):
        global NUM_NODES
        NUM_NODES += 1
        j = game.get_game_copy(game_info)
        game.play_move(j, move)

        v = -negamax(j, PLIES-1, -1, -beta, -alpha)
        if v > vmax:
            vmax = v
            bestMove = move
        if v > alpha:
            alpha = v

    return bestMove

def negamax(game_info, plies, color, alpha, beta):
    ####### GOAL STATE EVALUATION #######
    if game.is_game_over(game_info):
        winner = game.get_winner(game_info)
        if winner == AI_PLAYER:
            return color * (10000 - plies) # winning A$AP
        elif winner == 0:
            return 0
        else:
            return color * (plies - 10000)
    ####################################

    if plies == 0:
        return color * heuristic(game_info)

    global NUM_NODES
    vmax = -INFINITY
    for move in game.get_valid_moves(game_info):
        NUM_NODES += 1
        j = game.get_game_copy(game_info)
        game.play_move(j, move)

        v = -negamax(j, plies-1, -color, -beta, -alpha)
        vmax = max(vmax, v)
        alpha = max(alpha, vmax)
        if alpha >= beta:
            break

    return vmax


############################################################################

def get_inputs(game_info):
    return [d_scores(game_info), d_grains(game_info), ai_wk_pits(game_info), op_wk_pits(game_info)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = get_inputs(game_info)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))


def d_scores(game_info):
    return game.get_score_player(game_info, AI_PLAYER) - game.get_score_player(game_info, OPPONENT)

def d_grains(game_info):
    return sum(game_info[0][AI_PLAYER-1]) - sum(game_info[0][OPPONENT-1])

def ai_wk_pits(game_info):
    cpt = 0
    for seeds in game_info[0][AI_PLAYER-1]:
        if seeds <= 2:
            cpt += 1
    return -cpt

def op_wk_pits(game_info):
    cpt = 0
    for seeds in game_info[0][OPPONENT-1]:
        if seeds <= 2:
            cpt += 1
    return cpt
