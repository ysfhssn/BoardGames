#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
from Awele.Joueurs import MASTER, MCTS, Ayo_ab, Ayo, joueur_random, joueur_horizon, joueur_minimax, joueur_negamax, joueur_minimax_ab, joueur_negamax_ab, joueur_minimax_ab_order
import time
JOUEURS_TREE = [Ayo, Ayo_ab, joueur_horizon, joueur_minimax, joueur_negamax, joueur_minimax_ab, joueur_negamax_ab, joueur_minimax_ab_order, MASTER]


START = None
def main():
    from Awele import awele
    game.game = awele
    global START
    NB_PARTIES = 1 #int(input("Nombre de parties: "))
    START = time.time()
    NB_PARTIES_GAGNES_J1 = 0
    NB_PARTIES_GAGNES_J2 = 0
    NB_PARTIES_EGALITES = 0

    for i in range(NB_PARTIES):
        print(f"\n\n########## DEBUT PARTIE {i+1} ##########")
        jeu = game.initialiseJeu()
        #game.affiche(jeu)

        start = time.time()
        while not game.finJeu(jeu):
            start_coup = time.time()
            if len(game.getCoupsJoues(jeu)) < 0: coup = joueur_random.saisieCoup(jeu)
            else: coup = game.saisieCoup(jeu)
            end_coup = time.time()
            temps_coup = end_coup - start_coup
            if coup is None: return # human quit

            print_stats_coup(jeu, temps_coup)

            game.joueCoup(jeu, coup)
            #game.affiche(jeu)
            #game.changeJoueur(jeu) deja effectue dans joueCoup
        end = time.time()
        temps = end - start

        gagnant = game.getGagnant(jeu)

        print(f"TEMPS PARTIE {i+1}: {temps:.5f} seconds")
        if game.joueur1 in JOUEURS_TREE:
            print(f"NB_NOEUDS_J1 PARTIE {i+1}: {game.joueur1.NB_NOEUDS}")
            game.joueur1.NB_NOEUDS = 0
        if game.joueur2 in JOUEURS_TREE:
            print(f"NB_NOEUDS_J2 PARTIE {i+1}: {game.joueur2.NB_NOEUDS}")
            game.joueur2.NB_NOEUDS = 0
        print(f"NB COUPS: {len(game.getCoupsJoues(jeu))}")
        print(f"SCORE FINAL: {game.getScores(jeu)}")

        if gagnant == 1:
            print(f"GAGNANT PARTIE {i+1}: Joueur {gagnant}")
            NB_PARTIES_GAGNES_J1 += 1
        elif gagnant == 2:
            print(f"GAGNANT PARTIE {i+1}: Joueur {gagnant}")
            NB_PARTIES_GAGNES_J2 += 1
        else:
            print(f"GAGNANT PARTIE {i+1}: Egalite")
            NB_PARTIES_EGALITES += 1


    print("\n\n###########################################")
    print(f"{game.joueur1.__name__.upper().split('.')[-1].split('_')[-1]} VS {game.joueur2.__name__.upper().split('.')[-1].split('_')[-1]}")
    print("\nNB_PARTIES:          ", NB_PARTIES)
    print("NB_PARTIES_GAGNES_J1:", NB_PARTIES_GAGNES_J1)
    print("NB_PARTIES_GAGNES_J2:", NB_PARTIES_GAGNES_J2)
    print("NB_PARTIES_EGALITES: ", NB_PARTIES_EGALITES)
    print("###########################################")

def print_stats_coup(jeu, temps_coup):
    if jeu[1] == 1:
        joueur = game.joueur1.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]
        print(f"TEMPS COUP {joueur}: {temps_coup:.5f} seconds")
        if game.joueur1 in JOUEURS_TREE:
            print(f"\tNB_NOEUDS: {game.joueur1.NB_NOEUDS}")
            if joueur == "OPTI": print(f"\tNB_CACHE: {game.joueur1.NB_CACHE}")
    if jeu[1] == 2:
        joueur = game.joueur2.__name__.upper().split('.')[-1].split('_')[-1].split('.')[-1].split('_')[-1]
        print(f"TEMPS COUP {joueur}: {temps_coup:.5f} seconds")
        if game.joueur2 in JOUEURS_TREE:
            print(f"\tNB_NOEUDS: {game.joueur2.NB_NOEUDS}")
            if joueur == "OPTI": print(f"\tNB_CACHE: {game.joueur2.NB_CACHE}")

if __name__ == "__main__":
    #######################
    game.joueur1 = MASTER
    game.joueur2 =  MCTS
    #######################
    main()
    END = time.time()
    temps = END - START
    print(f"\n\nTemps total: {temps:.5f} seconds")
