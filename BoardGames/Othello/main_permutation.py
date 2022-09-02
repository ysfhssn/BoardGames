#!/usr/bin/env python
# -*- coding: utf-8 -*-
import main
import time

def main_permutation():
    main.game.player1, main.game.player2 = main.game.player2, main.game.player1
    main.main()
    END = time.time()
    round_time = END - main.START
    print(f"\n\nTotal time: {round_time:.5f} seconds")
    main.game.player1, main.game.player2 = main.game.player2, main.game.player1

if __name__ == "__main__":
    main_permutation()