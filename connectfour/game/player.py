import random
from copy import deepcopy
from game.board import GameBoard


class Player:
    def __init__(self, symbol, is_ai=False):
        """Alustaa Pelaaja-olion annetulla symbolilla

        Args:
            symbol: Pelaajan symboli
            is_ai: True jos pelaaja on tekoäly, muuten False
        """
        self.symbol = symbol
        self.is_ai = is_ai

    def make_move(self, column, board):
        """
        Pelaajan siirto annetussa sarakkeessa.

        Args:
            :param column: Sarake, johon siirto tehdään
            :param board: Pelilauta, jolla siirto tehdään

        Returns:
            bool: True, jos siirto onnistuu, muuten False
        """
        return board.make_move(column, self.symbol)

    def user_input(self, board):
        """
        Käyttäjän syötteen pyytäminen ja tarkistaminen.

        Args:
            :param board: pelilauta, jolla syötettä tarkistetaan

        Returns:
            int: käyttäjän valitsema sarake
        """
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
        """
        Tekee tekoälyn tai käyttäjän valitseman siirron laudalla.

        Args:
            :param board: pelilauta, jolla siirto tehdään

        Returns:
            int: valittu sarake
        """
        vcolumns = [col for col in range(1, board.columns + 1) if board.check_valid_move(col)]
        return random.choice(vcolumns) if vcolumns else None
        #return self.make_ai_move(board)

    def make_ai_move(self, board):
        # if self.is_ai:
        # return self.minimax_move(board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True)
        # else:
        # return self.user_input(board)
        if self.is_ai:
            return self.ai_move(board)
        else:
            return self.user_input(board)

    def opponent_symbol(self):
        return 'O' if self.symbol == 'X' else 'X'

    def minimax_move(self, board, depth, alpha, beta, maximizing):
        if depth == 0 or board.winner_check(self.symbol) or board.winner_check(self.opponent_symbol()):
            return self.evaluate(board)

        valid_columns = [col for col in range(1, board.columns + 1) if board.check_valid_move(col)]

        if maximizing:
            max_evaluate = float('-inf')
            best_col = None
            for col in valid_columns:
                new_board = GameBoard()
                new_board.board = deepcopy(board.board)

                if new_board.make_move(col, self.symbol):
                    eval = self.minimax_move(new_board, depth - 1, alpha, beta, False)

                    if eval is not None:
                        max_evaluate = max(max_evaluate, eval)
                        alpha = max(alpha, eval)

                        if beta <= alpha:
                            break

                        if eval > max_evaluate:
                            max_evaluate = eval
                            best_col = col

            return best_col
        else:
            min_evaluate = float('inf')
            best_col = None
            for col in valid_columns:
                new_board = GameBoard()
                new_board.board = deepcopy(board.board)

                if new_board.make_move(col, self.opponent_symbol()):
                    eval = self.minimax_move(board, depth - 1, alpha, beta, True)

                    if eval is not None:
                        min_evaluate = min(min_evaluate, eval)
                        beta = min(beta, eval)

                        if beta <= alpha:
                            break

                        if eval < min_evaluate:
                            min_evaluate = eval
                            best_col = col

            return best_col

    def evaluate(self, board):
        ai = self.symbol
        opponent = self.opponent_symbol()

        score = 0

        # rows
        for row in board.board:
            score += self.eval_sequence(row, ai, opponent)

        # columns
        for col in range(board.columns):
            column = [row[col] for row in board.board]
            score += self.eval_sequence(column, ai, opponent)

        # diagonals
        for i in range(board.rows - 3):
            for j in range(board.columns - 3):
                diagonal = [board.board[i + k][j + k] for k in range(4)]
                score += self.eval_sequence(diagonal, ai, opponent)

        for i in range(3, board.rows):
            for j in range(board.columns - 3):
                diagonal = [board.board[i - k][j + k] for k in range(4)]
                score += self.eval_sequence(diagonal, ai, opponent)

        return score

    def eval_sequence(self, sequence, ai, opponent):
        score = 0
        ai_count = sequence.count(ai)
        opponent_count = sequence.count(opponent)
        empty = sequence.count(None)

        if ai_count == 4:
             score += 100

        elif ai_count == 3 and empty == 1:
            score += 10

        elif ai_count == 2 and empty == 2:
            score += 5

        if ai_count == 2 and empty == 2 and (sequence[0] == None or sequence[3] == None):
            score += 3

        if opponent_count == 3 and empty == 1:
            score -= 8

        if opponent_count == 2 and empty == 2:
            score -= 4

        if sequence[1] == opponent or sequence[2] == opponent:
            score += 2

        return score
