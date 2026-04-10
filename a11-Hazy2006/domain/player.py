"""Player entity for Gomoku game."""

class Player:
    """Represents a player in the Gomoku game."""

    def __init__(self, name, symbol, is_human=True):
        # Initialize player fields
        self._name = name
        self._symbol = symbol
        self._is_human = is_human

    @property
    def name(self):
        # Return player's name
        return self._name

    @property
    def symbol(self):
        # Return player's symbol constant
        return self._symbol

    @property
    def is_human(self):
        # True if player is human
        return self._is_human

    def __str__(self):
        # Human-readable representation
        player_type = "Human" if self._is_human else "Computer"
        return f"{self._name} ({player_type})"