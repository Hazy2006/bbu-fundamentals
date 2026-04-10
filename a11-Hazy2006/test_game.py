"""
Simple test to verify the game works correctly.
This creates a game and simulates some moves.
"""

from domain.board import Board
from domain.player import Player
from business.game_controller import GameController
from business.game_rules import GameRules


def test_basic_game():
    """Test basic game functionality."""
    print("Testing basic game functionality...")

    # Create a game
    controller = GameController("Player X", "Computer", False, 'medium')
    controller.start_game()

    print("Game created successfully")

    # Make some moves
    assert controller.make_move(7, 7), "Failed to make move at (7, 7)"
    print("Player X moved to (7, 7)")

    # AI should make a move
    ai_move = controller.get_ai_move()
    if ai_move:
        row, col = ai_move
        assert controller.make_move(row, col), f"AI failed to make move at ({row}, {col})"
        print(f"AI moved to ({row}, {col})")

    print("Game is functioning correctly")


def test_win_detection():
    """Test win detection."""
    print("\nTesting win detection...")

    board = Board()
    rules = GameRules(board)

    # Test horizontal win
    for col in range(5):
        board.set_cell(0, col, Board.PLAYER_X)

    assert rules.check_winner(0, 4, Board.PLAYER_X), "Horizontal win not detected"
    print("Horizontal win detected")

    # Reset and test vertical win
    board.clear()
    for row in range(5):
        board.set_cell(row, 0, Board.PLAYER_O)

    assert rules.check_winner(4, 0, Board.PLAYER_O), "Vertical win not detected"
    print("Vertical win detected")

    # Reset and test diagonal win
    board.clear()
    for i in range(5):
        board.set_cell(i, i, Board.PLAYER_X)

    assert rules.check_winner(4, 4, Board.PLAYER_X), "Diagonal win not detected"
    print("Diagonal win detected")


def test_ai_blocking():
    """Test AI blocking behavior."""
    print("\nTesting AI blocking...")

    controller = GameController("Player X", "Computer", False, 'medium')
    controller.start_game()

    # Create a scenario where player X is about to win
    for col in range(4):
        controller.board.set_cell(0, col, Board.PLAYER_X)

    # Switch to AI's turn
    controller._current_player = controller.player2

    # AI should block at (0, 4)
    ai_move = controller.get_ai_move()
    assert ai_move == (0, 4), f"AI should block at (0, 4), but chose {ai_move}"
    print("AI correctly blocks opponent's winning move")


def test_ai_winning():
    """Test AI winning behavior."""
    print("\nTesting AI winning move...")

    controller = GameController("Player X", "Computer", False, 'medium')
    controller.start_game()

    # Create a scenario where AI can win
    for col in range(4):
        controller.board.set_cell(1, col, Board.PLAYER_O)

    # Switch to AI's turn
    controller._current_player = controller.player2

    # AI should win at (1, 4)
    ai_move = controller.get_ai_move()
    assert ai_move == (1, 4), f"AI should win at (1, 4), but chose {ai_move}"
    print("AI correctly takes winning move")


def test_input_validation():
    """Test input validation."""
    print("\nTesting input validation...")

    board = Board()

    # Test invalid positions
    try:
        board.get_cell(-1, 0)
        assert False, "Should raise ValueError for negative row"
    except ValueError:
        print("Rejects negative row")

    try:
        board.get_cell(0, 15)
        assert False, "Should raise ValueError for column out of bounds"
    except ValueError:
        print("Rejects column out of bounds")

    # Test invalid values
    try:
        board.set_cell(0, 0, 999)
        assert False, "Should raise ValueError for invalid value"
    except ValueError:
        print("Rejects invalid cell value")


if __name__ == "__main__":
    print("=" * 50)
    print("Running Gomoku Tests")
    print("=" * 50)

    try:
        test_basic_game()
        test_win_detection()
        test_ai_blocking()
        test_ai_winning()
        test_input_validation()

        print("\n" + "=" * 50)
        print("All tests passed!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\nTest failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        exit(1)