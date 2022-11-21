#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
dirname = os.path.dirname(__file__)
from stockfish import Stockfish # pip install stockfish

UCI_DICT = {
    "8":0, "7":1, "6":2, "5":3, "4":4, "3":5, "2":6, "1":7,
    "a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7
}

MOVE_DICT = {
    "row": { 0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3", 6:"2", 7:"1" },
    "col": { 0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h" }
}

stockfish = Stockfish(os.path.join(dirname, "stockfish_20011801_x64.exe"))

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    ucis = get_ucis(game_info)
    stockfish.set_position(ucis)
    print(stockfish.get_board_visual())
    print(stockfish.get_best_move())
    ucis.append(stockfish.get_best_move())
    stockfish.set_position(ucis)
    return uci_to_move(ucis[-1])

def get_ucis(game_info):
    return [move_to_uci(move) + ("q" if i in game_info[6] else "") for i, move in enumerate(game_info[3])]

def move_to_uci(move):
    """ (int, int, int, int) -> str """
    i, j, di, dj = move
    return MOVE_DICT["col"][j] + MOVE_DICT["row"][i] + MOVE_DICT["col"][dj] + MOVE_DICT["row"][di]

def uci_to_move(uci):
    """ str -> (int, int, int, int) """
    return (UCI_DICT[uci[1]], UCI_DICT[uci[0]], UCI_DICT[uci[3]], UCI_DICT[uci[2]])

if __name__ == '__main__':
    stockfish = Stockfish("./stockfish_20011801_x64.exe")
    ucis = []
    while True:
        print("WHITE")
        ucis.append(stockfish.get_best_move())
        stockfish.set_position(ucis)
        print(stockfish.get_board_visual())
        print("BLACK")
        ucis.append(stockfish.get_best_move())
        stockfish.set_position(ucis)
        print(stockfish.get_board_visual())
        print(ucis)
