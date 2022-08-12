#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
game.GUI = True
import othello
if game.GUI: import pygame
from Othello.Joueurs import joueur_minimax_ab, joueur_negamax_ab, joueur_random
import time
import random
from tqdm import tqdm


game.game = othello
game.joueur1 = joueur_minimax_ab
game.joueur2 = joueur_negamax_ab
# game.GUI = False


# generate solutions
NB_SOLUTIONS = 4
solutions = []
for _ in range(NB_SOLUTIONS):
    solutions.append([random.uniform(0,1),
                      random.uniform(0,1),
                      random.uniform(0,1)])


NB_PARTIES = 2
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
            if len(game.getCoupsJoues(jeu)) <= 4:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)
            if game.GUI: game.game.draw_board(jeu)

        gagnant = game.getGagnant(jeu)

        if gagnant == 1:
            SCORE += 1


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

            if len(game.getCoupsJoues(jeu)) <= 4:
                coup = joueur_random.saisieCoup(jeu)
            else:
                coup = game.saisieCoup(jeu)
            game.joueCoup(jeu, coup)
            if game.GUI: game.game.draw_board(jeu)

        gagnant = game.getGagnant(jeu)

        if gagnant == 2:
            SCORE += 1

    game.joueur1, game.joueur2 = game.joueur2, game.joueur1
    return SCORE


start = time.time()

NB_GEN = 2
THRESHOLD_FITNESS = 0.75 * 2 * NB_PARTIES // 1
print(f"NB_PARTIES = {2 * NB_PARTIES}")
print(f"THRESHOLD_FITNESS = {THRESHOLD_FITNESS}")

for i in range(NB_GEN):
    ranked_solutions = []
    for s in tqdm(solutions):
        game.joueur1.WEIGHTS = s
        fitn = fitness()
        ranked_solutions.append( (fitn, s) )

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
    for rs in best_solutions:
        genes1.append(rs[1][0])
        genes2.append(rs[1][1])
        genes3.append(rs[1][2])

    new_generation = []
    mutation_rate = random.uniform(0.99, 1.01)
    for _ in range(NB_SOLUTIONS):
        g1 = random.choice(genes1) * mutation_rate
        g2 = random.choice(genes2) * mutation_rate
        g3 = random.choice(genes3) * mutation_rate
        new_generation.append([g1, g2, g3])

    solutions = new_generation

end = time.time()
print(f"\nTemps: {(end-start)/60} minutes")

if game.GUI: pygame.quit()


