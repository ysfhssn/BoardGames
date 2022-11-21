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
    return [pieces(game_info, AI_PLAYER), pieces(game_info, OPPONENT)]

def heuristic(game_info):
    """ Linear combination of weights and elementary heuristics """
    inputs = get_inputs(game_info)
    assert(len(inputs) == len(WEIGHTS))
    return sum(h * w for h, w in zip(inputs, WEIGHTS))

def pieces(game_info, player):
    board = game_info[0]
    cpt = 0

    # Check horizontal positions for win
    for c in range(COLS-(N-1)):
        for r in range(ROWS):
            player = board[r][c]
            if player == 0: continue
            line = [board[r][c+i] for i in range(N)]
            cpt += line.count(player)

	# Check vertical positions for win
    for c in range(COLS):
        for r in range(ROWS-(N-1)):
            player = board[r][c]
            if player == 0: continue
            line = [board[r+i][c] for i in range(N)]
            cpt += line.count(player)

	# Check negatively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(ROWS-(N-1)):
            player = board[r][c]
            if player == 0: continue
            line = [board[r+i][c+i] for i in range(N)]
            cpt += line.count(player)

	# Check positively sloped diaganols
    for c in range(COLS-(N-1)):
        for r in range(N-1, ROWS):
            player = board[r][c]
            if player == 0: continue
            line = [board[r-i][c+i] for i in range(N)]
            cpt += line.count(player)

    return cpt if player == AI_PLAYER else -cpt
