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

#WEIGHTS = [DISTANCE_AI, DISTANCE_OP, SCORE_AI, SCORE_OP]
WEIGHTS = [0.5423951311022498, 0.279653976578467, 0.7472380135785962, 0.901115667929279]

PLIES = 7
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

        v = minimax(j, PLIES-1, False, alpha, beta)
        if v > vmax:
            vmax = v
            bestMove = move
    if game.GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None

    return bestMove

def minimax(game_info, plies, maximizingPlayer, alpha, beta):	####### GOAL STATE EVALUATION #######
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

            v = minimax(j, plies-1, False, alpha, beta)
            if v > vmax: vmax = v
            if v >= beta: return v # beta cutoff
            if v > alpha: alpha = v

        return vmax

    else:
        vmin = INFINITY
        for move in game.get_valid_moves(game_info):
            NUM_NODES += 1
            j = game.get_game_copy(game_info)
            game.play_move(j, move)

            v = minimax(j, plies-1, True, alpha, beta)
            if v < vmin: vmin = v
            if v <= alpha: return v # alpha cutoff
            if v < beta: beta = v

        return vmin

############################################################################

def get_inputs(game_info):
    return [distance(game_info, AI_PLAYER), distance(game_info, OPPONENT), score(game_info, AI_PLAYER), score(game_info, OPPONENT)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = get_inputs(game_info)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def distance(game_info, player):
    cpt_j = 0
    cpt_r = 0
    board = game_info[0]

    for i in range(1, 6):
        empty = True
        for j in range(7):
            if board[i][j][0] == "j":
                empty = False
                if board[i][j][1] == "+":
                    cpt_j = cpt_j + j
                else:
                    cpt_j = cpt_j + 12-j
                break
        if empty:
            cpt_j += 12

    for j in range(1, 6):
        empty = True
        for i in range(7):
            if board[i][j][0] == "r":
                empty = False
                if board[i][j][1] == "+":
                    cpt_r = cpt_r + 6-i
                else:
                    cpt_r = cpt_r + 6+i
                break
        if empty:
            cpt_r += 12

    s = [cpt_j, cpt_r][player-1]
    return s if player == AI_PLAYER else -s

def score(game_info, player):
    cpt = 100 * game.get_score_player(game_info, player)
    return cpt if player == AI_PLAYER else -cpt
