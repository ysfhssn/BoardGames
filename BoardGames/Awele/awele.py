#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game

NB_COUPS_MAX = 100

def initialiseJeu():
    """ void -> jeu
        coup = (int, int)
        Initialise le jeu List[...] :
            0: plateau      	List[List[int]]
            1: joueur       	int (1 ou 2)
            2: coups valides	List[(int, int)]
            3: coups joues  	List[(int, int)]
            4: scores       	List[int, int]
    """
    plateau = [[4,4,4,4,4,4],
               [4,4,4,4,4,4]]
    return [plateau, 1, None, [], [0, 0]]

def initialiseInteressant(key=0):
    d = {
        0: [[0,1,0,0,0,0],
            [0,0,0,0,0,0]],
        1: [[1,0,0,0,0,0],
            [1,0,0,0,0,0]],
        2: [[6,0,0,0,0,0],
            [1,0,0,2,2,2]],
    }

    return [d[key], 1, None, [], [0, 0]]

def adversaireAffame(jeu):
    adversaire = game.getJoueur(jeu)%2 + 1
    return sum(jeu[0][adversaire-1]) == 0

def adversaireNourri(jeu, coup):
    joueur = game.getJoueur(jeu)
    if joueur == 1:
        return game.getCaseVal(jeu, coup[0], coup[1]) - coup[1] > 0
    return game.getCaseVal(jeu, coup[0], coup[1]) + coup[1] > 5

def getCoupsValides(jeu):
    if jeu[2] is None:
        row = game.getJoueur(jeu) - 1
        b = adversaireAffame(jeu)
        jeu[2] = [(row, col) for col in range(6) if game.getCaseVal(jeu, row, col) > 0 and (not b or adversaireNourri(jeu, (row, col)))]
    return jeu[2]

def finJeu(jeu):
    if jeu[4][0] >= 25 or jeu[4][1] >= 25:
        return True
    if not game.getCoupsValides(jeu):
        jeu[4][0] += sum(jeu[0][0])
        jeu[4][1] += sum(jeu[0][1])
        return True
    if len(game.getCoupsJoues(jeu)) >= NB_COUPS_MAX:
        return True

    return False



def nextCase(row, col):
    if row == 0 and col == 0:
        return (1, 0)
    if row == 1 and col == 5:
        return (0, 5)
    if row == 0:
        return (row, col-1)
    else:
        return (row, col+1)

def prevCase(row, col):
    if row == 1 and col == 0:
        return (0, 0)
    if row == 0 and col == 5 :
        return (1, 5)
    if row == 0:
        return (row, col+1)
    else:
        return (row, col-1)

def egrainer(jeu, coup):
    """Retourne la case finale"""
    row = coup[0]
    col = coup[1]
    grains = game.getCaseVal(jeu, row, col)
    case = coup
    jeu[0][row][col] = 0
    while grains > 0:
        case = nextCase(case[0], case[1])
        if case != coup:
            jeu[0][case[0]][case[1]] += 1
            grains -= 1
    return case

def joueCoup(jeu, coup):
    row, col = egrainer(jeu, coup)
    copyJeu = game.getCopieJeu(jeu)

    joueur = game.getJoueur(jeu)
    campAdverse = joueur % 2
    grains = game.getCaseVal(jeu, row, col)

    while(row == campAdverse and (grains == 2 or grains == 3)):
        jeu[0][row][col] = 0
        jeu[4][joueur-1] += grains
        row, col = prevCase(row, col)
        grains = game.getCaseVal(jeu, row, col)

    if adversaireAffame(jeu):
        jeu[0] = copyJeu[0]
        jeu[4] = copyJeu[4]

    game.changeJoueur(jeu)
    jeu[2] = None
    jeu[3].append(coup)



def printPlateau(jeu):
	plateau = jeu[0]

	for i in range(len(plateau[0])):
		if i == 0:
			print("%5s|" %(""), end="")
		print("%3s  |" %(i), end="")

	print("\n", "-"*6*7)

	for i in range(len(plateau)):
		print("%3s  |" %(i), end="")
		for j in range(len(plateau[i])):
			if plateau[i][j] == 0:
				print("%5s|" %(""), end="")
			else:
				print("%3s  |" %(plateau[i][j]), end="")

		print("\n", "-"*6*7)

def affiche(jeu):
	""" jeu -> void
        Affiche l'etat du jeu de la maniere suivante :
                Coup joue = <dernier coup>
                Scores = <score 1>, <score 2>
                Plateau : ...

                Joueur <joueur>, a vous de jouer
        Hypothese : le contenu de chaque case ne depasse pas 5 caracteres
    """
	print("Last coup joue =", "Aucun" if not jeu[3] else jeu[3][-1])
	print(f"Scores = {jeu[4]}")
	print("Plateau:")
	printPlateau(jeu)
	print(f"Joueur {jeu[1]}, a vous de jouer\n")
