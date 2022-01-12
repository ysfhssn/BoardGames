#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Joueurs'))
import game
import othello
import joueur_random
import joueur_minimax_ab, joueur_negamax_ab
import time


game.game = othello
game.joueur1 = joueur_minimax_ab
game.joueur2 = joueur_negamax_ab


# test horizon 1
game.joueur1.PLIES = 1
game.joueur2.PLIES = 1

# Il y aura 2*NB_PARTIES*len(j1.weights) parties
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
THRESHOLD_score_max = 0.7 * 2 * NB_PARTIES // 1

game.joueur1.WEIGHTS = game.joueur1.WEIGHTS
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

