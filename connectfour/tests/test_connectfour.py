import unittest
from connectfour.game.connect4 import *


class TestConnectFour(unittest.TestCase):
    def test_minimax(self):
        player1 = HumanPlayer("Human", "X", "\033[32m")
        player2 = ComputerPlayer("Computer", "O", "\033[31m")
        board = Board(player1, player2)

        result_score, result_move = minimax(board, player1, 5, 0)
        self.assertIsInstance(result_score, (float, int))
        self.assertIsInstance(result_move, Move)


class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.player1 = HumanPlayer("Player1", "X", "red")
        self.player2 = HumanPlayer("Player2", "O", "green")

    def test_get_moves(self):
        board = Board(self.player1, self.player2)
        board.board[5][0] = self.player1.get_symbol()
        board.board[5][1] = self.player2.get_symbol()

        valid_moves = board.get_moves()
        self.assertNotIn(Move(self.player1, 1), valid_moves)

    def test_get_open_row(self):
        board = Board(self.player1, self.player2)
        board.board[5][0] = self.player1.get_symbol()
        board.board[4][0] = self.player2.get_symbol()
        open_row =board.get_open_row(0)
        self.assertEqual(open_row, 3)


class TestPlayerMethods(unittest.TestCase):
    pass


class TestMoveMethods(unittest.TestCase):
    pass

    def test_connectfour(self):
        pass


if __name__ == '__main__':
    unittest.main()