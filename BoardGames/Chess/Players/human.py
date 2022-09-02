#!/usr/bin/env python
# -*- coding: utf-8 -*-
import game
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
        print("Coups valides: ", game.get_valid_moves(game_info))
        i = int(input("Votre row: "))
        j = int(input("Votre col: "))
        di = int(input("Votre row de deplacement: "))
        dj = int(input("Votre col de deplacement: "))
        while (i, j, di, dj) not in game.get_valid_moves(game_info):
            print("Coup invalide !")
            i = int(input("Votre row: "))
            j = int(input("Votre col: "))
            di = int(input("Votre row de deplacement: "))
            dj = int(input("Votre col de deplacement: "))
        return (i, j, di, dj)

    else:
        WIN = game.game.WIN
        SIZE = game.game.SIZE
        IMAGES = game.game.IMAGES
        draw_board = game.game.draw_board
        get_valid_moves_of_piece = game.game.get_valid_moves_of_piece

        snd_loop = False
        while not game.game.is_game_over(game_info):
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
                        key = "b" + piece[1]
                        WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))
                    else:
                        key = "w" + piece[1]
                        WIN.blit(IMAGES[key], (j*SIZE,i*SIZE))

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
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: return None
                            x, y = pygame.mouse.get_pos()
                            if pygame.mouse.get_pressed()[0]:
                                di, dj = y//SIZE, x//SIZE
                                if (i, j, di, dj) in game.get_valid_moves(game_info):
                                    return (i, j, di, dj)
                                else:
                                    snd_loop = False
