#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
if game.GUI: import pygame
from Chess.Players import minimax_ab, minimax_ab_opti, master, mcts, random_move
import time
JOUEURS_TREE = [minimax_ab, minimax_ab_opti, master, mcts]


START = None
def main():
    from Chess import chess
    game.game = chess
    global START
    NUM_ROUNDS = N = 1 #int(input("Number of rounds: "))
    START = time.time()
    NUM_ROUNDS_WON_P1 = 0
    NUM_ROUNDS_WON_P2 = 0
    NUM_ROUNDS_DRAWS = 0

    i = 0
    while i < NUM_ROUNDS:
        print(f"\n\n########## DEBUT PARTIE {i+1} ##########")
        game_info = game.init()
        #game_info = game.init_test("EN PASSANT")
        #game.print_game(game_info)
        if game.GUI:
            pygame.display.set_mode((chess.WIDTH, chess.HEIGHT))
            chess.draw_board(game_info)

        start = time.time()
        while not game.is_game_over(game_info):
            if game.GUI:
                pygame.display.set_mode((chess.WIDTH, chess.HEIGHT))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

            move_start = time.time()
            if len(game.get_played_moves(game_info)) < 0: move = random_move.get_move(game_info)
            else: move = game.get_move(game_info)
            move_end = time.time()
            move_time = move_end - move_start
            if move is None: return # human quit

            print_stats_coup(game_info, move_time)

            game.play_move(game_info, move)
            if game.GUI: chess.draw_board(game_info)
            #game.print_game(game_info)
            #game.change_player(game_info) deja effectue dans play_move
        end = time.time()
        round_time = end - start

        winner = game.get_winner(game_info)

        print(f"ROUND TIME {i+1}: {round_time:.5f} seconds")
        print(f"NUM_MOVES: {len(game.get_played_moves(game_info))}")
        print(f"FINAL SCORE: {game.get_scores(game_info)}")

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
            pa_rect.topleft = (0, chess.HEIGHT+5)
            chess.WIN.blit(pa, pa_rect)
            pygame.display.update()
            while True:
                close = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: close = True
                if close: break

                x, y = pygame.mouse.get_pos()
                if pa_rect.collidepoint((x,y)):
                    if pygame.mouse.get_pressed()[0]:
                        NUM_ROUNDS += N
                        time.sleep(0.1)
                        break


    print("\n\n###########################################")
    print(f"{game.player1.__name__.upper().split('.')[-1].split('_')[-1]} VS {game.player2.__name__.upper().split('.')[-1].split('_')[-1]}")
    print("\nNUM_ROUNDS:          ", NUM_ROUNDS)
    print("NUM_ROUNDS_WON_P1:", NUM_ROUNDS_WON_P1)
    print("NUM_ROUNDS_WON_P2:", NUM_ROUNDS_WON_P2)
    print("NUM_ROUNDS_DRAWS: ", NUM_ROUNDS_DRAWS)
    print("###########################################")


def print_stats_coup(game_info, move_time):
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
    game.player2 =  mcts
    #######################
    main()
    END = time.time()
    round_time = END - START
    print(f"\n\nTotal time: {round_time:.5f} seconds")
