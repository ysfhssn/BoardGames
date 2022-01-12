#!/usr/bin/env python
# -*- coding: utf-8 -*-
import main, time

def main_permutation():
    main.game.joueur1, main.game.joueur2 = main.game.joueur2, main.game.joueur1
    main.main()
    END = time.time()
    temps = END - main.START
    print(f"\n\nTemps total: {temps:.5f} seconds")
    main.game.joueur1, main.game.joueur2 = main.game.joueur2, main.game.joueur1

if __name__ == "__main__":
    main_permutation()