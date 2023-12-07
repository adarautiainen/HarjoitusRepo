from game.connect4 import *

"""
def main():
    board = initialize_board()
    PLAYER_PIECE = "X"
    COMPUTER_PIECE = "O"
    PLAYER_TURN = True

    print_board(board)

    while not game_over(board, PLAYER_PIECE, COMPUTER_PIECE):
        if PLAYER_TURN:
            col = play_game()
            while col not in get_valid_locations(board):
                col = play_game()
            drop_piece(board, col, PLAYER_PIECE)
        else:
            col, _ = minimax_with_alphabeta(board, 6, -math.inf, math.inf, True)
            print("Computer drops", col + 1)
            if is_valid_drop(board, col):
                drop_piece(board, col, COMPUTER_PIECE)

        print_board(board)
        PLAYER_TURN = not PLAYER_TURN

    if check_winner(board, COMPUTER_PIECE):
        print("Computer wins!")
    elif check_winner(board, PLAYER_PIECE):
        print("Player wins!")
    else:
        print("Draw!")
"""

if __name__ == "__main__":
    main()
