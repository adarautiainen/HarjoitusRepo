
class Player:
    def __init__(self, symbol, is_ai=False):
        self.symbol = symbol
        self.is_ai = is_ai

    def make_move(self, column, game_board):
        return game_board.make_move(column, self.symbol)