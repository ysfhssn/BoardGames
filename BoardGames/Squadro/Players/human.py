import game
if game.GUI: import pygame
from Squadro import squadro


def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    l = None
    c = None
    if not game.GUI:
        print("Valid moves: ", game.get_valid_moves(game_info))
        l = int(input("Row: "))
        c = int(input("Col: "))
        while (l, c) not in game.get_valid_moves(game_info):
            print("Invalid move !")
            l = int(input("Row: "))
            c = int(input("Col: "))
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
                            if game_info[1] == 1:
                                l = (y+game.game.PIECE_WIDTH)//game.game.SIZE
                                c = (x+game.game.PIECE_LENGTH)//game.game.SIZE if x > game.game.PIECE_LENGTH else 0
                            else:
                                l = (y+game.game.PIECE_LENGTH)//game.game.SIZE if y > game.game.PIECE_LENGTH else 0
                                c = (x+game.game.PIECE_WIDTH)//game.game.SIZE
                        if (l, c) in game.get_valid_moves(game_info):
                            return (l, c)
