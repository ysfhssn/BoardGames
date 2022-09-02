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
from Awele.Players import random, master, minimax_ab_order
import time


game.game = awele
game.player1 = minimax_ab_order
game.player2 = master


# test depth 2
game.player1.PLIES = 2
game.player2.PLIES = 2

# Il y aura au minimum 2*NUM_ROUNDS*len(j1.weights) parties
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

eps = 0.1
n = len(game.player1.WEIGHTS)
THRESHOLD_score_max = 0.8 * 2 * NUM_ROUNDS // 1

"""# si player1 et player2 ont les memes poids
game.player1.WEIGHTS = master.WEIGHTS"""
print(f"Au debut: {game.player1.WEIGHTS}")
print(f"THRESHOLD_score_max = {THRESHOLD_score_max}\n")

score_max = fitness()
print(f"*** DEB *** score_max = {score_max}")

if score_max < THRESHOLD_score_max:
    for i in range(n):
        # determiner le sens de l'amelioration
        sens = None
        game.player1.WEIGHTS[i] += eps
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
            game.player1.WEIGHTS[i] -= 2 * eps
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
            game.player1.WEIGHTS[i] += eps
            print(f"Index {i}: Aucune modification")
            continue

        # tant qu'il y a amelioration a faire
        game.player1.WEIGHTS[i] += eps * sens
        score = fitness()
        if score >= THRESHOLD_score_max:
            score_max = score
            print(f"score_max = {score_max}")
            print("Limite score_max atteint")
            break

        while score > score_max:
            score_max = score
            print(f"\tAmelioration: score_max = {score_max}")
            game.player1.WEIGHTS[i] += eps * sens
            score = fitness()

        game.player1.WEIGHTS[i] -= eps * sens
        print(f"Index {i}: {game.player1.WEIGHTS[i]}")


print(f"\n*** FIN *** {game.player1.WEIGHTS}")
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
