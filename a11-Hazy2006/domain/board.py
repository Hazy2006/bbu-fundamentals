"""Board entity for Gomoku game."""


class Board:
    """Represent a standard size Gomoku board (15x15)."""

    # Variables to represent the board size and the players
    # While the size is an obvious choice, the other variables are represented as keys
    BOARD_SIZE = 15
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self):
        # Initialize an empty board grid
        self._grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]

    def get_cell(self, row, col):
        # Return value at specified cell; raise for invalid position
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._grid[row][col]

    def set_cell(self, row, col, value):
        # Set cell value after validating position and value
        if not self._is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        if value not in [self.EMPTY, self.PLAYER_X, self.PLAYER_O]:
            raise ValueError(f"Invalid value: {value}")
        self._grid[row][col] = value

    def is_empty(self, row, col):
        # True if the given cell is empty
        return self.get_cell(row, col) == self.EMPTY

    def is_full(self):
        # True if no empty cells remain
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.is_empty(row, col):
                    return False
        return True

    def get_empty_cells(self):
        # Return list of all empty (row, col) tuples
        empty_cells = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.is_empty(row, col):
                    empty_cells.append((row, col))
        return empty_cells

    def clear(self):
        # Reset board to empty state
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                self._grid[row][col] = self.EMPTY

    def _is_valid_position(self, row, col):
        # Check if coordinates are on the board
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def get_grid(self):
        # Return a copy of the grid
        return [row[:] for row in self._grid]
