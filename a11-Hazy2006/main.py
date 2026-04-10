# Main entry point for Gomoku game.
# Provides a menu to choose between console and GUI interfaces.

import sys
from business.game_controller import GameController
from presentation.console_ui import ConsoleUI

# Try to import GUI, but continue if not available
try:
    from presentation.gui import GomokuGUI

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    GomokuGUI = None


def print_main_menu():
    # Print the main menu.
    print("\n" + "=" * 50)
    print("GOMOKU - Five in a Row")
    print("=" * 50)
    print("\n1. Play Console Version")
    if GUI_AVAILABLE:
        print("2. Play GUI Version")
    else:
        print("2. Play GUI Version (Not available - requires tkinter)")
    print("3. Exit")
    print()


def get_game_setup():
    # Prompt user for game setup and return (player1_name, player2_name, player2_is_human, ai_difficulty)
    try:
        print("\n--- Game Setup ---")
        player1_name = input("Enter Player 1 name (default: Player X): ").strip()
        if not player1_name:
            player1_name = "Player X"

        print("\nChoose opponent:")
        print("1. Human Player")
        print("2. Computer (Easy)")
        print("3. Computer (Medium)")
        print("4. Computer (Hard)")

        while True:
            choice = input("Enter choice (1-4): ").strip()
            if choice == "1":
                player2_name = input("Enter Player 2 name (default: Player O): ").strip()
                if not player2_name:
                    player2_name = "Player O"
                return player1_name, player2_name, True, 'medium'
            elif choice == "2":
                return player1_name, "Computer (Easy)", False, 'easy'
            elif choice == "3":
                return player1_name, "Computer (Medium)", False, 'medium'
            elif choice == "4":
                return player1_name, "Computer (Hard)", False, 'hard'
            else:
                print("Invalid choice. Please enter 1-4.")
    except EOFError:
        print("\nInput ended. Using default settings.")
        return "Player X", "Computer (Medium)", False, 'medium'


def run_console():
    # Start and run the console version of the game.
    player1_name, player2_name, player2_is_human, ai_difficulty = get_game_setup()

    controller = GameController(
        player1_name=player1_name,
        player2_name=player2_name,
        player2_is_human=player2_is_human,
        ai_difficulty=ai_difficulty
    )

    console_ui = ConsoleUI(controller)
    console_ui.run()


def run_gui():
    # Start and run the GUI version of the game (if available).
    if not GUI_AVAILABLE:
        print("\nGUI is not available. Please install tkinter or use the console version.")
        return

    player1_name, player2_name, player2_is_human, ai_difficulty = get_game_setup()

    controller = GameController(
        player1_name=player1_name,
        player2_name=player2_name,
        player2_is_human=player2_is_human,
        ai_difficulty=ai_difficulty
    )

    gui = GomokuGUI(controller)
    gui.run()


def main():
    # Main program loop and menu handling.
    print("\nWelcome to Gomoku!")
    print("A strategy board game where you try to get 5 pieces in a row.")

    while True:
        try:
            print_main_menu()
            choice = input("Enter your choice (1-3): ").strip()

            if choice == "1":
                run_console()
            elif choice == "2":
                try:
                    run_gui()
                except Exception as e:
                    print(f"\nError running GUI: {e}")
                    print("GUI requires a display. Try the console version instead.")
            elif choice == "3":
                print("\nThank you for playing Gomoku!")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except EOFError:
            print("\n\nInput ended. Thank you for playing Gomoku!")
            sys.exit(0)
        except KeyboardInterrupt:
            print("\n\nInterrupted. Thank you for playing Gomoku!")
            sys.exit(0)


if __name__ == "__main__":
    main()