# GUI implementation for Gomoku using tkinter.

import tkinter as tk
from tkinter import messagebox
from domain.board import Board
from domain.game_state import GameState


class GomokuGUI:
    # Graphical user interface for Gomoku using tkinter.

    CELL_SIZE = 40
    BOARD_PADDING = 20
    PIECE_RADIUS = 15

    def __init__(self, game_controller):
        # Initialize GUI with GameController instance.
        self._controller = game_controller

        # Create main window
        self._root = tk.Tk()
        self._root.title("Gomoku (Five in a Row)")

        # Calculate window size
        board_size = Board.BOARD_SIZE * self.CELL_SIZE + 2 * self.BOARD_PADDING

        # Create top frame for game info
        self._info_frame = tk.Frame(self._root)
        self._info_frame.pack(pady=10)

        self._status_label = tk.Label(self._info_frame, text="", font=("Arial", 14, "bold"))
        self._status_label.pack()

        # Create canvas for board
        self._canvas = tk.Canvas(
            self._root,
            width=board_size,
            height=board_size,
            bg="wheat"
        )
        self._canvas.pack()

        # Create button frame
        self._button_frame = tk.Frame(self._root)
        self._button_frame.pack(pady=10)

        self._new_game_button = tk.Button(
            self._button_frame,
            text="New Game",
            command=self._new_game,
            font=("Arial", 12)
        )
        self._new_game_button.pack(side=tk.LEFT, padx=5)

        # Bind click event
        self._canvas.bind("<Button-1>", self._handle_click)

        # Start the game
        self._controller.start_game()
        self._draw_board()
        self._update_status()

    def run(self):
        # Run the GUI main loop.
        self._root.mainloop()

    def _draw_board(self):
        # Draw the game board and pieces.
        self._canvas.delete("all")

        # Draw grid lines
        for i in range(Board.BOARD_SIZE):
            x = self.BOARD_PADDING + i * self.CELL_SIZE
            y = self.BOARD_PADDING + i * self.CELL_SIZE

            # Vertical lines
            self._canvas.create_line(
                x, self.BOARD_PADDING,
                x, self.BOARD_PADDING + (Board.BOARD_SIZE - 1) * self.CELL_SIZE,
                fill="black", width=1
            )

            # Horizontal lines
            self._canvas.create_line(
                self.BOARD_PADDING, y,
                self.BOARD_PADDING + (Board.BOARD_SIZE - 1) * self.CELL_SIZE, y,
                fill="black", width=1
            )

        # Draw star points (decorative dots at key positions)
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for row, col in star_points:
            x = self.BOARD_PADDING + col * self.CELL_SIZE
            y = self.BOARD_PADDING + row * self.CELL_SIZE
            self._canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill="black"
            )

        # Draw pieces
        board = self._controller.board
        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                cell = board.get_cell(row, col)
                if cell != Board.EMPTY:
                    self._draw_piece(row, col, cell)

    def _draw_piece(self, row, col, symbol):
        # Draw a piece at (row, col) for given symbol.
        x = self.BOARD_PADDING + col * self.CELL_SIZE
        y = self.BOARD_PADDING + row * self.CELL_SIZE

        color = "black" if symbol == Board.PLAYER_X else "white"
        outline = "black"

        self._canvas.create_oval(
            x - self.PIECE_RADIUS, y - self.PIECE_RADIUS,
            x + self.PIECE_RADIUS, y + self.PIECE_RADIUS,
            fill=color, outline=outline, width=2
        )

    def _handle_click(self, event):
        # Handle mouse clicks on the board; convert pixels to board coords and play move.
        if self._controller.is_game_over():
            return

        # Only handle human player clicks
        if not self._controller.current_player.is_human:
            return

        # Convert pixel coordinates to board coordinates
        col = round((event.x - self.BOARD_PADDING) / self.CELL_SIZE)
        row = round((event.y - self.BOARD_PADDING) / self.CELL_SIZE)

        # Validate coordinates
        if not (0 <= row < Board.BOARD_SIZE and 0 <= col < Board.BOARD_SIZE):
            return

        # Make the move
        if self._controller.make_move(row, col):
            self._draw_board()
            self._update_status()

            # Check if game is over
            if self._controller.is_game_over():
                self._show_game_over()
            else:
                # If AI's turn, make AI move
                if not self._controller.current_player.is_human:
                    self._root.after(500, self._make_ai_move)

    def _make_ai_move(self):
        # Execute the AI's move and update display.
        if self._controller.is_game_over():
            return

        ai_move = self._controller.get_ai_move()
        if ai_move:
            row, col = ai_move
            self._controller.make_move(row, col)
            self._draw_board()
            self._update_status()

            if self._controller.is_game_over():
                self._show_game_over()

    def _update_status(self):
        # Update the status label with current player or game result.
        if self._controller.is_game_over():
            state = self._controller.state
            if state == GameState.DRAW:
                text = "Game Over - Draw!"
            else:
                winner = self._controller.get_winner()
                text = f"Game Over - {winner.name} wins!"
        else:
            current = self._controller.current_player
            symbol = "X (Black)" if current.symbol == Board.PLAYER_X else "O (White)"
            text = f"Current Player: {current.name} - {symbol}"

        self._status_label.config(text=text)

    def _show_game_over(self):
        # Show a dialog with the game outcome.
        state = self._controller.state

        if state == GameState.DRAW:
            message = "The game is a draw!"
        else:
            winner = self._controller.get_winner()
            message = f"{winner.name} wins!"

        messagebox.showinfo("Game Over", message)

    def _new_game(self):
        # Reset controller and redraw board to start a new game.
        self._controller.start_game()
        self._draw_board()
        self._update_status()

