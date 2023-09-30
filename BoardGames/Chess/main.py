#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
if game.GUI: import pygame
from Chess.Players import minimax_ab, minimax_ab_opti, master, sfish, random_move, human, mcts
import time
JOUEURS_TREE = [minimax_ab, minimax_ab_opti, master]


def main():
    from Chess import chess
    game.game = chess
    NUM_ROUNDS = N = 1 #int(input("Number of rounds: "))
    NUM_ROUNDS_WON_P1 = 0
    NUM_ROUNDS_WON_P2 = 0
    NUM_ROUNDS_DRAWS = 0
    NUM_FIRST_RANDOM_MOVES = 0

    game_start = time.time()
    i = 0
    while i < NUM_ROUNDS:
        print(f"\n\n########## DEBUT PARTIE {i+1} ##########")
        game_info = game.init()
        #game_info = game.init_test("PROMOTION")
        #game.print_game(game_info)
        if game.GUI:
            pygame.display.set_mode((chess.WIDTH, chess.HEIGHT))
            chess.draw_board(game_info)

        round_start = time.time()
        while not game.is_game_over(game_info):
            if game.GUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        chess.stop_event.set()
                        return

            move_start = time.time()
            if len(game.get_played_moves(game_info)) < NUM_FIRST_RANDOM_MOVES: move = random_move.get_move(game_info)
            else: move = game.get_move(game_info)
            move_end = time.time()
            move_time = move_end - move_start
            if move is None:
                chess.stop_event.set()
                return # human quit

            print_move_stats(game_info, move_time)

            if game.play_move(game_info, move) == 'quit':
                chess.stop_event.set()
                return # human quit

            if game.GUI: chess.draw_board(game_info)
            #game.print_game(game_info)
            #game.change_player(game_info) deja effectue dans play_move
        round_end = time.time()
        round_time = round_end - round_start

        winner = game.get_winner(game_info)

        print(f"ROUND TIME {i+1}: {round_time:.5f} seconds")
        print(f"NUM_MOVES: {len(game.get_played_moves(game_info))}")
        print(f"FINAL SCORE: {game.get_score(game_info)}")

        if winner == 1:
            print(f"WINNER ROUND {i+1}: Player {winner}")
            NUM_ROUNDS_WON_P1 += 1
        elif winner == 2:
            print(f"WINNER ROUND {i+1}: Player {winner}")
            NUM_ROUNDS_WON_P2 += 1
        else:
            print(f"WINNER ROUND {i+1}: Draw")
            NUM_ROUNDS_DRAWS += 1

        i += 1

        if game.GUI and i == NUM_ROUNDS:
            pa = pygame.transform.scale(pygame.image.load(os.path.join(dirname, "./Images/playagain.jpg")).convert_alpha(), (200,90))
            pa_rect = pa.get_rect()
            pa_rect.topleft = (0, chess.HEIGHT-chess.OFFSET+5)
            chess.WIN.blit(pa, pa_rect)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        chess.stop_event.set()
                        return

                x, y = pygame.mouse.get_pos()
                if pa_rect.collidepoint((x, y)):
                    clicked = False
                    if pygame.mouse.get_pressed()[0]:
                        clicked = True
                    if clicked:
                        clicked = False
                        NUM_ROUNDS += N
                        break
    game_end = time.time()
    game_time = game_end - game_start

    print("\n\n###########################################")
    print(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1]}")
    print("\nNUM_ROUNDS:       ", NUM_ROUNDS)
    print("NUM_ROUNDS_WON_P1:", NUM_ROUNDS_WON_P1)
    print("NUM_ROUNDS_WON_P2:", NUM_ROUNDS_WON_P2)
    print("NUM_ROUNDS_DRAWS: ", NUM_ROUNDS_DRAWS)
    print("###########################################")

    print(f"\n\nTotal time: {game_time:.5f} seconds")

def print_move_stats(game_info, move_time):
    if game_info[1] == 1:
        player = game.player1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]
        print(f"MOVE TIME {player}: {move_time:.5f} seconds")
        if game.player1 in JOUEURS_TREE:
            print(f"\tNUM_NODES: {game.player1.NUM_NODES}")
            if player == "OPTI": print(f"\tNUM_NODES_CACHE: {game.player1.NUM_NODES_CACHE}")
    if game_info[1] == 2:
        player = game.player2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]
        print(f"MOVE TIME {player}: {move_time:.5f} seconds")
        if game.player2 in JOUEURS_TREE:
            print(f"\tNUM_NODES: {game.player2.NUM_NODES}")
            if player == "OPTI": print(f"\tNUM_NODES_CACHE: {game.player2.NUM_NODES_CACHE}")

if __name__ == "__main__":
    #######################
    game.player1 = master
    game.player2 = mcts
    #######################
    main()
