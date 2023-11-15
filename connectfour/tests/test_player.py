import unittest
from unittest.mock import patch
from game.player import Player
from game.board import GameBoard


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('X')
        self.board = GameBoard()

    @patch('builtins.input', return_value='3')
    def test_user_input(self, mock_input):
        user_input = self.player.user_input(self.board)
        self.assertEqual(user_input, 3)

    @patch('random.choice', return_value=4)
    def test_ai_move(self, choice):
        ai_move = self.player.ai_move(self.board)
        self.assertEqual(ai_move, 4)

    @patch('builtins.input', return_value='2')
    def test_make_move(self, mock_input):
        column = int(mock_input.return_value)
        move = self.player.make_move(column, self.board)
        self.assertTrue(move)
        self.assertEqual(self.board.board[5][1], 'X')

    @patch('random.choice', return_value=3)
    def test_make_ai_move(self, mock_choice):
        self.player.is_ai = True
        move = self.player.make_ai_move(self.board)
        self.assertEqual(move, 3)


if __name__ == '__main__':
    unittest.main()

