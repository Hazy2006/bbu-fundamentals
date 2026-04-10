"""AI player for Gomoku game."""

import random
from domain.board import Board
from business.game_rules import GameRules


class AI:
    def __init__(self, board, rules, player_symbol, opponent_symbol, difficulty='medium'):
        # To initialize AI we need the board and the rules to evaluate moves
        # As arguments we have the board, the rules, the AI's symbol, the opponent's symbol and the difficulty level
        self._board = board
        self._rules = rules
        self._player_symbol = player_symbol
        self._opponent_symbol = opponent_symbol
        self._difficulty = difficulty

    def get_move(self):
        if self._difficulty == 'easy':
            return self._get_random_move()
        elif self._difficulty == 'medium':
            return self._get_strategic_move()
        else:  # hard
            return self._get_minimax_move()

    def _get_random_move(self):
        # Happens rarely, for example in cases where the board is full, no strategic movement found or simply specific patterns
        empty_cells = self._board.get_empty_cells()
        if not empty_cells:
            return None
        return random.choice(empty_cells)

    def _get_strategic_move(self):
        # "The beginning logic" of the AI's predictions and movements
        # 1. Check if AI can win
        winning_move = self._rules.find_threat(self._player_symbol)
        if winning_move:
            return winning_move

        # 2. Check if opponent can win and block it
        blocking_move = self._rules.find_threat(self._opponent_symbol)
        if blocking_move:
            return blocking_move

        # 3. Make a smart move (prefer center and near existing pieces)
        smart_move = self._get_smart_move()
        if smart_move:
            return smart_move

        # 4. Fallback to random move
        return self._get_random_move()
    
    def _get_smart_move(self):
        # Prefer center and moves near existing pieces
        center = Board.BOARD_SIZE // 2

        # If board is empty, play in center
        if self._board.is_empty(center, center):
            return (center, center)

        # Find moves near existing pieces
        candidate_moves = []
        empty_cells = self._board.get_empty_cells()

        for row, col in empty_cells:
            # Check if this cell is adjacent to any existing piece
            if self._has_adjacent_piece(row, col):
                # Prioritize based on distance to center
                distance = abs(row - center) + abs(col - center)
                candidate_moves.append((distance, row, col))

        if candidate_moves:
            # Sort by distance and return closest to center
            candidate_moves.sort()
            return (candidate_moves[0][1], candidate_moves[0][2])

        return None

    def _has_adjacent_piece(self, row, col):
        # True if there's an existing piece within 2 cells
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if (0 <= r < Board.BOARD_SIZE and
                        0 <= c < Board.BOARD_SIZE and
                        not self._board.is_empty(r, c)):
                    return True
        return False

    def _get_minimax_move(self):
        # Evaluates cases for minimax algorithm
        # First check for immediate win or block
        winning_move = self._rules.find_threat(self._player_symbol)
        if winning_move:
            return winning_move

        blocking_move = self._rules.find_threat(self._opponent_symbol)
        if blocking_move:
            return blocking_move

        # Use minimax with limited depth for performance
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Get candidate moves (cells near existing pieces)
        candidate_moves = self._get_candidate_moves()

        for row, col in candidate_moves:
            self._board.set_cell(row, col, self._player_symbol)

            # Check for immediate win
            if self._rules.check_winner(row, col, self._player_symbol):
                self._board.set_cell(row, col, Board.EMPTY)
                return (row, col)

            score = self._minimax(2, False, alpha, beta)
            self._board.set_cell(row, col, Board.EMPTY)

            if score > best_score:
                best_score = score
                best_move = (row, col)

            alpha = max(alpha, best_score)

        return best_move if best_move else self._get_strategic_move()

    def _get_candidate_moves(self):
        # Searches possible advantageous moves (cells near existing pieces)
        empty_cells = self._board.get_empty_cells()

        # If board is empty, return center
        if len(empty_cells) == Board.BOARD_SIZE * Board.BOARD_SIZE:
            center = Board.BOARD_SIZE // 2
            return [(center, center)]

        # Return cells adjacent to existing pieces
        candidates = []
        for row, col in empty_cells:
            if self._has_adjacent_piece(row, col):
                candidates.append((row, col))

        # Limit number of candidates for performance
        if len(candidates) > 15:
            # Prioritize center area
            center = Board.BOARD_SIZE // 2
            candidates.sort(key=lambda pos: abs(pos[0] - center) + abs(pos[1] - center))
            candidates = candidates[:15]

        return candidates if candidates else empty_cells[:15]

    def _minimax(self, depth, is_maximizing, alpha, beta):
        # Minimax algorithm which consists in evaluating the board recursively
        # Using some intervals (-1000,1000) to represent losing and winning states
        # Returns an evaluation score
        # Check for terminal states
        if self._board.is_full():
            return 0

        if depth == 0:
            return self._evaluate_board()

        if is_maximizing:
            max_score = float('-inf')
            candidate_moves = self._get_candidate_moves()

            for row, col in candidate_moves:
                self._board.set_cell(row, col, self._player_symbol)

                if self._rules.check_winner(row, col, self._player_symbol):
                    self._board.set_cell(row, col, Board.EMPTY)
                    return 1000

                score = self._minimax(depth - 1, False, alpha, beta)
                self._board.set_cell(row, col, Board.EMPTY)

                max_score = max(max_score, score)
                alpha = max(alpha, score)

                if beta <= alpha:
                    break

            return max_score
        else:
            min_score = float('inf')
            candidate_moves = self._get_candidate_moves()

            for row, col in candidate_moves:
                self._board.set_cell(row, col, self._opponent_symbol)

                if self._rules.check_winner(row, col, self._opponent_symbol):
                    self._board.set_cell(row, col, Board.EMPTY)
                    return -1000

                score = self._minimax(depth - 1, True, alpha, beta)
                self._board.set_cell(row, col, Board.EMPTY)

                min_score = min(min_score, score)
                beta = min(beta, score)

                if beta <= alpha:
                    break

            return min_score

    def _evaluate_board(self):
        # Evaluate position on board
        score = 0
        # Evaluate all positions
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                if not self._board.is_empty(row, col):
                    symbol = self._board.get_cell(row, col)
                    multiplier = 1 if symbol == self._player_symbol else -1
                    score += multiplier * self._evaluate_position(row, col, symbol)

        return score

    def _evaluate_position(self, row, col, symbol):
        # Evaluate a single position based on potential lines
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = self._rules.count_consecutive(row, col, dr, dc, symbol)

            # Score based on consecutive pieces
            if count >= 4:
                score += 100
            elif count == 3:
                score += 10
            elif count == 2:
                score += 2

        return score