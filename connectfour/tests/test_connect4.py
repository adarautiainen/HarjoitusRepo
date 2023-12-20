import math
import unittest
from unittest.mock import patch
from connectfour.game.connect4 import (
    initialize_board, minimax_with_alphabeta, check_winner, game_over,
    is_valid_drop, get_next_open_row, drop_piece, get_valid_locations,
    evaluate_window, evaluate, play_game, print_board)


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
            [self.empty_piece, self.empty_piece, self.player_piece, self.empty_piece, self.empty_piece,
             self.empty_piece,
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
            [self.empty_piece, self.empty_piece, self.empty_piece, self.empty_piece, self.player_piece,
             self.empty_piece,
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
        board = initialize_board()
        depth = 5
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board, depth, alpha, beta, maximizing_player)

        self.assertIsNotNone(col)
        self.assertIsInstance(value, int)
        self.assertTrue(alpha <= value <= beta)

    def test_minimax_with_alphabeta_winning(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            ["O", " ", " ", " ", " ", " ", " "],
            ["O", " ", " ", " ", " ", " ", " "],
            ["O", " ", " ", " ", " ", " ", " "]
        ]
        depth = 5
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta, maximizing_player)

        self.assertEqual(col, 0)  # maximizing player should choose column 0 to win
        self.assertEqual(value, 9999999)  # value of winning move

        board_min = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "],
            ["X", " ", " ", " ", " ", " ", " "]
        ]
        maximizing_player = False
        col_min, value_min = minimax_with_alphabeta(board_min, depth, alpha, beta, maximizing_player)

        self.assertEqual(col_min, 0)
        self.assertEqual(value_min, -9999999)

    def test_minimax_with_alphabeta_blocking(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            ["X", "X", "X", " ", " ", " ", " "]
        ]
        depth = 5
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 3)
        self.assertNotEqual(value, 9999999)

        board_min = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            ["O", "O", "O", " ", " ", " ", " "]
        ]
        maximizing_player = False
        col_min, value_min = minimax_with_alphabeta(board_min, depth, alpha, beta,
                                                    maximizing_player)

        self.assertEqual(col_min, 3)
        self.assertNotEqual(value_min, -9999999)

    def test_minimax_with_alphabeta_draw(self):
        board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"]
        ]
        depth = 5
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board, depth, alpha, beta, maximizing_player)
        self.assertIsNone(col)
        self.assertEqual(value, 0)

    def test_minimax_with_alphabeta_depth(self):
        board = [
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["O", "X", "O", "X", "O", "X", "O"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["X", "O", "X", "O", "X", "O", "X"],
            ["O", "X", "O", "X", "O", "X", "O"]
        ]
        depth = 0
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board, depth, alpha, beta,
                                            maximizing_player)
        #expected = evaluate(board, self.computer_piece)

        self.assertIsNone(col)
        self.assertEqual(value, 0)

    def test_minimax_with_alphabeta_2(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", "X", " ", "O", " ", " ", " "],
            [" ", "X", " ", "O", " ", " ", " "],
            [" ", "X", " ", "O", " ", " ", " "]
        ]
        depth = 7
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 3)
        self.assertEqual(value, 9999999)

    def test_minimax_with_alphabeta_3(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "X", "X", "O", " ", " "],
            ["O", "X", "X", "O", "O", "O", "X"]
        ]
        depth = 7
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 4)

    def test_minimax_with_alphabeta_4(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "X", "X", " ", " ", " "],
            ["O", "X", "X", "O", "O", "O", " "]
        ]
        depth = 7
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 6)

    def test_minimax_with_alphabeta_5(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "X", " ", " ", " "],
            ["X", " ", " ", "O", "X", " ", " "],
            ["X", "X", " ", "O", "O", "O", " "]
        ]
        depth = 7
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 0)

    def test_minimax_with_alphabeta_6(self):
        board_max = [
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "X", " ", " ", " "],
            [" ", " ", " ", "O", "X", " ", " "],
            ["X", "X", "X", "O", "O", "O", " "]
        ]
        depth = 7
        alpha = -math.inf
        beta = math.inf
        maximizing_player = True
        col, value = minimax_with_alphabeta(board_max, depth, alpha, beta,
                                            maximizing_player)
        self.assertEqual(col, 6)

    def test_evaluate_window_three_in_a_row(self):
        window = ["O", "O", "O", " "]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 100)

    def test_evaluate_window_two_in_a_row(self):
        window = [" ", "O", " ", "O"]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 50)

    def test_evaluate_window_two_in_a_row_next(self):
        window = ["O", "O", " ", " "]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 50)

    def test_evaluate_window_two_in_a_row_empty_either_side(self):
        window = ["O", " ", " ", "O"]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, 50)

    def test_evaluate_window_opponent_three_in_a_row(self):
        window = ["X", "X", "X", " "]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, -100)

    def test_evaluate_window_opponent_two_in_a_row(self):
        window = ["X", "X", " ", " "]
        piece = "O"
        score = evaluate_window(window, piece)
        self.assertEqual(score, -30)

    def test_play_game(self):
        with patch('builtins.input', return_value="3"):
            col = play_game()
            self.assertEqual(col, 2) # function returns col - 1

    def test_play_game_invalid(self):
        with patch('builtins.input', side_effect=["invalid input", "4"]):
            col = play_game()
            self.assertEqual(col, 3)


if __name__ == '__main__':
    unittest.main()
