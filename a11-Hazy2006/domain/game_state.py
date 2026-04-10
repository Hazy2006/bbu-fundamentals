"""Game state entity for Gomoku game."""

from enum import Enum

# Simple enum of possible game states
class GameState(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    PLAYER_X_WON = 2
    PLAYER_O_WON = 3
    DRAW = 4