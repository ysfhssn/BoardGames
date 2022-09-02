import game

def get_move(game_info):
    print("Coups valides: ", game.get_valid_moves(game_info))
    row = game.get_player(game_info) - 1
    col = int(input("Votre col: "))

    while((row, col) not in game.get_valid_moves(game_info)):
        col = int(input("Coup invalide !\nVotre col: "))

    return (row, col)
