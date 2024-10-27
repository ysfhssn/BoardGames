#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
dirname = os.path.dirname(__file__)
parent = os.path.dirname(dirname)
sys.path.append(parent)
import game
import copy
import math

"""

RULES:    http://www.ffjd.fr/Web/index.php?page=reglesdujeu


"""

ROWS = 10
COLS = 10


if game.GUI:
    import pygame
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.SysFont("couriernew", 20)
    HEIGHT = 600 + 50
    WIDTH = 600
    SIZE = WIDTH // ROWS
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")


def init():
    board = [[" "] * ROWS for _ in range(COLS)]
    for i in range(ROWS):
        for j in range(COLS):
            if i % 2 != j % 2:
                if i < 4:
                    board[i][j] = "b"
                elif i > 5:
                    board[i][j] = "w"
    return [board, 1, None, [], [0, 0]]

def init_test(key):
    game_info = init()
    from Checkers.Players import human
    game.player1 = human
    game.player2 = human
    try:
        plats = {
            "MULTIPLE": [
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", "b", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", "", " ", " ",  " ", " "],
                [" ", "b", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", "w", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            ],
            "MULTIPLE_Q": [
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", "b", " ", " ", " ", " ", " ", "W", " ", " "],
                [" ", " ", " ", " ", " ", "", " ", " ",  " ", " "],
                [" ", "b", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", "b", " ", " "],
                [" ", " ", "w", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            ],
            "MULTIPLE_Q2": [
                ["B", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", "w", " ", " ", " ", " ", " ", "b", " ", " "],
                [" ", " ", " ", " ", " ", "", "b", " ",  " ", " "],
                [" ", "w", " ", "w", " ", "w", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "w", " ", "w", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", "w", " ", " "],
                [" ", " ", "b", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            ],
            "MULTIPLE_EQ": [
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", "b", " ", " ", " ", " ", " ", "b", " ", " "],
                [" ", " ", " ", " ", " ", "", " ", " ",  " ", " "],
                [" ", " ", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", "w", " ", " ", " ", " ", " "],
                [" ", "b", " ", " ", " ", " ", " ", "b", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                [" ", " ", " ", "b", " ", "b", " ", " ", " ", " "],
                [" ", " ", " ", " ", "w", " ", " ", " ", " ", " "],
                [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            ]
        }
        game_info[0] = plats[key]
    except: pass
    return game_info

def get_valid_moves(game_info):
    if game_info[2] is None:
        moves = []
        combo_moves = []
        board, player = game_info[0], game_info[1]
        for i in range(ROWS):
            for j in range(COLS):
                piece = board[i][j]
                if (player == 1 and piece in ["w", "W"]) or (player == 2 and piece in ["b", "B"]):
                    piece_moves = get_valid_moves_of_piece(game_info, i, j)
                    for move in piece_moves:
                        if isinstance(move, tuple):
                            moves.append(move)
                        elif isinstance(move, list):
                            combo_moves.append(move)
        game_info[2] = [move for move in combo_moves if len(move) == len(max(combo_moves, key=len))] if combo_moves else moves
    return game_info[2]

def get_valid_moves_of_piece(game_info, row, col):
    board = game_info[0]
    piece = board[row][col]
    if piece == " ":
        return []

    directions = [-1] if piece == "w" else [1] if piece == "b" else [1, -1]
    moves = []
    combo_moves = []

    def capture_chain(current_row, current_col, path, temp_board):
        found_capture = False
        for direction in [-1, 1]:  # Les captures peuvent être faites dans les deux directions
            for delta_col in [-1, 1]:
                mid_row, mid_col = current_row + direction, current_col + delta_col
                new_row, new_col = current_row + 2 * direction, current_col + 2 * delta_col

                # Vérifiez les captures immédiates
                if (0 <= mid_row < ROWS and 0 <= mid_col < COLS and
                    0 <= new_row < ROWS and 0 <= new_col < COLS and
                    ((temp_board[mid_row][mid_col] in ["b", "B"] and piece in ["w", "W"]) or
                     (temp_board[mid_row][mid_col] in ["w", "W"] and piece in ["b", "B"])) and
                    temp_board[new_row][new_col] == " "):

                    new_temp_board = copy.deepcopy(temp_board)
                    new_temp_board[current_row][current_col] = " "
                    new_temp_board[mid_row][mid_col] = " "
                    new_temp_board[new_row][new_col] = piece

                    capture_path = path + [(current_row, current_col, new_row, new_col)]
                    found_capture = True
                    capture_chain(new_row, new_col, capture_path, new_temp_board)

        if not found_capture and path:
            combo_moves.append(path)

    capture_chain(row, col, [], board)

    # Mouvements pour les dames
    if piece in ["W", "B"]:
        for direction in directions:
            for delta_col in [-1, 1]:
                new_row, new_col = row, col
                while True:
                    new_row += direction
                    new_col += delta_col
                    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                        if board[new_row][new_col] == " ":
                            moves.append((row, col, new_row, new_col))
                        elif board[new_row][new_col] in ["b", "B"] if piece in ["w", "W"] else board[new_row][new_col] in ["w", "W"]:
                            # Une pièce adverse est présente, on peut tenter de capturer
                            next_row, next_col = new_row + direction, new_col + delta_col
                            if 0 <= next_row < ROWS and 0 <= next_col < COLS and board[next_row][next_col] == " ":
                                # Capture à distance pour les dames
                                new_temp_board = copy.deepcopy(board)
                                new_temp_board[row][col] = " "
                                new_temp_board[new_row][new_col] = piece
                                new_temp_board[new_row + direction][new_col + delta_col] = " "
                                capture_chain(new_row + direction, new_col + delta_col, [(row, col, next_row, next_col)], new_temp_board)
                            break  # On ne peut pas aller plus loin dans cette direction
                        else:
                            break  # Une pièce amicale est présente, on ne peut pas se déplacer
                    else:
                        break  # Sortie du damier

    # Filtrer pour ne garder que les captures les plus longues
    if combo_moves:
        max_length = max(len(move) for move in combo_moves)
        return [move for move in combo_moves if len(move) == max_length]

    # Ajout des mouvements simples pour les pions
    if piece in ["w", "b"]:
        direction = -1 if piece == "w" else 1
        for delta_col in [-1, 1]:
            new_row, new_col = row + direction, col + delta_col
            if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == " ":
                moves.append((row, col, new_row, new_col))

    return moves

def is_game_over(game_info):
    board = game_info[0]
    white_pieces = any("w" in row or "W" in row for row in board)
    black_pieces = any("b" in row or "B" in row for row in board)
    if not white_pieces: game_info[4][1] = 1
    elif not black_pieces: game_info[4][0] = 1
    return not white_pieces or not black_pieces

def play_move(game_info, move):
    board = game_info[0]

    if isinstance(move, tuple):
        row, col, new_row, new_col = move
        board[new_row][new_col] = board[row][col].upper() if (new_row == 0 and board[row][col] == "w") or (new_row == ROWS-1 and board[row][col] == "b") else board[row][col]
        # Capture
        if abs(new_row - row) >= 2:
            board[new_row - 1 if new_row - row > 0 else new_row + 1][new_col - 1 if new_col - col > 0 else new_col + 1] = " "
        board[row][col] = " "
    elif isinstance(move, list):
        for m in move:
            row, col, new_row, new_col = m
            # Capture
            if abs(new_row - row) >= 2:
                board[new_row - 1 if new_row - row > 0 else new_row + 1][new_col - 1 if new_col - col > 0 else new_col + 1] = " "
            board[new_row][new_col] = board[row][col].upper() if (new_row == 0 and board[row][col] == "w") or (new_row == ROWS-1 and board[row][col] == "b") else board[row][col]
            board[row][col] = " "

    game.change_player(game_info)
    game_info[2] = None
    game_info[3].append(move)

def print_game(game_info):
    board = game_info[0]
    print("   ---------------------------------------")
    for i, row in enumerate(board):
        print(f"{i} | " + " | ".join(row) + " |")
    print("   ---------------------------------------")
    print("    " + "   ".join(map(str, range(COLS))))
    print(f"\nTurn: {'White' if game_info[1] == 1 else 'Black'}")

def draw_piece(piece, center_coords):
    if piece == "w":
        pygame.draw.circle(WIN, (255, 255, 255), center_coords, SIZE // 2 - 3)
    elif piece == "b":
        pygame.draw.circle(WIN, (0, 0, 0), center_coords, SIZE // 2 - 3)
    elif piece == "W":
        pygame.draw.circle(WIN, (255, 255, 255), center_coords, SIZE // 2 - 3)
        pygame.draw.circle(WIN, (200, 200, 200), center_coords, SIZE // 2 - 6)
    elif piece == "B":
        pygame.draw.circle(WIN, (0, 0, 0), center_coords, SIZE // 2 - 3)
        pygame.draw.circle(WIN, (50, 50, 50), center_coords, SIZE // 2 - 6)

def draw_last_move(game_info):
    if game_info[3]:  # Vérifiez si des mouvements ont été effectués
        last_move = [game_info[3][-1]] if isinstance(game_info[3][-1], tuple) else game_info[3][-1]
        for mv in last_move:
            i, j, di, dj = mv
            start_pos = (j * SIZE + SIZE // 2, i * SIZE + SIZE // 2)
            end_pos = (dj * SIZE + SIZE // 2, di * SIZE + SIZE // 2)
            pygame.draw.line(WIN, (139, 69, 19), start_pos, end_pos, 4)
            draw_arrow(start_pos, end_pos)

def draw_arrow(start_pos, end_pos):
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    arrow_length = 10

    p1 = (end_pos[0] - arrow_length * math.cos(angle - math.pi / 6),
          end_pos[1] - arrow_length * math.sin(angle - math.pi / 6))
    p2 = (end_pos[0] - arrow_length * math.cos(angle + math.pi / 6),
          end_pos[1] - arrow_length * math.sin(angle + math.pi / 6))

    pygame.draw.polygon(WIN, (139, 69, 19), [end_pos, p1, p2])

def draw_board(game_info):
    WIN.fill((168, 115, 50))
    board = game_info[0]

    for i in range(ROWS):
        if i != 0:
            pygame.draw.line(WIN, (0, 0, 0), (0, i * SIZE), (WIDTH, i * SIZE))
        for j in range(COLS):
            if j != 0:
                pygame.draw.line(WIN, (0, 0, 0), (j * SIZE, 0), (j * SIZE, WIDTH))

            piece = board[i][j]
            center_coords = (j * SIZE + SIZE // 2, i * SIZE + SIZE // 2)
            draw_piece(piece, center_coords)

    draw_last_move(game_info)

    if is_game_over(game_info):
        winner = "White" if not any("b" in row or "B" in row for row in board) else "Black"
        text_str = f"Winner: {winner}"
    else:
        text_str = f"Player {game_info[1]}'s Turn"
    text = FONT.render(text_str, True, (0, 0, 0) if game_info[1] == 1 else (255, 255, 255))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))

    pygame.display.update()


