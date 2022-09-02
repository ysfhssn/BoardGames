#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Players'))
import game
import awele
import random
import minimax_ab, negamax_ab, minimax_ab_order
import ayo_ab, master
import time
import random
from tqdm import tqdm


game.game = awele
game.player1 = ayo_ab
game.player2 = master


# generate solutions
NB_SOLUTIONS = 10
solutions = []
n = len(game.player1.WEIGHTS)
for _ in range(NB_SOLUTIONS):
    solutions.append([random.uniform(0,1) for _ in range(n)])


# Il y aura 2*NUM_ROUNDS*NB_SOLUTIONS parties
NUM_ROUNDS = 5
def fitness():
    SCORE = 0

    for i in range(NUM_ROUNDS):
        game_info = game.init()

        while not game.is_game_over(game_info):
            if len(game.get_played_moves(game_info)) <= 4:
                move = random.get_move(game_info)
            else:
                move = game.get_move(game_info)
            game.play_move(game_info, move)

        winner = game.get_winner(game_info)

        if winner == 1:
            SCORE += 1


    game.player1, game.player2 = game.player2, game.player1
    for i in range(NUM_ROUNDS):
        game_info = game.init()

        while not game.is_game_over(game_info):
            if len(game.get_played_moves(game_info)) <= 4:
                move = random.get_move(game_info)
            else:
                move = game.get_move(game_info)
            game.play_move(game_info, move)

        winner = game.get_winner(game_info)

        if winner == 2:
            SCORE += 1

    game.player1, game.player2 = game.player2, game.player1
    return SCORE


start = time.time()

NB_GEN = 2
THRESHOLD_FITNESS = 0.8 * 2 * NUM_ROUNDS // 1
print(f"NUM_ROUNDS = {2 * NUM_ROUNDS}")
print(f"THRESHOLD_FITNESS = {THRESHOLD_FITNESS}")

for i in range(NB_GEN):
    ranked_solutions = []
    for s in tqdm(solutions):
        game.player1.WEIGHTS = s
        fitn = fitness()
        ranked_solutions.append((fitn, s))

    ranked_solutions.sort(reverse=True)
    print(f"=== GEN {i+1} === 3 best solutions ===")
    for rs in ranked_solutions[:3]:
        print(rs)

    if ranked_solutions[0][0] >= THRESHOLD_FITNESS:
        break

    # Crossovers and mutations
    best_solutions = ranked_solutions[:3]
    genes1 = []
    genes2 = []
    genes3 = []
    genes4 = []
    genes5 = []
    genes6 = []
    genes7 = []
    genes8 = []
    genes9 = []
    genes10 = []
    genes11 = []
    genes12 = []
    for rs in best_solutions:
        genes1.append(rs[1][0])
        genes2.append(rs[1][1])
        genes3.append(rs[1][2])
        genes4.append(rs[1][3])
        genes5.append(rs[1][4])
        genes6.append(rs[1][5])
        genes7.append(rs[1][6])
        genes8.append(rs[1][7])
        genes9.append(rs[1][8])
        genes10.append(rs[1][9])
        genes11.append(rs[1][10])
        genes12.append(rs[1][11])

    new_generation = []
    mutation_rate = random.uniform(0.99, 1.01)
    for _ in range(NB_SOLUTIONS//2):
        g1 = random.choice(genes1) * mutation_rate
        g2 = random.choice(genes2) * mutation_rate
        g3 = random.choice(genes3) * mutation_rate
        g4 = random.choice(genes4) * mutation_rate
        g5 = random.choice(genes5) * mutation_rate
        g6 = random.choice(genes6) * mutation_rate
        g7 = random.choice(genes7) * mutation_rate
        g8 = random.choice(genes8) * mutation_rate
        g9 = random.choice(genes9) * mutation_rate
        g10 = random.choice(genes10) * mutation_rate
        g11 = random.choice(genes11) * mutation_rate
        g12 = random.choice(genes12) * mutation_rate
        new_generation.append([g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12])

    solutions = new_generation

end = time.time()
print(f"\nTemps: {(end-start)/60} minutes")

"""
                                                DEPTH 4
    CONTRE master:
            [0.5534748381291195, 0.4616523993252173, 0.49302249597961767, 0.6862599526142863, 0.3444121846742263, 0.721958905863068, 0.6509160093379074, 0.44053105064314346, 0.6506520262665414, 0.5194329933897871, 0.355696633999106, 0.7590032048352058]

=== GEN 1 === 3 best solutions ===
(5, [0.4746814056431268, 0.08439711520556892, 0.37188504383785304, 0.5361242338096542, 0.2015216534775638, 0.33869936730318495, 0.13044501884469184, 0.7366210651089573, 0.33302626772612876, 0.8811074941336178, 0.17292341457415472, 0.3527073517297321])
(5, [0.3629896622951405, 0.5460233393759555, 0.2582546488803469, 0.014193906570616144, 0.6158182971869506, 0.06469030488498273, 0.3140272907474593, 0.03668154951482461, 0.5024514150150688, 0.3983320325096431, 0.8003992606869791, 0.5519372799935668])
(4, [0.6181246226825173, 0.8840541044629479, 0.24739152341908366, 0.19462225033223268, 0.2808294023833151, 0.06252527973225486, 0.9962916467394782, 0.5690770842848133, 0.66011648869301, 0.09964392425999646, 0.7233205659079345, 0.9509080775604748])

=== GEN 2 === 3 best solutions ===
(8, [0.6144990095777895, 0.08390208349891629, 0.3697037502298756, 0.19348069253727876, 0.2003396271985201, 0.06431086357406718, 0.1296798929260424, 0.5657391597649498, 0.6562445720855371, 0.8759393536645629, 0.17190913141022976, 0.9453305214158368])
(6, [0.47189715945438643, 0.08390208349891629, 0.2567398549294539, 0.5329795944011367, 0.6122062118460969, 0.062158537387337016, 0.1296798929260424, 0.5657391597649498, 0.49950428369572103, 0.3959956139556752, 0.7957045147699381, 0.3506385449719369])
(4, [0.6144990095777895, 0.08390208349891629, 0.2459404471855981, 0.5329795944011367, 0.6122062118460969, 0.062158537387337016, 0.9904478930399837, 0.7323004105210728, 0.6562445720855371, 0.8759393536645629, 0.17190913141022976, 0.3506385449719369])

Temps: 30.120272394021352 minutes
"""
