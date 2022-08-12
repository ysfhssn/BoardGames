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
from Awele.Joueurs import joueur_random, MASTER, joueur_minimax_ab_order
import time


game.game = awele
game.joueur1 = joueur_minimax_ab_order
game.joueur2 = MASTER


# test depth 2
game.joueur1.PLIES = 2
game.joueur2.PLIES = 2

# Il y aura au minimum 2*NB_PARTIES*len(j1.weights) parties
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

eps = 0.1
n = len(game.joueur1.WEIGHTS)
THRESHOLD_score_max = 0.8 * 2 * NB_PARTIES // 1

"""# si joueur1 et joueur2 ont les memes poids
game.joueur1.WEIGHTS = MASTER.WEIGHTS"""
print(f"Au debut: {game.joueur1.WEIGHTS}")
print(f"THRESHOLD_score_max = {THRESHOLD_score_max}\n")

score_max = fitness()
print(f"*** DEB *** score_max = {score_max}")

if score_max < THRESHOLD_score_max:
    for i in range(n):
        # determiner le sens de l'amelioration
        sens = None
        game.joueur1.WEIGHTS[i] += eps
        score = fitness()
        if score >= THRESHOLD_score_max:
            score_max = score
            print(f"score_max = {score_max}")
            print("Limite score_max atteint")
            break

        if score > score_max:
            sens = 1
            score_max = score
            print(f"*** Sens + *** score_max = {score_max}")

        if sens is None:
            game.joueur1.WEIGHTS[i] -= 2 * eps
            score = fitness()
            if score >= THRESHOLD_score_max:
                score_max = score
                print(f"score_max = {score_max}")
                print("Limite score_max atteint")
                break

            if score > score_max:
                sens = -1
                score_max = score
                print(f"*** Sens - *** score_max = {score_max}")

        if sens is None:
            game.joueur1.WEIGHTS[i] += eps
            print(f"Index {i}: Aucune modification")
            continue

        # tant qu'il y a amelioration a faire
        game.joueur1.WEIGHTS[i] += eps * sens
        score = fitness()
        if score >= THRESHOLD_score_max:
            score_max = score
            print(f"score_max = {score_max}")
            print("Limite score_max atteint")
            break

        while score > score_max:
            score_max = score
            print(f"\tAmelioration: score_max = {score_max}")
            game.joueur1.WEIGHTS[i] += eps * sens
            score = fitness()

        game.joueur1.WEIGHTS[i] -= eps * sens
        print(f"Index {i}: {game.joueur1.WEIGHTS[i]}")


print(f"\n*** FIN *** {game.joueur1.WEIGHTS}")
print(f"\tscore_max = {score_max}")

end = time.time()
print(f"\nTemps: {(end-start)/60} minutes")

"""
Au debut: [1.0, 0.0, 0.0, 0.0]
THRESHOLD_score_max = 8.0

*** DEB *** score_max = 3
*** Sens + *** score_max = 4
Index 0: 1.1
*** Sens + *** score_max = 6
Index 1: 0.1
Index 2: Aucune modification
Index 3: Aucune modification

*** FIN *** [1.1, 0.1, 0.0, 0.0]
    score_max = 6

Temps: 4.1506758570671085 minutes
"""
