from game.board import GameBoard
from game.player import Player


def main():
    board = GameBoard()
    player1 = Player('X', is_ai=False)

    while not board.winner_check('X') and not board.winner_check('O'):
        column = player1.user_input(board)
        player1.make_move(column, board)
        board.display_board()


if __name__ == "__main__":
    main()
