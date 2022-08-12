#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Joueurs'))
import game
import awele
import joueur_humain, joueur_random, joueur_premier_coup
import joueur_horizon, joueur_minimax, joueur_negamax
import joueur_minimax_ab, joueur_negamax_ab, joueur_minimax_ab_order
import Ayo, Ayo_ab
import multiprocessing as mp
import time
JOUEURS_TREE = [Ayo, Ayo_ab, joueur_horizon, joueur_minimax, joueur_negamax, joueur_minimax_ab, joueur_negamax_ab, joueur_minimax_ab_order]


game.game = awele
game.joueur1 = joueur_minimax_ab_order
game.joueur2 = joueur_minimax_ab_order


NB_PARTIES_GAGNES_J1 = mp.Value("i", 0)
NB_PARTIES_GAGNES_J2 = mp.Value("i", 0)
NB_PARTIES_EGALITES = mp.Value("i", 0)
def main_loop():
    global NB_PARTIES_GAGNES_J1, NB_PARTIES_GAGNES_J2, NB_PARTIES_EGALITES
    jeu = game.initialiseJeu()
    #game.affiche(jeu)

    while not game.finJeu(jeu):
        if len(game.getCoupsJoues(jeu)) <= 4:
            coup = joueur_random.saisieCoup(jeu)
        else:
            coup = game.saisieCoup(jeu)
        game.joueCoup(jeu, coup)
        #game.affiche(jeu)
        #game.changeJoueur(jeu) deja effectue dans joueCoup

    gagnant = game.getGagnant(jeu)

    print("\n-------------------------------------------------")
    if game.joueur1 in JOUEURS_TREE:
        print(f"NB_NOEUDS_J1 PARTIE : {game.joueur1.NB_NOEUDS}")
        game.joueur1.NB_NOEUDS = 0
    if game.joueur2 in JOUEURS_TREE:
        print(f"NB_NOEUDS_J2 PARTIE : {game.joueur2.NB_NOEUDS}")
        game.joueur2.NB_NOEUDS = 0
    print(f"NB COUPS: {len(game.getCoupsJoues(jeu))}")
    print(f"SCORE FINAL: {game.getScores(jeu)}")

    if gagnant == 1:
        print(f"GAGNANT PARTIE : Joueur {gagnant}")
        NB_PARTIES_GAGNES_J1.value += 1
    elif gagnant == 2:
        print(f"GAGNANT PARTIE : Joueur {gagnant}")
        NB_PARTIES_GAGNES_J2.value += 1
    else:
        print("GAGNANT PARTIE : Egalite")
        NB_PARTIES_EGALITES.value += 1

def main():
    NB_PARTIES = int(input("Nombre de parties: "))
    processes = []
    start = time.time()
    for i in range(NB_PARTIES):
        p = mp.Process(target=main_loop)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    end = time.time()
    temps = end - start
    print(f"\nTemps total : {temps:.5f} seconds")

    print("\n\n###########################################")
    print(f"{game.joueur1.__name__.upper().split('.')[-1].split('_')[-1]} VS {game.joueur2.__name__.upper().split('.')[-1].split('_')[-1]}")
    print("\nNB_PARTIES:          ", NB_PARTIES)
    print("NB_PARTIES_GAGNES_J1:", NB_PARTIES_GAGNES_J1.value)
    print("NB_PARTIES_GAGNES_J2:", NB_PARTIES_GAGNES_J2.value)
    print("NB_PARTIES_EGALITES: ", NB_PARTIES_EGALITES.value)
    print("###########################################")



if __name__ == "__main__":
    main()
