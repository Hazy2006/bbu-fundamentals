# Unit tests for GameRules class.

import unittest
from domain.board import Board
from business.game_rules import GameRules


class TestGameRules(unittest.TestCase):
    # Test cases for GameRules class.

    def setUp(self):
        # Set up test fixtures.
        self.board = Board()
        self.rules = GameRules(self.board)

    def test_is_valid_move(self):
        # Test is_valid_move method.
        # Empty cell should be valid
        self.assertTrue(self.rules.is_valid_move(0, 0))

        # Occupied cell should be invalid
        self.board.set_cell(0, 0, Board.PLAYER_X)
        self.assertFalse(self.rules.is_valid_move(0, 0))

        # Out of bounds should be invalid
        self.assertFalse(self.rules.is_valid_move(-1, 0))
        self.assertFalse(self.rules.is_valid_move(15, 0))

    def test_check_winner_horizontal(self):
        # Test horizontal win detection.
        # Place 5 pieces horizontally
        for col in range(5):
            self.board.set_cell(0, col, Board.PLAYER_X)

        # Check that the last move creates a win
        self.assertTrue(self.rules.check_winner(0, 4, Board.PLAYER_X))

        # Check that a move in the middle also detects the win
        self.assertTrue(self.rules.check_winner(0, 2, Board.PLAYER_X))

    def test_check_winner_vertical(self):
        # Test vertical win detection.
        # Place 5 pieces vertically
        for row in range(5):
            self.board.set_cell(row, 0, Board.PLAYER_O)

        # Check that the last move creates a win
        self.assertTrue(self.rules.check_winner(4, 0, Board.PLAYER_O))

    def test_check_winner_diagonal(self):
        # Test diagonal win detection.
        # Place 5 pieces diagonally
        for i in range(5):
            self.board.set_cell(i, i, Board.PLAYER_X)

        # Check that the last move creates a win
        self.assertTrue(self.rules.check_winner(4, 4, Board.PLAYER_X))

    def test_check_winner_anti_diagonal(self):
        # Test anti-diagonal win detection.
        # Place 5 pieces anti-diagonally
        for i in range(5):
            self.board.set_cell(i, 4 - i, Board.PLAYER_O)

        # Check that the last move creates a win
        self.assertTrue(self.rules.check_winner(4, 0, Board.PLAYER_O))

    def test_check_winner_no_win(self):
        # Test that no win is detected when there are only 4 pieces.
        # Place 4 pieces horizontally
        for col in range(4):
            self.board.set_cell(0, col, Board.PLAYER_X)

        # Should not detect a win
        self.assertFalse(self.rules.check_winner(0, 3, Board.PLAYER_X))

    def test_find_threat_winning_move(self):
        # Test finding a winning move.
        # Place 4 pieces horizontally with a gap
        for col in [0, 1, 2, 3]:
            self.board.set_cell(0, col, Board.PLAYER_X)

        # Should find the winning move at (0, 4)
        threat = self.rules.find_threat(Board.PLAYER_X)
        self.assertIsNotNone(threat)
        self.assertEqual(threat, (0, 4))

    def test_find_threat_no_threat(self):
        # Test when there's no immediate winning move.
        # Place 3 pieces with no immediate win
        for col in [0, 1, 2]:
            self.board.set_cell(0, col, Board.PLAYER_X)

        # Place opponent pieces to block
        self.board.set_cell(0, 3, Board.PLAYER_O)
        self.board.set_cell(0, 4, Board.PLAYER_O)

        # Should not find a threat
        threat = self.rules.find_threat(Board.PLAYER_X)
        self.assertIsNone(threat)

    def test_count_consecutive(self):
        # Test counting consecutive pieces using public interface.
        # Place 3 pieces horizontally
        for col in [5, 6, 7]:
            self.board.set_cell(5, col, Board.PLAYER_X)

        # Count from middle piece using public method
        count = self.rules.count_consecutive(5, 6, 0, 1, Board.PLAYER_X)
        self.assertEqual(count, 3)

    def test_check_winner_more_than_five(self):
        # Test that 6 or more in a row is also a win.
        # Place 6 pieces horizontally
        for col in range(6):
            self.board.set_cell(0, col, Board.PLAYER_X)

        # Should still detect a win
        self.assertTrue(self.rules.check_winner(0, 5, Board.PLAYER_X))


if __name__ == '__main__':
    unittest.main()