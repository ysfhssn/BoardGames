import game
import random

def saisieCoup(jeu):
    return random.choice(game.getCoupsValides(jeu))
