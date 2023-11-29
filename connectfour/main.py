from connectfour.game.player import Player
from connectfour.game.board import GameBoard


def main():
    board = GameBoard()
    player1 = Player('X', is_ai=False)
    player2 = Player('O', is_ai=True)

    while not board.winner_check(player1.symbol) and \
            not board.winner_check(player2.symbol):
        # human plays
        column = player1.user_input(board)
        player1.make_move(column, board)
        board.display_board()
        if board.winner_check(player1.symbol):
            print(f"Player with symbol {player1.symbol} wins!")
            break

        if board.is_board_full():
            print("It's a tie!")
            board.display_board()
            break

        # ai plays
        print("Next computer plays: ")
        column_ai = player2.make_ai_move(board)
        player2.make_move(column_ai, board)
        #board.make_move(column_ai, player2.symbol)
        board.display_board()
        if board.winner_check(player2.symbol):
            print(f"Player with symbol {player2.symbol} wins!")
            board.display_board()
            break

        if board.is_board_full():
            print("It's a tie!")
            board.display_board()
            break


if __name__ == "__main__":
    main()
