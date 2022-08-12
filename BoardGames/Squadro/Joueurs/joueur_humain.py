import game
if game.GUI: import pygame
from Squadro import squadro


def saisieCoup(jeu):
    """ jeu -> coup
        Retourne un coup a jouer
    """
    l = None
    c = None
    if not game.GUI:
        print("Coups valides: ", game.getCoupsValides(jeu))
        l = int(input("Votre ligne: "))
        c = int(input("Votre colonne: "))
        while (l, c) not in game.getCoupsValides(jeu):
            print("Coup invalide !")
            l = int(input("Votre ligne: "))
            c = int(input("Votre colonne: "))
        return (l, c)

    else:
        rects = sum(squadro.RECTS.values(), [])
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None

                x, y = pygame.mouse.get_pos()
                for rect in rects:
                    if rect.collidepoint((x,y)):
                        if pygame.mouse.get_pressed()[0]:
                            if jeu[1] == 1:
                                l = (y+game.game.PIECE_WIDTH)//game.game.SIZE
                                c = (x+game.game.PIECE_LENGTH)//game.game.SIZE if x > game.game.PIECE_LENGTH else 0
                            else:
                                l = (y+game.game.PIECE_LENGTH)//game.game.SIZE if y > game.game.PIECE_LENGTH else 0
                                c = (x+game.game.PIECE_WIDTH)//game.game.SIZE
                        if (l, c) in game.getCoupsValides(jeu):
                            return (l, c)
