import game
if game.GUI: import pygame

def saisieCoup(jeu):
    col = None

    if not game.GUI:
        print("Coups valides: ", game.getCoupsValides(jeu))

        col = int(input("Votre colonne: "))

        while col not in game.getCoupsValides(jeu):
            col = int(input("Coup invalide !\nVotre colonne: "))

        return col

    else:
        WIN = game.game.WIN
        SIZE = game.game.SIZE
        RED = game.game.RED
        YELLOW = game.game.YELLOW
        draw_board = game.game.draw_board

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return None
                x, _ = pygame.mouse.get_pos()

                if pygame.mouse.get_pressed()[0]:
                    col = x//SIZE
                    if col in game.getCoupsValides(jeu):
                        return col
                else:
                    draw_board(jeu, update=False)
                    pygame.draw.circle(WIN, RED if jeu[1] == 1 else YELLOW, (x, SIZE//2 + 2), SIZE//2 - 2)

            pygame.display.update()
