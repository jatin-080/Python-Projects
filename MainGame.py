import tkinter as tk
import random
import time

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        
        # Players and whose turn it is
        self.players = ["Player 1", "Player 2"]
        self.current_player = 0  # Player turn tracker
        
        # Board size and cell dimensions
        self.board_size = 10
        self.cell_size = 50
        
        # Snakes and Ladders mappings
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        
        # Player positions start at 0
        self.player_positions = {self.players[0]: 0, self.players[1]: 0}
        self.game_over = False
        
        # Label to display dice roll result
        self.dice_roll_label = tk.Label(self.root, text="Roll the Dice!", font=('Arial', 16))
        self.dice_roll_label.grid(row=0, column=0, columnspan=3)
        
        # Dice roll button
        self.roll_button = tk.Button(self.root, text="Roll Dice", font=('Arial', 14), command=self.roll_dice)
        self.roll_button.grid(row=1, column=0, columnspan=3)
        
        # Canvas for the board drawing
        self.canvas = tk.Canvas(self.root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size)
        self.canvas.grid(row=2, column=0, columnspan=3)
        
        # Draw the initial game board
        self.draw_board()

    def draw_board(self):
        """Draws the board, snakes, and ladders"""
        # Create board grid
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = 'white' if (row + col) % 2 == 0 else 'light gray'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                # Add cell numbers
                cell_number = (self.board_size * (self.board_size - 1 - row)) - col
                self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text=str(cell_number), font=('Arial', 10))
        
        # Draw snakes
        for start, end in self.snakes.items():
            start_pos = self.get_coordinates(start)
            end_pos = self.get_coordinates(end)
            self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], width=3, fill='red')
        
        # Draw ladders
        for start, end in self.ladders.items():
            start_pos = self.get_coordinates(start)
            end_pos = self.get_coordinates(end)
            self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], width=3, fill='green')
        
        # Draw player positions
        for player, position in self.player_positions.items():
            pos = self.get_coordinates(position)
            self.canvas.create_oval(pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15, fill="blue", outline="black")
            self.canvas.create_text(pos[0], pos[1], text=player[7], font=('Arial', 12, 'bold'), fill="white")
        
    def get_coordinates(self, cell):
        """Get x, y coordinates for a given cell number on the board"""
        row = (self.board_size * self.board_size - cell) // self.board_size
        col = (cell - 1) % self.board_size
        x = col * self.cell_size + self.cell_size / 2
        y = row * self.cell_size + self.cell_size / 2
        return x, y

    def roll_dice(self):
        """Simulates a dice roll and updates player position"""
        if self.game_over:
            return
        
        # Roll the dice
        dice_value = random.randint(1, 6)
        self.dice_roll_label.config(text=f"{self.players[self.current_player]} rolled a {dice_value}")
        
        current_position = self.player_positions[self.players[self.current_player]]
        new_position = current_position + dice_value
        
        # Check if the new position is within bounds (<=100)
        if new_position <= 100:
            if new_position in self.snakes:
                new_position = self.snakes[new_position]
                self.dice_roll_label.config(text=f"{self.players[self.current_player]} hit a snake!")
            elif new_position in self.ladders:
                new_position = self.ladders[new_position]
                self.dice_roll_label.config(text=f"{self.players[self.current_player]} climbed a ladder!")
            
            self.player_positions[self.players[self.current_player]] = new_position
        
        # Redraw board with updated positions
        self.canvas.delete("all")
        self.draw_board()
        
        # Check for winner
        if self.player_positions[self.players[self.current_player]] == 100:
            self.dice_roll_label.config(text=f"{self.players[self.current_player]} wins!")
            self.game_over = True
        else:
            # Switch turn to next player
            self.current_player = (self.current_player + 1) % 2
            time.sleep(1)  # Add a short delay for smoother gameplay

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()
import tkinter as tk
import random
import time
