#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
grandparent = os.path.dirname(parent)
sys.path.append(grandparent)
import game
import math
import random

AI_PLAYER = None
OPPONENT = None
INFINITY = float("inf")
SQRT2 = math.sqrt(2)

#################################################################################
c = SQRT2
def UCB1(Si):
    if Si.ni == 0 or Si.parent.ni is None: return INFINITY
    return Si.wi/Si.ni + c*math.sqrt(math.log(Si.parent.ni/Si.ni))

class Node:
    def __init__(self, jeu, parent=None):
        self.jeu = jeu
        self.parent = parent
        self.children = []
        self.wi = 0
        self.ni = 0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def get_random_child(self):
        return random.choice(self.children) if self.children else None

    def get_max_child(self):
        if not self.children: return None
        return max(self.children, key=lambda c: UCB1(c))
#################################################################################

NB_ITERATIONS = 1000
NB_ROLLOUTS = 1

def saisieCoup(jeu):
    global AI_PLAYER, OPPONENT
    AI_PLAYER = game.getJoueur(jeu)
    OPPONENT = AI_PLAYER%2 + 1

    # Init
    ROOT = Node(jeu)
    for coup in game.getCoupsValides(jeu):
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)
        ROOT.add_child(Node(j))

    # Selection - Expansion - Rollout - Backpropagation
    for _ in range(NB_ITERATIONS):
        leaf = select(ROOT)

        if game.finJeu(leaf.jeu):
            backpropagate(leaf, NB_ROLLOUTS) if game.getGagnant(leaf.jeu) == AI_PLAYER else backpropagate(leaf, 0)
            continue

        if leaf.ni == 0:
            score = rollout(leaf)
        else:
            children = expand(leaf)
            score = rollout(children[0])

        backpropagate(leaf, score)

    # Best coup
    vmax = -INFINITY
    bestCoup = None
    for c in ROOT.children:
        if c.ni > vmax:
            vmax = c.ni
            bestCoup = c.jeu[3][-1]
    return bestCoup

def select(root):
    node = root
    while node.children:
        node = node.get_max_child()
    return node

def expand(leaf):
    jeu = leaf.jeu
    for coup in game.getCoupsValides(jeu):
        j = game.getCopieJeu(jeu)
        game.joueCoup(j, coup)
        leaf.add_child(Node(j))
    return leaf.children

def rollout(leaf):
    jeu = leaf.jeu
    score = 0
    for _ in range(NB_ROLLOUTS):
        j = game.getCopieJeu(jeu)
        while not game.finJeu(j):
            try: coup = random.choice(game.getCoupsValides(j))
            except: print(game.getCoupsValides(j))
            game.joueCoup(j, coup)
        if game.getGagnant(j) == AI_PLAYER: score += 1
    return score

def backpropagate(leaf, score):
    node = leaf
    while node is not None:
        node.wi += score
        node.ni += 1
        node = node.parent
