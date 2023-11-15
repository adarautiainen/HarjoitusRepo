import random


class Player:
    def __init__(self, symbol, is_ai=False):
        self.symbol = symbol
        self.is_ai = is_ai

    def make_move(self, column, board):
        return board.make_move(column, self.symbol)

    def user_input(self, board):
        while True:
            try:
                column = int(input(f"Player {self.symbol}, enter the column (1-{board.columns}): "))
                if 1 <= column <= board.columns and board.check_valid_move(column):
                    return column
                else:
                    print("Invalid move!")
            except ValueError:
                print("You must enter number!")

    def ai_move(self, board):
        vcolumns = [col for col in range(1, board.columns + 1) if board.check_valid_move(col)]
        return random.choice(vcolumns) if vcolumns else None

    def make_ai_move(self, board):
        if self.is_ai:
            return self.ai_move(board)
        else:
            return self.user_input(board)


