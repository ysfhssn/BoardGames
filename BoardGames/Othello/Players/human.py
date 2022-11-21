import game
if game.GUI: import pygame

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
        SIZE = game.game.SIZE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    l, c = y//SIZE, x//SIZE
                if (l, c) in game.get_valid_moves(game_info):
                    return (l, c)
