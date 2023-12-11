import math
import random
import sys
from copy import deepcopy

EMPTY_PIECE = " "
PLAYER_PIECE = "X"
COMPUTER_PIECE = "O"
ROWS = 6
COLUMNS = 7


def minimax_with_alphabeta(board_array, depth, alpha, beta, maximizing_player):
    """
    Suorittaa minimax-algoritmin alphabeta-karsinnalla.

    Args:
        :param board_array: pelilauta
        :param depth: syvyyden rajoitus
        :param alpha: alfan arvo
        :param beta: betan arvo
        :param maximizing_player: totuusarvo, joka kertoo
         onko vuorossa maksimoiva pelaaja

    :return:
        Tuple (column, value), jossa column on valittu sarake ja value sen arvo
    """

    if depth == 0 or game_over(board_array, PLAYER_PIECE, COMPUTER_PIECE):
        if game_over(board_array, PLAYER_PIECE, COMPUTER_PIECE):
            if check_winner(board_array, COMPUTER_PIECE):
                return None, 9999999
            if check_winner(board_array, PLAYER_PIECE):
                return None, -9999999
            # game is over, no more valid moves
            return None, 0
        # depth is zero
        return None, evaluate(board_array, COMPUTER_PIECE)

    if maximizing_player:
        value = -9999999
        column = random.choice(get_valid_locations(board_array))
        for col in get_valid_locations(board_array):
            b_copy = deepcopy(board_array)
            drop_piece(b_copy, col, COMPUTER_PIECE)
            new_score = minimax_with_alphabeta(b_copy,
                                               depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = 9999999
        column = random.choice(get_valid_locations(board_array))
        for col in get_valid_locations(board_array):
            b_copy = deepcopy(board_array)
            drop_piece(b_copy, col, PLAYER_PIECE)
            new_score = minimax_with_alphabeta(b_copy,
                                               depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def initialize_board():
    return [[EMPTY_PIECE for _ in range(COLUMNS)] for _ in range(ROWS)]


def check_winner(board_array, piece):
    """
    Tarkistaa, onko annetulla pelinappulalla voitettu peli

    Args:
        :param board_array: pelilauta
        :param piece: pelajaan pelinappula
    :return:
        totuusarvo, joka kertoo onko voitettu
    """
    # Check horizontal locations
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board_array[r][c] == piece and board_array[r][c + 1]\
                    == piece and board_array[r][c + 2] == piece and \
                    board_array[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board_array[r][c] == piece and board_array[r + 1][c]\
                    == piece and board_array[r + 2][c] == piece and \
                    board_array[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board_array[r][c] == piece and board_array[r + 1][c + 1]\
                    == piece and board_array[r + 2][
                c + 2] == piece and board_array[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board_array[r][c] == piece and board_array[r - 1][c + 1]\
                    == piece and board_array[r - 2][
                c + 2] == piece and board_array[r - 3][c + 3] == piece:
                return True

    return False


def game_over(board_array, player_piece, computer_piece):
    for piece in [player_piece, computer_piece]:
        if check_winner(board_array, piece):
            return True

    if all(board_array[0][c] is not EMPTY_PIECE for c in range(COLUMNS)):
        return True

    return False


def is_valid_drop(board_array, col):
    return board_array[0][col] == EMPTY_PIECE


def get_next_open_row(board_array, col):
    for row in range(ROWS - 1, -1, -1):
        if board_array[row][col] is EMPTY_PIECE:
            return row


def drop_piece(board_array, col, piece):
    if not is_valid_drop(board_array, col):
        print("Tried invalid drop at column", col)
        sys.exit(0)

    row = get_next_open_row(board_array, col)
    board_array[row][col] = piece


def get_valid_locations(board_array):
    """
    Etsii ja palauttaa listan sarakkeista joihin pelinappula voidaan pudottaa

    Args:
        :param board_array: pelilauta
    :return:
        Lista indekseistä, joihin pelinappula voidaan pudottaa
    """
    valid_locations = []
    for col in range(COLUMNS):
        if is_valid_drop(board_array, col):
            valid_locations.append(col)
    return valid_locations


def print_board(board_array):
    s = ""
    for row in board_array:
        for cell in row:
            if cell == EMPTY_PIECE:
                s += "-" + " "
            elif cell == PLAYER_PIECE:
                s += "\033[32m" + cell + " " + "\033[0m"
            else:
                s += "\033[31m" + cell + " " + "\033[0m"
        s += "\n"
    for i in range(1, COLUMNS + 1):
        s += str(i) + " "
    s += "\n"
    print(s)


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == COMPUTER_PIECE else COMPUTER_PIECE
    empty = EMPTY_PIECE

    piece_count = window.count(piece)
    opp_piece_count = window.count(opp_piece)
    empty_count = window.count(empty)

    # four in a row
    if piece_count == 4:
        score += 100

    # three in a row with one empty
    elif piece_count == 3 and empty_count == 1:
        score += 10

    # two in a row with two empty
    elif piece_count == 2 and empty_count == 2:
        score += 5

    # two in a row with an empty space on either side
    if piece_count == 2 and empty_count == 2\
            and (window[0] == empty or window[3] == empty):
        score += 3

    # penalty if opponent has three in a row with one empty
    if opp_piece_count == 3 and empty_count == 1:
        score -= 8

    # opponent has two in a row with two empty
    if opp_piece_count == 2 and empty_count == 2:
        score -= 4

    # bonus for central column presence
    #if window[1] == piece or window[2] == piece:
        #score += 2

    return score


def evaluate(board_array, piece):
    score = 0

    # Score Horizontal
    for r in range(ROWS):
        row_array = [i for i in board_array[r]]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMNS):
        col_array = [row[c] for row in board_array]
        for r in range(ROWS - 3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board_array[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board_array[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def play_game():
    while True:
        try:
            col = int(input("Select column to drop (1-{}): ".format(COLUMNS)))
            if 1 <= col <= COLUMNS:
                return col - 1  # match the 0-based indexing of the board_array
            else:
                print("Please enter a number between 1 and {}.".format(COLUMNS))
        except ValueError:
            print("Invalid input!")


#board = [[EMPTY_PIECE for _ in range(COLUMNS)] for _ in range(ROWS)]
#PLAYER_TURN = True

def main():
    board = initialize_board()
    player_turn = True
    print_board(board)

    while not game_over(board, PLAYER_PIECE, COMPUTER_PIECE):
        if player_turn:
            col = play_game()
            while col not in get_valid_locations(board):
                col = play_game()
            drop_piece(board, col, PLAYER_PIECE)
        else:
            col, _ = minimax_with_alphabeta(board, 5, -math.inf, math.inf, True)
            print("Computer drops", col + 1)
            if is_valid_drop(board, col):
                drop_piece(board, col, COMPUTER_PIECE)

        print_board(board)
        player_turn = not player_turn

    # print result
    if check_winner(board, COMPUTER_PIECE):
        print("Computer wins!")
    elif check_winner(board, PLAYER_PIECE):
        print("Player wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
