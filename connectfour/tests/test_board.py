import unittest
from connectfour.game.board import GameBoard


class TestGameBoard(unittest.TestCase):
    def test_board_state(self):
        board = GameBoard()
        self.assertEqual(board.board, [[' '] * 7 for _ in range(6)])

    def test_valid_move(self):
        board = GameBoard()
        self.assertTrue(board.check_valid_move(6))  # valid move in column
        self.assertTrue(board.check_valid_move(3))  # valid move -||-
        self.assertFalse(board.check_valid_move(1))  # invalid move -||- !!tää epäonnistuu!!
        self.assertFalse(board.check_valid_move(8))  # invalid move -||-

    def test_make_move(self):
        board = GameBoard()
        self.assertTrue(board.make_move(5, 'X'))  # make move
        self.assertEqual(board.board[5][4], 'X')  # check after the move
        self.assertTrue(board.make_move(5, 'O'))
        self.assertEqual(board.board[4][4], 'O')

    def test_winner_check(self):
        board = GameBoard()
        board.board = [
            ['X', ' ', ' ', ' ', ' ', ' ', ' '],
            ['X', 'O', ' ', ' ', ' ', ' ', ' '],
            ['X', 'O', 'O', ' ', ' ', ' ', ' '],
            ['X', 'O', 'X', ' ', ' ', ' ', ' '],
            ['O', 'X', 'O', ' ', ' ', ' ', ' '],
            ['O', 'X', 'X', ' ', ' ', ' ', ' '],
        ]
        self.assertTrue(board.winner_check('X'))
        self.assertFalse(board.winner_check('O'))
