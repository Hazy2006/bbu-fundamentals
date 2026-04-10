# Console UI for Gomoku game.

from domain.board import Board
from domain.game_state import GameState


class ConsoleUI:
    # Console-based user interface for Gomoku.

    def __init__(self, game_controller):
        self._controller = game_controller
        
    def run(self):
        self.display_welcome()

        while True:
            self._controller.start_game()
            self.display_board()

            while not self._controller.is_game_over():
                current_player = self._controller.current_player

                if current_player.is_human:
                    self._handle_human_turn()
                else:
                    self._handle_ai_turn()

                self.display_board()

            self.display_game_over()

            if not self._ask_play_again():
                break

        print("\nThanks for playing Gomoku!")

    def display_welcome(self):
        # Print welcome and rules to the console.
        print("=" * 50)
        print("Welcome to Gomoku (Five in a Row)!")
        print("=" * 50)
        print("\nRules:")
        print("- The board is 15x15")
        print("- Players take turns placing pieces")
        print("- First to get 5 in a row (horizontally, vertically, or diagonally) wins")
        print("- Enter moves as row and column (e.g., '7 7' for center)")
        print("- Coordinates range from 0 to 14")
        print()

    def display_board(self):
        # Print the current board state.
        board = self._controller.board
        print("\n   ", end="")

        # Column headers
        for col in range(Board.BOARD_SIZE):
            print(f"{col:2}", end=" ")
        print()

        # Board rows
        for row in range(Board.BOARD_SIZE):
            print(f"{row:2} ", end="")

            for col in range(Board.BOARD_SIZE):
                cell = board.get_cell(row, col)
                if cell == Board.EMPTY:
                    symbol = "."
                elif cell == Board.PLAYER_X:
                    symbol = "X"
                else:  # PLAYER_O
                    symbol = "O"

                print(f" {symbol} ", end="")

            print(f" {row:2}")

        print("   ", end="")
        for col in range(Board.BOARD_SIZE):
            print(f"{col:2}", end=" ")
        print("\n")

    def _handle_human_turn(self):
        # Handle input and play a human player's turn.
        current_player = self._controller.current_player
        print(f"\n{current_player.name}'s turn (Symbol: {'X' if current_player.symbol == Board.PLAYER_X else 'O'})")

        while True:
            try:
                move_input = input("Enter your move (row col): ").strip()

                if not move_input:
                    print("Please enter a valid move.")
                    continue

                parts = move_input.split()
                if len(parts) != 2:
                    print("Please enter two numbers separated by space (e.g., '7 7').")
                    continue

                row = int(parts[0])
                col = int(parts[1])

                if self._controller.make_move(row, col):
                    break
                else:
                    print(f"Invalid move! Cell ({row}, {col}) is occupied or out of bounds.")
                    print("Please try again.")

            except EOFError:
                print("\nInput ended. Exiting game.")
                import sys
                sys.exit(0)
            except ValueError as e:
                print(f"Invalid input! Please enter numbers only.")
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again.")

    def _handle_ai_turn(self):
        # Request and apply AI move.
        current_player = self._controller.current_player
        print(f"\n{current_player.name}'s turn (Symbol: {'X' if current_player.symbol == Board.PLAYER_X else 'O'})")
        print("Computer is thinking...")

        ai_move = self._controller.get_ai_move()
        if ai_move:
            row, col = ai_move
            self._controller.make_move(row, col)
            print(f"Computer placed at ({row}, {col})")

    def display_game_over(self):
        # Print the game over banner and result.
        print("\n" + "=" * 50)
        print("GAME OVER!")
        print("=" * 50)

        state = self._controller.state

        if state == GameState.DRAW:
            print("The game is a draw!")
        else:
            winner = self._controller.get_winner()
            print(f"{winner.name} wins!")

        print("=" * 50)

    def _ask_play_again(self):
        # Ask players if they want to play again; return True/False.
        while True:
            try:
                response = input("\nPlay again? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                else:
                    print("Please enter 'y' or 'n'.")
            except EOFError:
                return False
