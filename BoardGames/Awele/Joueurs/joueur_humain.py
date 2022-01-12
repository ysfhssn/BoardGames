#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(grandparent)
import game

def saisieCoup(jeu):
    print("Coups valides: ", game.getCoupsValides(jeu))
    row = game.getJoueur(jeu) - 1
    col = int(input("Votre colonne: "))

    while((row, col) not in game.getCoupsValides(jeu)):
        col = int(input("Coup invalide !\nVotre colonne: "))

    return (row, col)