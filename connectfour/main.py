from game.board import GameBoard
from game.player import Player


def main():
    board = GameBoard()
    player1 = Player('X', is_ai=False)
    player2 = Player('O', is_ai=True)

    while not board.winner_check(player1.symbol) and not board.winner_check(player2.symbol):
        board.display_board()

        # human plays
        column = player1.user_input(board)
        player1.make_move(column, board)
        if board.winner_check(player1.symbol):
            print(f"Player with symbol {player1.symbol} wins!")
            break

        board.display_board()

        # ai plays
        column_ai = player2.make_ai_move(board)
        player2.make_move(column_ai, board)
        if board.winner_check(player2.symbol):
            print(f"Player with symbol {player2.symbol} wins!")
            break


if __name__ == "__main__":
    main()
