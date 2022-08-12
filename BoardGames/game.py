#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""
    NOMENCLATURE A RESPECTER
    coup = (int, int)
    jeu = List[...] :
        0: plateau      	List[List[int]]
        1: joueur       	int (1 ou 2)
        2: coups valides	List[(int, int)]
        3: coups joues  	List[(int, int)]
        4: scores       	List[int, int]
"""

game	= None #Contient le module du jeu specifique: awele ou othello
joueur1	= None #Contient le module du joueur 1
joueur2	= None #Contient le module du joueur 2
GUI     = True


############################## Fonctions minimales ##############################

############### Fonctions utiles ###############
def getPlateau(jeu):
    """ jeu -> plateau
        Retourne le plateau du jeu passe en parametre
    """
    return jeu[0]

def getJoueur(jeu):
    """ jeu -> nat
        Retourne le joueur a qui c'est le tour de jouer dans le jeu passe en parametre
    """
    return jeu[1]

def changeJoueur(jeu):
    """ jeu -> void
        Change le joueur a qui c'est le tour de jouer dans le jeu passe en parametre (1 ou 2)
    """
    jeu[1] = 2 if jeu[1] == 1 else 1

def getGagnant(jeu):
    """ jeu -> nat
        Retourne le numero du joueur gagnant apres avoir finalise la partie. Retourne 0 si match nul
    """
    if jeu[4][0] == jeu[4][1]:
        return 0
    return 1 if jeu[4][0] > jeu[4][1] else 2

# Attention ce getter est specifique a un jeu !!!
def getCoupsValides(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups valides dans le jeu passe en parametre
        Si None, alors on met a jour la liste des coups valides
    """
    return game.getCoupsValides(jeu)

def getCoupsJoues(jeu):
    """ jeu -> List[coup]
        Retourne la liste des coups joues dans le jeu passe en parametre
    """
    return jeu[3]

def getScores(jeu):
    """ jeu -> Pair[nat nat]
        Retourne les scores du jeu passe en parametre
    """
    return jeu[4]

def getScore(jeu, joueur):
    """ jeu * nat -> int
        Retourne le score du joueur
        Hypothese: le joueur est 1 ou 2
    """
    return jeu[4][0] if joueur == 1 else jeu[4][1]

def getCaseVal(jeu, ligne, colonne):
    """ jeu * nat * nat -> nat
        Retourne le contenu de la case ligne,colonne du jeu
        Hypothese: les numeros de ligne et colonne appartiennent bien au plateau  : ligne<=getNbLignes(jeu) and colonne<=getNbColonnes(jeu)
    """
    return jeu[0][ligne][colonne]

def getCopieJeu(jeu):
    """ jeu -> jeu
        Retourne une copie du jeu passe en parametre
        Quand on copie un jeu on en calcule forcement les coups valides avant
    """
    jeu_copy = []
    for i in jeu:
        if isinstance(i, list):
            if i != [] and isinstance(i[0], list): jeu_copy.append([ii[:] for ii in i])
            else: jeu_copy.append(i[:])
        else: jeu_copy.append(i)
    return jeu_copy

def coupValide(jeu, coup):
    """ jeu * coup -> bool
        Retourne vrai si le coup appartient a la liste de coups valides du jeu
    """
    return coup in jeu[2]



######### Fonctions specifiques a un jeu #########
def initialiseJeu():
    """ void -> jeu
        Initialise le jeu (nouveau plateau, liste des coups joues vide, liste des coups valides None, scores a 0 et joueur = 1)
    """
    return game.initialiseJeu()

def initialiseInteressant(key=0):
    return game.initialiseInteressant(key)

def finJeu(jeu):
    """ jeu -> bool
        Retourne vrai si c'est la fin du jeu
    """
    return game.finJeu(jeu)

def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
        On suppose que la fonction n'est appelee que si il y a au moins un coup valide possible
        et qu'elle retourne obligatoirement un coup valide
    """
    joueur = getJoueur(jeu)
    return joueur1.saisieCoup(jeu) if joueur == 1 else joueur2.saisieCoup(jeu)

def joueCoup(jeu, coup):
    """ jeu * coup -> void
        Joue un coup a l'aide de la fonction joueCoup defini dans le module game
        Hypothese: le coup est valide
        Met tous les champs de jeu a jour (sauf coups valides qui est fixe a None)
    """
    game.joueCoup(jeu, coup)

def affiche(jeu):
    """ jeu -> void
        Affiche l'etat du jeu de la maniere suivante :
            Coup joue = <dernier coup>
            Scores = <score 1>, <score 2>
            Plateau :

                       |       0     |     1       |      2     |      ...
                ------------------------------------------------
                    0  | <Case 0,0>  | <Case 0,1>  | <Case 0,2> |      ...
                ------------------------------------------------
                    1  | <Case 1,0>  | <Case 1,1>  | <Case 1,2> |      ...
                ------------------------------------------------
                  ...  |     ...     |     ...     |     ...    |      ...

            Joueur <joueur>, a vous de jouer
    """
    game.affiche(jeu)


if __name__ == "__main__":
    if GUI:
        import games_selection
        games_selection.selection()
    else:
        print("GUI mode is off")
