#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
from Squadro.Joueurs import joueur_minimax_ab, MASTER, joueur_random
import game
game.GUI = True
import squadro
if game.GUI: import pygame
import time
import random
import math
from tqdm import tqdm


game.game = squadro
game.joueur1 = joueur_minimax_ab
game.joueur2 = MASTER


# generate solutions
NB_SOLUTIONS = 20
solutions = []
for _ in range(NB_SOLUTIONS):
    solutions.append([random.uniform(0,1),
                      random.uniform(0,1),
                      random.uniform(0,1),
                      random.uniform(0,1)])


# Il y aura 2*NB_PARTIES*NB_SOLUTIONS parties par generation
NB_PARTIES = 1
def fitness():
    SCORE = 0

    for i in range(NB_PARTIES):
        jeu = game.initialiseJeu()
        if game.GUI: game.game.draw_board(jeu)

        while not game.finJeu(jeu):
            if game.GUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

            if len(game.getCoupsJoues(jeu)) < 0:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)
            if game.GUI: game.game.draw_board(jeu)

        gagnant = game.getGagnant(jeu)

        if gagnant == 1:
            SCORE += 1000
        else:
            SCORE += jeu[4][0]


    game.joueur1, game.joueur2 = game.joueur2, game.joueur1
    for i in range(NB_PARTIES):
        jeu = game.initialiseJeu()
        if game.GUI: game.game.draw_board(jeu)

        while not game.finJeu(jeu):
            if game.GUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

            if len(game.getCoupsJoues(jeu)) < 0:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)
            if game.GUI: game.game.draw_board(jeu)

        gagnant = game.getGagnant(jeu)

        if gagnant == 2:
            SCORE += 1000
        else:
            SCORE += jeu[4][1]

    game.joueur1, game.joueur2 = game.joueur2, game.joueur1
    return SCORE


start = time.time()

NB_GEN = 2
THRESHOLD_FITNESS = math.ceil(0.8 * 2 * NB_PARTIES) * 1000
print(f"NB_PARTIES = {2 * NB_PARTIES}")
print(f"THRESHOLD_FITNESS = {THRESHOLD_FITNESS}")

for i in range(NB_GEN):
    ranked_solutions = []
    for s in tqdm(solutions):
        game.joueur1.WEIGHTS = s
        fitn = fitness()
        ranked_solutions.append((fitn, s))
        if fitn >= THRESHOLD_FITNESS: break

    ranked_solutions.sort(reverse=True)
    print(f"=== GEN {i+1} === 3 best solutions ===")
    if len(ranked_solutions) >= 3:
        for rs in ranked_solutions[:3]:
            print(rs)
    else:
        for rs in ranked_solutions:
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
    NB_SOLUTIONS //= 2
    for _ in range(NB_SOLUTIONS):
        g1 = random.choice(genes1) * random.uniform(0.99, 1.01)
        g2 = random.choice(genes2) * random.uniform(0.99, 1.01)
        g3 = random.choice(genes3) * random.uniform(0.99, 1.01)
        g4 = random.choice(genes4) * random.uniform(0.99, 1.01)
        new_generation.append([g1, g2, g3, g4])

    solutions = new_generation

end = time.time()
print(f"\nTemps: {(end-start)/60} minutes")
