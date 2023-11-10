
class Player:
    def __init__(self, symbol, is_ai=False):
        self.symbol = symbol
        self.is_ai = is_ai

    def make_move(self, column, game_board):
        return game_board.make_move(column, self.symbol)

    def user_input(self, board):
        while True:
            try:
                column = int(input(f"Player {self.symbol}, enter the colum (1-{board.columns}): "))
                if 1 <= column <= board.columns and board.check_valid_move(column):
                    return column
                else:
                    print("Invalid move!")
            except ValueError:
                print("You must enter number!")
