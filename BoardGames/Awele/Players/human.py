import game

def get_move(game_info):
    print("Valid moves: ", game.get_valid_moves(game_info))
    row = game.get_player(game_info) - 1
    col = int(input("Col: "))

    while((row, col) not in game.get_valid_moves(game_info)):
        col = int(input("Invalid move !\nCol: "))

    return (row, col)
