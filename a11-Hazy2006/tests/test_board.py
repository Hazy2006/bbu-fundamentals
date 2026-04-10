# Unit tests for Board class.

import unittest
from domain.board import Board


class TestBoard(unittest.TestCase):
    # Test cases for Board class.

    def setUp(self):
        # Set up test fixtures.
        self.board = Board()

    def test_board_initialization(self):
        # Ensure board initializes correctly.
        self.assertEqual(self.board.BOARD_SIZE, 15)

        # Check that all cells are empty
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                self.assertEqual(self.board.get_cell(row, col), Board.EMPTY)

    def test_set_and_get_cell(self):
        # Test setting and getting cell values.
        self.board.set_cell(0, 0, Board.PLAYER_X)
        self.assertEqual(self.board.get_cell(0, 0), Board.PLAYER_X)

        self.board.set_cell(7, 7, Board.PLAYER_O)
        self.assertEqual(self.board.get_cell(7, 7), Board.PLAYER_O)

    def test_invalid_position(self):
        # Test that invalid positions raise ValueError.
        with self.assertRaises(ValueError):
            self.board.get_cell(-1, 0)

        with self.assertRaises(ValueError):
            self.board.get_cell(0, 15)

        with self.assertRaises(ValueError):
            self.board.set_cell(15, 0, Board.PLAYER_X)

    def test_invalid_value(self):
        # Test that invalid values raise ValueError.
        with self.assertRaises(ValueError):
            self.board.set_cell(0, 0, 5)

    def test_is_empty(self):
        # Test is_empty method.
        self.assertTrue(self.board.is_empty(0, 0))

        self.board.set_cell(0, 0, Board.PLAYER_X)
        self.assertFalse(self.board.is_empty(0, 0))

    def test_is_full(self):
        # Test is_full method.
        self.assertFalse(self.board.is_full())

        # Fill the board
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                self.board.set_cell(row, col, Board.PLAYER_X)

        self.assertTrue(self.board.is_full())

    def test_get_empty_cells(self):
        # Test get_empty_cells method.
        empty_cells = self.board.get_empty_cells()
        self.assertEqual(len(empty_cells), Board.BOARD_SIZE * Board.BOARD_SIZE)

        self.board.set_cell(0, 0, Board.PLAYER_X)
        empty_cells = self.board.get_empty_cells()
        self.assertEqual(len(empty_cells), Board.BOARD_SIZE * Board.BOARD_SIZE - 1)
        self.assertNotIn((0, 0), empty_cells)

    def test_clear(self):
        # Test clear method.
        self.board.set_cell(0, 0, Board.PLAYER_X)
        self.board.set_cell(1, 1, Board.PLAYER_O)

        self.board.clear()

        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                self.assertEqual(self.board.get_cell(row, col), Board.EMPTY)

    def test_get_grid(self):
        # Test get_grid returns a copy.
        grid = self.board.get_grid()

        # Modify the copy
        grid[0][0] = Board.PLAYER_X

        # Original should be unchanged
        self.assertEqual(self.board.get_cell(0, 0), Board.EMPTY)


if __name__ == '__main__':
    unittest.main()