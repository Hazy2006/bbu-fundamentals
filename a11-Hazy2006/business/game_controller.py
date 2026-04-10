"""Game controller - Manages game flow and coordinates layers."""

from domain.board import Board
from domain.player import Player
from domain.game_state import GameState
from business.game_rules import GameRules
from business.ai import AI


class GameController:
    """Controls the game flow and coordinates between layers."""

    def __init__(self, player1_name="Player X", player2_name="Player O",
                 player2_is_human=False, ai_difficulty='medium'):
        # Initialize controller, board, rules, players and optional AI
        self._board = Board()
        self._rules = GameRules(self._board)

        self._player1 = Player(player1_name, Board.PLAYER_X, True)
        self._player2 = Player(player2_name, Board.PLAYER_O, player2_is_human)

        self._current_player = self._player1
        self._state = GameState.NOT_STARTED

        # Initialize AI if player 2 is computer
        self._ai = None
        if not player2_is_human:
            self._ai = AI(self._board, self._rules,
                          Board.PLAYER_O, Board.PLAYER_X, ai_difficulty)

    def start_game(self):
        # Start a new game: clear board and set initial state/player
        self._board.clear()
        self._current_player = self._player1
        self._state = GameState.IN_PROGRESS

    def make_move(self, row, col):
        # Attempt to place a piece for the current player
        if self._state != GameState.IN_PROGRESS:
            return False

        if not self._rules.is_valid_move(row, col):
            return False

        # Place the piece
        self._board.set_cell(row, col, self._current_player.symbol)

        # Check for winner
        if self._rules.check_winner(row, col, self._current_player.symbol):
            if self._current_player.symbol == Board.PLAYER_X:
                self._state = GameState.PLAYER_X_WON
            else:
                self._state = GameState.PLAYER_O_WON
            return True

        # Check for draw
        if self._board.is_full():
            self._state = GameState.DRAW
            return True

        # Switch player
        self._switch_player()

        return True

    def get_ai_move(self):
        # Return AI move if it's the AI's turn, else None
        if self._ai is None or self._current_player.is_human:
            return None

        return self._ai.get_move()

    def _switch_player(self):
        # Toggle current player
        if self._current_player == self._player1:
            self._current_player = self._player2
        else:
            self._current_player = self._player1

    @property
    def board(self):
        # Expose the game board
        return self._board

    @property
    def current_player(self):
        # Expose current player
        return self._current_player

    @property
    def state(self):
        # Expose game state
        return self._state

    @property
    def player1(self):
        # Expose player1
        return self._player1

    @property
    def player2(self):
        # Expose player2
        return self._player2

    def is_game_over(self):
        # True if game reached a terminal state
        return self._state in [GameState.PLAYER_X_WON,
                               GameState.PLAYER_O_WON,
                               GameState.DRAW]

    def get_winner(self):
        # Return winner player or None
        if self._state == GameState.PLAYER_X_WON:
            return self._player1
        elif self._state == GameState.PLAYER_O_WON:
            return self._player2
        return None