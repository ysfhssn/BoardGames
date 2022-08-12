import game

def saisieCoup(jeu):
    print("Coups valides: ", game.getCoupsValides(jeu))
    row = game.getJoueur(jeu) - 1
    col = int(input("Votre colonne: "))

    while((row, col) not in game.getCoupsValides(jeu)):
        col = int(input("Coup invalide !\nVotre colonne: "))

    return (row, col)
