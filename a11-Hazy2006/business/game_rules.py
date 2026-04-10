"""Game rules and validation for Gomoku."""

from domain.board import Board


class GameRules:
    """Contains game rules and validation logic."""

    WIN_LENGTH = 5  # Number of consecutive pieces needed to win

    def __init__(self, board):
        # Store board reference
        self._board = board

    def is_valid_move(self, row, col):
        # Return True if move is inside board and cell is empty
        try:
            return self._board.is_empty(row, col)
        except ValueError:
            return False

    def check_winner(self, last_row, last_col, player_symbol):
        # Check four directions for a winning run
        directions = [
            (0, 1),  # Horizontal
            (1, 0),  # Vertical
            (1, 1),  # Diagonal
            (1, -1)  # Anti-diagonal
        ]

        for dr, dc in directions:
            if self._count_consecutive(last_row, last_col, dr, dc, player_symbol) >= self.WIN_LENGTH:
                return True

        return False

    def _count_consecutive(self, row, col, dr, dc, symbol):
        # Count consecutive pieces including the starting cell
        count = 1  # Count the piece at (row, col)

        # Count in positive direction
        count += self._count_in_direction(row, col, dr, dc, symbol)

        # Count in negative direction
        count += self._count_in_direction(row, col, -dr, -dc, symbol)

        return count

    def _count_in_direction(self, row, col, dr, dc, symbol):
        # Count consecutive pieces in one direction (excluding start)
        count = 0
        r, c = row + dr, col + dc

        while (0 <= r < Board.BOARD_SIZE and
               0 <= c < Board.BOARD_SIZE and
               self._board.get_cell(r, c) == symbol):
            count += 1
            r += dr
            c += dc

        return count

    def find_threat(self, player_symbol):
        # Find a move that would immediately win for player_symbol
        empty_cells = self._board.get_empty_cells()

        for row, col in empty_cells:
            # Temporarily place the piece
            self._board.set_cell(row, col, player_symbol)

            # Check if this creates a win
            if self.check_winner(row, col, player_symbol):
                self._board.set_cell(row, col, Board.EMPTY)
                return (row, col)

            # Restore the cell
            self._board.set_cell(row, col, Board.EMPTY)

        return None

    def count_consecutive(self, row, col, dr, dc, symbol):
        # Public wrapper to count consecutive pieces including start
        return self._count_consecutive(row, col, dr, dc, symbol)