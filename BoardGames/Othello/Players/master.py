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

def minimax(game_info, plies, maximizingPlayer, alpha, beta):
	####### GOAL STATE EVALUATION #######
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
    return [positional(game_info), d_scores(game_info), d_mobility(game_info)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = get_inputs(game_info)
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

def positional(game_info):
    cpt = 0
    board = game_info[0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == AI_PLAYER:
                cpt += BOARD_WEIGHTS[i][j]
            if board[i][j] == OPPONENT:
                cpt -= BOARD_WEIGHTS[i][j]
    return cpt

def d_scores(game_info):
    return game.get_score_player(game_info, AI_PLAYER) - game.get_score_player(game_info, OPPONENT)

def d_mobility(game_info):
    j = game.get_game_copy(game_info)
    j[1] = AI_PLAYER
    m_ai = len(game.get_valid_moves(j))
    j[1] = OPPONENT
    m_op = len(game.get_valid_moves(j))

    c_ai = 0
    c_op = 0
    board = game_info[0]
    for i in [0, 7]:
        for j in [0, 7]:
            if board[i][j] == AI_PLAYER:
                c_ai += 1
            elif board[i][j] == OPPONENT:
                c_op += 1

    return 10 * (c_ai - c_op) + (m_ai - m_op)/(m_ai + m_op)
