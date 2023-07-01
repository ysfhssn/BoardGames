#!/usr/bin/env python
# -*- coding: utf-8 -*-
import game
from Chess.chess import WIN, SIZE, IMAGES, get_valid_moves_of_piece, draw_board, draw_timers
if game.GUI: import pygame

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer (int, int, int, int)
    """
    i = None
    j = None
    di = None
    dj = None

    if not game.GUI:
        print("Valid moves: ", game.get_valid_moves(game_info))
        i = int(input("Row: "))
        j = int(input("Col: "))
        di = int(input("Offset row: "))
        dj = int(input("Offset col: "))
        while (i, j, di, dj) not in game.get_valid_moves(game_info):
            print("Invalid move !")
            i = int(input("Row: "))
            j = int(input("Col: "))
            di = int(input("Offset row: "))
            dj = int(input("Offset col: "))
        return (i, j, di, dj)

    else:
        snd_loop = False
        while True:
            draw_board(game_info)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    snd_loop = True
                    i, j = y//SIZE, x//SIZE
                    if i < 0 or i >= len(game_info[0]): continue
                    if j < 0 or j >= len(game_info[0][0]): continue

                    piece = game_info[0][i][j]
                    if piece[0] == " ": continue
                    pygame.draw.rect(WIN, (129,150,105), (j*SIZE,i*SIZE,SIZE,SIZE))
                    if piece[0] == "b":
                        WIN.blit(IMAGES[piece], (j*SIZE,i*SIZE))
                    else:
                        WIN.blit(IMAGES[piece], (j*SIZE,i*SIZE))

                    for ii, jj, dii, djj in get_valid_moves_of_piece(game_info, game_info[0][i][j], i, j):
                        #print(game_info[0][i][j], get_valid_moves_of_piece(game_info, game_info[0][i][j], i, j))
                        if ((game_info[1] == 1 and game_info[0][i][j][0] == "w") or (game_info[1] == 2 and game_info[0][i][j][0] == "b")):
                            color = (129,150,105)
                        else:
                            color = (196,180,162)
                            pygame.draw.circle(WIN, color, (djj*SIZE+SIZE//2, dii*SIZE+SIZE//2), SIZE//7)
                            pygame.display.update()
                        if (ii, jj, dii, djj) in game.get_valid_moves(game_info):
                            pygame.draw.circle(WIN, color, (djj*SIZE+SIZE//2, dii*SIZE+SIZE//2), SIZE//7)
                            pygame.display.update()

                    while snd_loop:
                        draw_timers(game_info)
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: return None
                            x, y = pygame.mouse.get_pos()
                            if pygame.mouse.get_pressed()[0]:
                                di, dj = y//SIZE, x//SIZE
                                if (i, j, di, dj) in game.get_valid_moves(game_info):
                                    return (i, j, di, dj)
                                else:
                                    snd_loop = False
