import game
if game.GUI: import pygame

def get_move(game_info):
    """ game_info -> move
        Retourne un move a jouer
    """
    l = None
    c = None
    if not game.GUI:
        print("Coups valides: ", game.get_valid_moves(game_info))
        l = int(input("Votre row: "))
        c = int(input("Votre col: "))
        while (l, c) not in game.get_valid_moves(game_info):
            print("Coup invalide !")
            l = int(input("Votre row: "))
            c = int(input("Votre col: "))
        return (l, c)

    else:
        SIZE = game.game.SIZE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    l, c = y//SIZE, x//SIZE
                if (l, c) in game.get_valid_moves(game_info):
                    return (l, c)
