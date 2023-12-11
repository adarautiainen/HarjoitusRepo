import math
import unittest
from connectfour.game import connect4
from connectfour.game.connect4 import (
    initialize_board, minimax_with_alphabeta, check_winner, game_over,
    is_valid_drop, get_next_open_row, drop_piece, get_valid_locations,
    evaluate_window, evaluate)


class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.empty_piece = " "
        self.player_piece = "X"
        self.computer_piece = "O"
        self.rows = 6
        self.columns = 7

    def test_initialize_board(self):
        board = initialize_board()
        self.assertEqual(len(board), self.rows)
        self.assertEqual(len(board[0]), self.columns)
        # check that board is empty
        for row in board:
            self.assertTrue(all(cell == self.empty_piece for cell in row))

    def test_is_valid_drop_non_empty(self):
        board = [
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
        ]
        self.assertFalse(is_valid_drop(board, 0))

    def test_is_valid_drop_empty(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
        ]
        self.assertTrue(is_valid_drop(board, 0))

    def test_check_winner_horizontal(self):
        board = [
            [self.player_piece, self.player_piece, self.player_piece, self.player_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
        ]

        self.assertTrue(check_winner(board, self.player_piece))

    def test_check_winner_vertical(self):
        board = [
            [self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
        ]

        self.assertTrue(check_winner(board, self.player_piece))

    def test_check_winner_diagonal_positive(self):
        board = [
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.player_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.player_piece, self.empty_piece],
        ]

        self.assertTrue(check_winner(board, self.player_piece))

    def test_check_winner_diagonal_negative(self):
        board = [
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece,
             self.empty_piece],
            [self.empty_piece, self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
            [self.empty_piece, self.player_piece, self.empty_piece, self.empty_piece, self.empty_piece,
             self.empty_piece, self.empty_piece],
        ]

        self.assertTrue(check_winner(board, self.player_piece))

    def test_game_over_full_board(self):
        board = [
            ["O", "X", "O", "X", "O", "X", "O"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
        ]
        self.assertTrue(game_over(board, self.player_piece, self.computer_piece))

    def test_game_not_over(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "X", " ", " ", " "],
            [" ", " ", " ", "O", " ", " ", " "],
        ]
        self.assertFalse(game_over(board, self.player_piece, self.computer_piece))

    def test_valid_drop_non_empty_column(self):
        board = [
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
        ]
        self.assertTrue(is_valid_drop(board, 1))

    def test_next_open_row_empty(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ]
        self.assertEqual(get_next_open_row(board, 0), 5)

    def test_valid_drop(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ]
        drop_piece(board, 0, self.player_piece)
        self.assertEqual(board[5][0], self.player_piece)

    def test_invalid_drop(self):
        board = [
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
        ]
        with self.assertRaises(SystemExit):
            drop_piece(board, 0, self.player_piece)

    def test_valid_locations(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ]
        valid_locations = get_valid_locations(board)
        expected_valid_locations = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(valid_locations, expected_valid_locations)

    def test_no_valid_locations(self):
        board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
        ]
        valid_locations = get_valid_locations(board)
        expected_valid_locations = []
        self.assertEqual(valid_locations, expected_valid_locations)

    def test_minimax_with_alphabeta(self):
        board = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
        ]
        depth = 5
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True

        col, value = minimax_with_alphabeta(board, depth, alpha, beta, maximizing_player)

        self.assertIsNotNone(col)
        self.assertIsInstance(value, int)
        self.assertTrue(alpha <= value <= beta)

    def test_evaluate_window_four_in_a_row(self):
        window = ["X", "X", "X", "X"]
        piece = "X"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 100)

    def test_evaluate_window_three_in_a_row(self):
        window = ["X", "X", "X", " "]
        piece = "X"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 10)

    """
    def test_evaluate_window_two_in_a_row(self):
        window = ["X", "X", " ", " "]
        piece = "X"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 5)
    """

    def test_evaluate_window_opponent_three_in_a_row(self):
        window = ["O", "O", "O", " "]
        piece = "X"
        score = evaluate_window(window, piece)
        self.assertEqual(score, -8)

    def test_evaluate_window_opponent_two_in_a_row(self):
        window = ["O", "O", " ", " "]
        piece = "X"
        score = evaluate_window(window, piece)
        self.assertEqual(score, -4)


if __name__ == '__main__':
    unittest.main()
