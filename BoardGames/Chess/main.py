#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
sys.path.append(os.path.join(dirname, 'Joueurs'))
import game
if game.GUI: import pygame
import chess
import joueur_humain, joueur_minimax_ab, joueur_minimax_ab_opti, joueur_stockfish
import time
JOUEURS_TREE = [joueur_minimax_ab, joueur_minimax_ab_opti]


game.game = chess
game.joueur1 = joueur_humain
game.joueur2 = joueur_stockfish


START = None
def main():
    global START
    NB_PARTIES = N = 1 #int(input("Nombre de parties: "))
    START = time.time()
    NB_PARTIES_GAGNES_J1 = 0
    NB_PARTIES_GAGNES_J2 = 0
    NB_PARTIES_EGALITES = 0

    i = 0
    while i < NB_PARTIES:
        print(f"\n\n########## DEBUT PARTIE {i+1} ##########")
        jeu = game.initialiseJeu()
        #jeu = game.initialiseInteressant("EN PASSANT")
        #game.affiche(jeu)
        if game.GUI: game.game.draw_board(jeu)

        start = time.time()
        while not game.finJeu(jeu):
            if game.GUI:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)
            start_coup = time.time()
            coup = game.saisieCoup(jeu)
            end_coup = time.time()
            temps_coup = end_coup - start_coup

            if jeu[1] == 1:
                ai_name = game.joueur1.__name__.upper().split('_')[-1]
                print(f"TEMPS COUP {ai_name}: {temps_coup:.5f} seconds")
                if game.joueur1 in JOUEURS_TREE:
                    print(f"\tNB_NOEUDS: {game.joueur1.NB_NOEUDS}")
                    if ai_name == "OPTI": print(f"\tNB_CACHE: {game.joueur1.NB_CACHE}")
            if jeu[1] == 2:
                ai_name = game.joueur2.__name__.upper().split('_')[-1]
                print(f"TEMPS COUP {ai_name}: {temps_coup:.5f} seconds")
                if game.joueur2 in JOUEURS_TREE:
                    print(f"\tNB_NOEUDS: {game.joueur2.NB_NOEUDS}")
                    if ai_name == "OPTI": print(f"\tNB_CACHE: {game.joueur2.NB_CACHE}")

            game.joueCoup(jeu, coup)
            if game.GUI: game.game.draw_board(jeu)
            #game.affiche(jeu)
            #game.changeJoueur(jeu) deja effectue dans joueCoup
        end = time.time()
        temps = end - start

        gagnant = game.getGagnant(jeu)

        print(f"TEMPS PARTIE {i+1}: {temps:.5f} seconds")
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

        i += 1

        if game.GUI and i == NB_PARTIES:
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
                        NB_PARTIES += N
                        time.sleep(0.1)
                        break


    print("\n\n###########################################")
    print(f"{game.joueur1.__name__.upper()} VS {game.joueur2.__name__.upper()}")
    print("\nNB_PARTIES:          ", NB_PARTIES)
    print("NB_PARTIES_GAGNES_J1:", NB_PARTIES_GAGNES_J1)
    print("NB_PARTIES_GAGNES_J2:", NB_PARTIES_GAGNES_J2)
    print("NB_PARTIES_EGALITES: ", NB_PARTIES_EGALITES)
    print("###########################################")




if __name__ == "__main__":
    main()
    END = time.time()
    temps = END - START
    print(f"\n\nTemps total: {temps:.5f} seconds")
