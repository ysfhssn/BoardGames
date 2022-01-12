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
import joueur_premier_coup

game.game = awele
game.joueur1 = joueur_premier_coup
game.joueur2 = joueur_premier_coup


jeu = game.initialiseInteressant()
assert(game.getCaseVal(jeu, 0, 1) == 1)
assert(game.getCoupsValides(jeu) == [])
assert(game.finJeu(jeu) == True)
assert(game.getGagnant(jeu) == 1)
assert(game.getScores(jeu) == [1, 0])

jeu = game.initialiseInteressant(1)
assert(len(game.getCoupsValides(jeu)) == 1)
coup = game.saisieCoup(jeu)
game.joueCoup(jeu, coup)
assert(game.game.adversaireAffame(jeu) == True)
assert(game.finJeu(jeu) == True)
assert(game.getGagnant(jeu) == game.getJoueur(jeu))
assert(game.getScore(jeu, 2) == 2)

jeu = game.initialiseInteressant(2)
coup = game.saisieCoup(jeu)
game.joueCoup(jeu, coup)
assert(game.getScores(jeu) == [9, 0])
assert(game.finJeu(jeu) == True)
assert(game.getScores(jeu) == [9, 4])