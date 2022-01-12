#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Joueurs'))
import game
import awele
import joueur_random
import joueur_minimax_ab, joueur_negamax_ab, joueur_minimax_ab_order
import Ayo_ab, MASTER
import time
import random
from tqdm import tqdm


game.game = awele
game.joueur1 = joueur_minimax_ab
game.joueur2 = joueur_negamax_ab


# generate solutions
NB_SOLUTIONS = 10
solutions = []
for _ in range(NB_SOLUTIONS):
    solutions.append([random.uniform(0,1),
                      random.uniform(0,1),
                      random.uniform(0,1),
                      random.uniform(0,1)])


# Il y aura 2*NB_PARTIES*NB_SOLUTIONS parties
NB_PARTIES = 5
def fitness():
    SCORE = 0

    for i in range(NB_PARTIES):
        jeu = game.initialiseJeu()

        while not game.finJeu(jeu):
            if len(game.getCoupsJoues(jeu)) <= 4:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)

        gagnant = game.getGagnant(jeu)

        if gagnant == 1:
            SCORE += 1


    game.joueur1, game.joueur2 = game.joueur2, game.joueur1
    for i in range(NB_PARTIES):
        jeu = game.initialiseJeu()

        while not game.finJeu(jeu):
            if len(game.getCoupsJoues(jeu)) <= 4:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)

        gagnant = game.getGagnant(jeu)

        if gagnant == 2:
            SCORE += 1

    game.joueur1, game.joueur2 = game.joueur2, game.joueur1
    return SCORE


start = time.time()

NB_GEN = 2
THRESHOLD_FITNESS = 0.8 * 2 * NB_PARTIES // 1
print(f"NB_PARTIES = {2 * NB_PARTIES}")
print(f"THRESHOLD_FITNESS = {THRESHOLD_FITNESS}")

for i in range(NB_GEN):
    ranked_solutions = []
    for s in tqdm(solutions):
        game.joueur1.WEIGHTS = s
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
    for rs in best_solutions:
        genes1.append(rs[1][0])
        genes2.append(rs[1][1])
        genes3.append(rs[1][2])
        genes4.append(rs[1][3])

    new_generation = []
    mutation_rate = random.uniform(0.99, 1.01)
    for _ in range(NB_SOLUTIONS//2):
        g1 = random.choice(genes1) * mutation_rate
        g2 = random.choice(genes2) * mutation_rate
        g3 = random.choice(genes3) * mutation_rate
        g4 = random.choice(genes4) * mutation_rate
        new_generation.append([g1, g2, g3, g4])

    solutions = new_generation

end = time.time()
print(f"\nTemps: {(end-start)/60} minutes")


