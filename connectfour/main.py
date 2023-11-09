from game.board import GameBoard
from game.player import Player


def main():
    board = GameBoard()
    player1 = Player('X', is_ai=False)
    player2 = Player('O', is_ai=True)
    # player1.make_move(3, board)
    board.display_board()


if __name__ == "__main__":
    main()
