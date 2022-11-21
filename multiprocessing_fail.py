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
import human, random, first_move
import horizon, minimax, negamax
import minimax_ab, negamax_ab, minimax_ab_order
import ayo, ayo_ab
import multiprocessing as mp
import time
JOUEURS_TREE = [ayo, ayo_ab, horizon, minimax, negamax, minimax_ab, negamax_ab, minimax_ab_order]


game.game = awele
game.player1 = minimax_ab_order
game.player2 = minimax_ab_order


NUM_ROUNDS_WON_P1 = mp.Value("i", 0)
NUM_ROUNDS_WON_P2 = mp.Value("i", 0)
NUM_ROUNDS_DRAWS = mp.Value("i", 0)
def main_loop():
    global NUM_ROUNDS_WON_P1, NUM_ROUNDS_WON_P2, NUM_ROUNDS_DRAWS
    game_info = game.init()
    #game.print_game(game_info)

    while not game.is_game_over(game_info):
        if len(game.get_played_moves(game_info)) <= 4:
            move = random.get_move(game_info)
        else:
            move = game.get_move(game_info)
        game.play_move(game_info, move)
        #game.print_game(game_info)
        #game.change_player(game_info) deja effectue dans play_move

    winner = game.get_winner(game_info)

    print("\n-------------------------------------------------")
    if game.player1 in JOUEURS_TREE:
        print(f"NUM_NODES_P1 ROUND : {game.player1.NUM_NODES}")
        game.player1.NUM_NODES = 0
    if game.player2 in JOUEURS_TREE:
        print(f"NUM_NODES_P2 ROUND : {game.player2.NUM_NODES}")
        game.player2.NUM_NODES = 0
    print(f"NUM_MOVES: {len(game.get_played_moves(game_info))}")
    print(f"FINAL SCORE: {game.get_score(game_info)}")

    if winner == 1:
        print(f"Winner: Player {winner}")
        NUM_ROUNDS_WON_P1.value += 1
    elif winner == 2:
        print(f"Winner: Player {winner}")
        NUM_ROUNDS_WON_P2.value += 1
    else:
        print("Winner: Egalite")
        NUM_ROUNDS_DRAWS.value += 1

def main():
    NUM_ROUNDS = int(input("NUM_ROUNDS: "))
    processes = []
    start = time.time()
    for _ in range(NUM_ROUNDS):
        p = mp.Process(target=main_loop)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    end = time.time()
    game_time = end - start
    print(f"\nTotal time : {game_time:.5f} seconds")

    print("\n\n###########################################")
    print(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1]}")
    print("\nNUM_ROUNDS:       ", NUM_ROUNDS)
    print("NUM_ROUNDS_WON_P1:", NUM_ROUNDS_WON_P1.value)
    print("NUM_ROUNDS_WON_P2:", NUM_ROUNDS_WON_P2.value)
    print("NUM_ROUNDS_DRAWS: ", NUM_ROUNDS_DRAWS.value)
    print("###########################################")



if __name__ == "__main__":
    main()
