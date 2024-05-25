import tkinter as tk  # Import the tkinter module for creating GUI applications
import random  # Import the random module for making random choices
from tkinter import messagebox, simpledialog  # Import messagebox and simpledialog from tkinter for displaying messages and getting input

class TicTacToe:
    def __init__(self):  # Initialize the TicTacToe class
        self.root = tk.Tk()  # Create the main window
        self.root.title("Tic-Tac-Toe")  # Set the title of the window
        self.current_player = "X"  # Set the starting player to "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]  # Initialize a 3x3 board
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Initialize a 3x3 array for buttons
        self.player_wins = 0  # Initialize player win count
        self.computer_wins = 0  # Initialize computer win count

        # Ask for the player's name
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:")  # Get the player's name

        # Label to display player's name
        self.name_label = tk.Label(self.root, text=f"Player: {self.player_name}", font=("Arial", 14))
        self.name_label.grid(row=3, column=0, columnspan=3)  # Place the label in the grid

        # Variable to store the difficulty level
        self.difficulty = tk.StringVar(value="easy")

        # Radio buttons to select difficulty level
        self.easy_radio = tk.Radiobutton(self.root, text="Easy", variable=self.difficulty, value="easy", font=("Arial", 12))
        self.medium_radio = tk.Radiobutton(self.root, text="Medium", variable=self.difficulty, value="medium", font=("Arial", 12))
        self.hard_radio = tk.Radiobutton(self.root, text="Hard", variable=self.difficulty, value="hard", font=("Arial", 12))

        # Place the radio buttons in the grid
        self.easy_radio.grid(row=4, column=0)
        self.medium_radio.grid(row=4, column=1)
        self.hard_radio.grid(row=4, column=2)

        # Labels to display the win counts
        self.player_win_label = tk.Label(self.root, text=f"{self.player_name} Wins: {self.player_wins}", font=("Arial", 12))
        self.computer_win_label = tk.Label(self.root, text=f"Witty Wins: {self.computer_wins}", font=("Arial", 12))

        # Place the win count labels in the grid
        self.player_win_label.grid(row=5, column=0, columnspan=2)
        self.computer_win_label.grid(row=5, column=1, columnspan=2)

        # Create buttons for each cell in the board and add them to the window
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text="", font=("Arial", 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.make_move(row, col))  # Set the button's command
                self.buttons[i][j].grid(row=i, column=j)  # Place the button in the grid

    def make_move(self, row, col):  # Handle a player's move
        if self.board[row][col] == "":  # Check if the cell is empty
            self.board[row][col] = self.current_player  # Update the board
            self.buttons[row][col].config(text=self.current_player)  # Update the button text
            if self.check_winner(row, col):  # Check if the current player has won
                messagebox.showinfo("Winner!", f"{self.player_name} wins!" if self.current_player == "X" else "Witty wins!")  # Show a message box if there is a winner
                if self.current_player == "X" or self.current_player == self.player_name:
                    self.player_wins += 1  # Increment player win count
                else:
                    self.computer_wins += 1  # Increment computer win count
                self.update_win_labels()  # Update win count labels
                self.reset_game()  # Reset the game
            elif self.check_draw():  # Check if the game is a draw
                messagebox.showinfo("Draw!", "It's a draw!")  # Show a message box if it's a draw
                self.reset_game()  # Reset the game
            else:
                self.current_player = "O" if self.current_player == "X" else "X"  # Switch the player
                if self.current_player == "O":  # If it's the computer's turn
                    self.computer_move()  # Make a computer move

    def computer_move(self):  # Make a move for the computer
        difficulty = self.difficulty.get()
        if difficulty == "easy":
            self.easy_move()
        elif difficulty == "medium":
            self.medium_move()
        elif difficulty == "hard":
            self.hard_move()

        if self.check_winner(self.last_move_row, self.last_move_col):  # Check if the computer has won
            messagebox.showinfo("Winner!", "Witty wins!")  # Show a message box if the computer wins
            self.computer_wins += 1  # Increment computer win count
            self.update_win_labels()  # Update win count labels
            self.reset_game()  # Reset the game
        elif self.check_draw():  # Check if the game is a draw
            messagebox.showinfo("Draw!", "It's a draw!")  # Show a message box if it's a draw
            self.reset_game()  # Reset the game
        else:
            self.current_player = "X"  # Switch back to the player

    def easy_move(self):  # Easy difficulty - random move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            self.last_move_row, self.last_move_col = row, col

    def medium_move(self):  # Medium difficulty - block player
        # First check if computer can win
        if not self.check_for_win("O"):
            # Otherwise block player
            if not self.check_for_win("X"):
                # Otherwise make a random move
                self.easy_move()
    
    def hard_move(self):  # Hard difficulty - minimax
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        row, col = best_move
        self.board[row][col] = "O"
        self.buttons[row][col].config(text="O")
        self.last_move_row, self.last_move_col = row, col

    def check_for_win(self, player):  # Helper to check for winning move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = player
                    if self.check_winner(i, j):
                        self.board[i][j] = "O"
                        self.buttons[i][j].config(text="O")
                        self.last_move_row, self.last_move_col = i, j
                        return True
                    self.board[i][j] = ""
        return False

    def minimax(self, is_maximizing):
        if self.check_winner_state("O"):
            return 1
        elif self.check_winner_state("X"):
            return -1
        elif self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, row, col):  # Check if there is a winner
        # Check row
        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player:
            return True
        # Check column
        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
            return True
        # Check diagonal
        if row == col and self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
            return True
        if row + col == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
            return True
        return False

    def check_winner_state(self, player):  # Check if there is a winner for a specific player
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player:
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        return False

    def check_draw(self):  # Check if the game is a draw
        for row in self.board:  # Iterate through each row
            for cell in row:  # Iterate through each cell
                if cell == "":  # If there is an empty cell
                    return False  # It's not a draw
        return True  # It's a draw

    def reset_game(self):  # Reset the game
        for i in range(3):  # Iterate through each row
            for j in range(3):  # Iterate through each column
                self.board[i][j] = ""  # Clear the board cell
                self.buttons[i][j].config(text="")  # Reset the button text
        self.current_player = "X"  # Set the current player to "X"

    def update_win_labels(self):  # Update the win count labels
        self.player_win_label.config(text=f"{self.player_name} Wins: {self.player_wins}")
        self.computer_win_label.config(text=f"Witty Wins: {self.computer_wins}")

    def run(self):  # Run the game
        self.root.mainloop()  # Start the tkinter main loop

if __name__ == "__main__":  # If this script is run directly
    game = TicTacToe()  # Create an instance of the TicTacToe class
    game.run()  # Run the game
