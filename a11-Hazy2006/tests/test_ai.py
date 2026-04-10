# Unit tests for AI class.

import unittest
from domain.board import Board
from business.game_rules import GameRules
from business.ai import AI


class TestAI(unittest.TestCase):
    # Test cases for AI class.

    def setUp(self):
        # Set up test fixtures.
        self.board = Board()
        self.rules = GameRules(self.board)
        self.ai = AI(self.board, self.rules, Board.PLAYER_O, Board.PLAYER_X, 'medium')

    def test_ai_wins_when_possible(self):
        # AI should take a winning move when available.
        # Set up a scenario where AI can win
        for col in [0, 1, 2, 3]:
            self.board.set_cell(0, col, Board.PLAYER_O)

        # AI should choose (0, 4) to win
        move = self.ai.get_move()
        self.assertEqual(move, (0, 4))

    def test_ai_blocks_opponent_win(self):
        # AI should block opponent's winning move.
        # Set up a scenario where opponent can win
        for col in [0, 1, 2, 3]:
            self.board.set_cell(0, col, Board.PLAYER_X)

        # AI should block at (0, 4)
        move = self.ai.get_move()
        self.assertEqual(move, (0, 4))

    def test_ai_prioritizes_win_over_block(self):
        # AI prioritizes winning over blocking.
        # Set up where both AI and opponent can win
        # AI can win horizontally
        for col in [0, 1, 2, 3]:
            self.board.set_cell(5, col, Board.PLAYER_O)

        # Opponent can win vertically
        for row in [0, 1, 2, 3]:
            self.board.set_cell(row, 10, Board.PLAYER_X)

        # AI should prioritize winning
        move = self.ai.get_move()
        self.assertEqual(move, (5, 4))

    def test_ai_random_move(self):
        # AI returns a valid random move on easy difficulty.
        ai_easy = AI(self.board, self.rules, Board.PLAYER_O, Board.PLAYER_X, 'easy')

        # Get a random move
        move = ai_easy.get_move()

        # Should return a valid empty cell
        self.assertIsNotNone(move)
        row, col = move
        self.assertTrue(0 <= row < Board.BOARD_SIZE)
        self.assertTrue(0 <= col < Board.BOARD_SIZE)
        self.assertTrue(self.board.is_empty(row, col))

    def test_ai_center_preference(self):
        # AI prefers center on empty board.
        ai = AI(self.board, self.rules, Board.PLAYER_O, Board.PLAYER_X, 'medium')

        # On empty board, AI should prefer center
        move = ai.get_move()
        center = Board.BOARD_SIZE // 2
        self.assertEqual(move, (center, center))

    def test_ai_adjacent_preference(self):
        # AI prefers moves adjacent to existing pieces.
        # Place a piece in the center
        center = Board.BOARD_SIZE // 2
        self.board.set_cell(center, center, Board.PLAYER_X)

        # AI should make a move adjacent to the existing piece
        move = self.ai.get_move()
        self.assertIsNotNone(move)

        row, col = move
        # Check if move is within 2 cells of the center piece
        distance = max(abs(row - center), abs(col - center))
        self.assertLessEqual(distance, 2)


if __name__ == '__main__':
    unittest.main()