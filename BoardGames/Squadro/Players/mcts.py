import game
import math
import random

#####################
NB_ITERATIONS = 1000
NB_ROLLOUTS = 1
#####################

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")
SQRT2 = math.sqrt(2)



c = SQRT2
def UCB1(Si):
    if Si.ni == 0 or Si.parent.ni is None: return INFINITY
    return Si.wi/Si.ni + c*math.sqrt(math.log(Si.parent.ni/Si.ni))

class Node:
    def __init__(self, game_info, parent=None):
        self.game_info = game_info
        self.parent = parent
        self.children = []
        self.wi = 0
        self.ni = 0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_random_child(self):
        return random.choice(self.children) if self.children else None

    def get_max_child(self):
        if not self.children: return None
        return max(self.children, key=lambda c: UCB1(c))



def get_move(game_info):
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.get_player(game_info)
    OPPONENT = AI_PLAYER%2 + 1

    # Init
    ROOT = Node(game_info)
    for move in game.get_valid_moves(game_info):
        j = game.get_game_copy(game_info)
        game.play_move(j, move)
        ROOT.add_child(Node(j))

    # Selection - Expansion - Rollout - Backpropagation
    for _ in range(NB_ITERATIONS):
        leaf = select(ROOT)

        if game.is_game_over(leaf.game_info):
            backpropagate(leaf, NB_ROLLOUTS) if game.get_winner(leaf.game_info) == AI_PLAYER else backpropagate(leaf, 0)
            continue

        if leaf.ni == 0:
            score = rollout(leaf)
        else:
            children = expand(leaf)
            score = rollout(children[0])

        backpropagate(leaf, score)

    # Best move
    vmax = -INFINITY
    bestCoup = None
    for c in ROOT.children:
        if c.ni > vmax:
            vmax = c.ni
            bestCoup = c.game_info[3][-1]
    return bestCoup

def select(root):
    node = root
    while node.children:
        node = node.get_max_child()
    return node

def expand(leaf):
    game_info = leaf.game_info
    for move in game.get_valid_moves(game_info):
        j = game.get_game_copy(game_info)
        game.play_move(j, move)
        leaf.add_child(Node(j))
    return leaf.children

def rollout(leaf):
    game_info = leaf.game_info
    score = 0
    for _ in range(NB_ROLLOUTS):
        j = game.get_game_copy(game_info)
        while not game.is_game_over(j):
            move = random.choice(game.get_valid_moves(j))
            game.play_move(j, move)
        if game.get_winner(j) == AI_PLAYER: score += 1
    return score

def backpropagate(leaf, score):
    node = leaf
    while node is not None:
        node.wi += score
        node.ni += 1
        node = node.parent
