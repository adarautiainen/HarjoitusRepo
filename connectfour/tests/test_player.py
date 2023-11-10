import unittest
from connectfour.game.player import Player
from connectfour.game.board import GameBoard


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('X')
        self.board = GameBoard()

    # def test_make_move(self):
    # print("Before move:")
    # self.board.display_board()
    #  self.assertTrue(self.player.make_move(1, self.board))
    #  print("After move:")
    #  self.assertEqual(self.board.board[5][0], 'X')
    # self.assertFalse(self.player.make_move(1, self.board)) # testing invalid move (column filled)
    # self.assertFalse(self.player.make_move((8, self.board))) # testing invalid move (invalid column)
