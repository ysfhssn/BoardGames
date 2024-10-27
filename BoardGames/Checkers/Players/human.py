#!/usr/bin/env python
# -*- coding: utf-8 -*-
import game
if game.GUI:
    from Checkers.checkers import WIN, SIZE, draw_board, draw_piece, get_valid_moves_of_piece
    import pygame

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer (int, int, int, int)
    """
    i = None
    j = None
    di = None
    dj = None

    valid_moves = [(move[0][0], move[0][1], move[-1][-2], move[-1][-1]) for move in game.get_valid_moves(game_info)] if isinstance(game.get_valid_moves(game_info)[0], list) else game.get_valid_moves(game_info)

    print(valid_moves)

    if not game.GUI:
        print("Valid moves: ", valid_moves)
        i = int(input("Row: "))
        j = int(input("Col: "))
        di = int(input("Offset row: "))
        dj = int(input("Offset col: "))
        while (i, j, di, dj) not in valid_moves:
            print("Invalid move !")
            i = int(input("Row: "))
            j = int(input("Col: "))
            di = int(input("Offset row: "))
            dj = int(input("Offset col: "))
        if (i, j, di, dj) in valid_moves:
            if isinstance(game.get_valid_moves(game_info)[0], list):
                for mv in game.get_valid_moves(game_info):
                    if (i, j, di, dj) == (mv[0][0], mv[0][1], mv[-1][-2], mv[-1][-1]):
                        return mv
            return (i, j, di, dj)

    else:
        first_loop = False
        second_loop = False

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] or first_loop:
                    draw_board(game_info)
                    first_loop = False
                    second_loop = True
                    i, j = y//SIZE, x//SIZE
                    if i < 0 or i >= len(game_info[0]): continue
                    if j < 0 or j >= len(game_info[0][0]): continue

                    piece = game_info[0][i][j]
                    if piece == " ": continue
                    pygame.draw.rect(WIN, (129,150,105), (j*SIZE,i*SIZE,SIZE,SIZE))
                    center_coords = (j*SIZE+SIZE//2, i*SIZE+SIZE//2)
                    draw_piece(piece, center_coords)

                    for moves in get_valid_moves_of_piece(game_info, i, j):
                        if isinstance(moves, tuple): moves = [moves]
                        for idx, move in enumerate(moves):
                            _, _, dii, djj = move
                            if (moves[0][0], moves[0][1], moves[-1][-2], moves[-1][-1]) in valid_moves and idx == len(moves)-1 and ((game_info[1] == 1 and piece in ["w","W"]) or (game_info[1] == 2 and piece in ["b","B"])):
                                color = (129,150,105)
                            else:
                                color = (196,180,162)
                            pygame.draw.circle(WIN, color, (djj*SIZE+SIZE//2, dii*SIZE+SIZE//2), SIZE//7)

                    while second_loop:
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: return None
                            x, y = pygame.mouse.get_pos()
                            if pygame.mouse.get_pressed()[0]:
                                first_loop = True
                                second_loop = False
                                di, dj = y//SIZE, x//SIZE
                                if (i, j, di, dj) in valid_moves:
                                    if isinstance(game.get_valid_moves(game_info)[0], list):
                                        for mv in game.get_valid_moves(game_info):
                                            if (i, j, di, dj) == (mv[0][0], mv[0][1], mv[-1][-2], mv[-1][-1]):
                                                return mv
                                    return (i, j, di, dj)
                                else:
                                    i, j = di, dj
