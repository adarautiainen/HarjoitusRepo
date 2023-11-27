from __future__ import annotations
import copy
import math


def minimax(board: Board, player: Player, max_depth, current_depth) -> (float, Move):
    if board.is_game_over() or current_depth == max_depth:
        if board.is_game_over():
            if board.check_winner(player):
                return math.inf, None
            elif not board.check_winner(player):
                return -math.inf, None
            else:
                return 0, None
        else:
            return board.evaluate(player), None

    if board.current_player() == player:
        best_score = -math.inf
    else:
        best_score = math.inf

    best_move = None
    for move in board.get_moves():
        new_board = board.make_move(move)
        new_board.switch_player()

        # recurse
        current_score, current_move = minimax(new_board, player, max_depth, current_depth + 1)

        if board.current_player() == player:
            if current_score > best_score:
                best_score = current_score
                best_move = move
        else:
            if current_score < best_score:
                best_score = current_score
                best_move = move

    return best_score, best_move


class Board:
    columns = 7
    rows = 6

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.active_player = self.player1

        self.board = [[None for _ in range(Board.columns)] for _ in range(Board.rows)]

    def get_moves(self) -> list[Move]:
        valid_moves = []
        for col in range(Board.columns):
            if self.board[0][col] is None:
                valid_moves.append(Move(self.active_player, col))
        return valid_moves

    def get_open_row(self, col: int):
        for row in range(Board.rows - 1, -1, -1):
            if self.board[row][col] is None:
                return row

    def make_move(self, move: Move) -> Board:
        new_board = copy.copy(self)
        new_board.board = copy.deepcopy(self.board)

        col = move.get_column()
        row = new_board.get_open_row(col)
        new_board.board[row][col] = new_board.current_player().get_symbol()

        return new_board

    def evaluate(self, player: Player) -> float:
        score = 0

        # horizontal
        for r in range(Board.rows):
            row_array = [i for i in self.board[r]]
            for c in range(Board.columns - 3):
                seq = row_array[c:c + 4]
                score += self.evaluate_window(seq, player)

        # vertical
        for c in range(Board.columns):
            col_array = [row[c] for row in self.board]
            for r in range(Board.rows - 3):
                seq = col_array[r:r + 4]
                score += self.evaluate_window(seq, player)

        # diagonals
        for r in range(Board.rows - 3):
            for c in range(Board.columns - 3):
                seq = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(seq, player)

        for r in range(Board.rows - 3):
            for c in range(Board.columns - 3):
                seq = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(seq, player)

        return score

    def evaluate_window(self, window, player: Player):
        score = 0

        player_symbol = player.get_symbol()
        if player == self.player1:
            opponent = self.player2.get_symbol()
        else:
            opponent = self.player1.get_symbol()

        symbol_count = window.count(player_symbol)
        opponent_count = window.count(opponent)
        empty_count = window.count(None)

        # highest score for four in a row
        if symbol_count == 4:
            score += 100
        # three in a row
        elif symbol_count == 3 and empty_count == 1:
            score += 10
        # two in a row
        elif symbol_count == 2 and empty_count == 2:
            score += 5

        # two in a row with empty space on either side
        if symbol_count == 2 and empty_count == 2 and (window[0] == None or window[3] == None):
            score += 3
        # opponent has three in a row
        if opponent_count == 3 and empty_count == 1:
            score -= 8
        # opponent has two in a row
        if opponent_count == 2 and empty_count == 2:
            score -= 4

        return score

    def current_player(self) -> Player:
        return self.active_player

    def switch_player(self):
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def is_game_over(self) -> bool:
        for player in [self.player1, self.player2]:
            if self.check_winner(player):
                return True

        if all(self.board[0][c] is not None for c in range(Board.columns)):
            return True

        return False

    def check_winner(self, player: Player) -> bool:
        symbol = player.get_symbol()

        # horizontal check
        for row in self.board:
            if f"{symbol * 4}" in "".join(str(cell) if cell is not None else '' for cell in row):
                return True

        # vertical check
        for column in range(Board.columns):
            if f"{symbol * 4}" in "".join(str(row[column]) if row[column] is not None else '' for row in self.board):
                return True

        # diagonal check left->right
        for i in range(Board.rows - 3):
            for j in range(Board.columns - 3):
                if all(str(self.board[i + k][j + k]) == symbol if self.board[i + k][j + k] is not None else '' for k in
                       range(4)):
                    return True

        # diagonal check right->left
        for i in range(3, Board.rows):
            for j in range(Board.columns - 3):
                if all(str(self.board[i - k][j + k]) == symbol if self.board[i - k][j + k] is not None else '' for k in
                       range(4)):
                    return True

        return False

    def display_board(self):
        s = ""
        for row in self.board:
            for col in row:
                if col == None:
                    s += "-" + " "
                elif col == self.player1.get_symbol():
                    color = self.player1.get_color()
                    s += color + col + " " + "\033[0m"
                else:
                    color = self.player2.get_color()
                    s += color + col + " " + "\033[0m"
            s += "\n"

        for i in range(1, Board.columns + 1):
            s += str(i) + " "
        s += "\n"

        print(s)


class Player:
    def __init__(self, name, symbol, color):
        self.name = name
        self.symbol = symbol
        self.color = color

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_color(self):
        return self.color

    def get_move(self, board: Board) -> Move:
        pass


class HumanPlayer(Player):

    def __init__(self, name, symbol, color):
        super().__init__(name, symbol, color)

    def get_move(self, board: Board) -> Move:
        valid_moves = board.get_moves()
        valid_columns = [move.get_column() + 1 for move in valid_moves]

        col = None
        while col not in valid_columns:
            try:
                prompt = "'{}' select column for drop {}:".format(self.name, valid_columns)
                col = int(input(prompt))
                if col not in valid_columns:
                    print("Invalid column!")
            except ValueError:
                print("Invalid input!")

        return Move(self, col - 1)


class ComputerPlayer(Player):
    def __init__(self, name, symbol, color):
        super().__init__(name, symbol, color)

    def get_move(self, board: Board) -> Move:
        score, move = minimax(board, self, 5, 0)
        print("{} plays {} with score {}".format(self.name, move.get_column() + 1, score))
        return move


class Move:
    def __init__(self, player: Player, column):
        self.player = player
        self.column = column

    def get_column(self) -> int:
        return self.column

    def get_player(self) -> Player:
        return self.player


class ConnectFour():
    def __init__(self, player1: Player, player2: Player):
        self.turn = 0
        self.board = Board(player1, player2)

    def run(self):
        while not self.board.is_game_over():
            self.board.display_board()
            current_player = self.board.current_player()
            move = current_player.get_move(self.board)
            self.board = self.board.make_move(move)
            self.board.switch_player()

        self.board.display_board()
        print("Game over!")


if __name__ == "__main__":
    player1 = HumanPlayer("Human1", "X", "\033[32m")
    computer = ComputerPlayer("Computer", "O", "\033[31m")
    game = ConnectFour(player1, computer)
    game.run()
