import game
if game.GUI: import pygame

def get_move(game_info):
    col = None

    if not game.GUI:
        print("Valid moves: ", game.get_valid_moves(game_info))

        col = int(input("Col: "))

        while col not in game.get_valid_moves(game_info):
            col = int(input("Invalid move !\nCol: "))

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
                    if col in game.get_valid_moves(game_info):
                        return col
                else:
                    draw_board(game_info, update=False)
                    pygame.draw.circle(WIN, RED if game_info[1] == 1 else YELLOW, (x, SIZE//2 + 2), SIZE//2 - 2)

            pygame.display.update()
