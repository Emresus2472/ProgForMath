import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Reversi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reversi Spel")
        self.configure(bg="green")
        self.geometry("685x559")

        self.size = 6
        self.turn = "Blue"
        self.board = []
        self.board_colors = []  # Track colors separately
        self.possible_moves = []
        self.show_help = False  # Help toggle

        self.create_widgets()
        self.create_board_buttons()
        self.update_possible_moves()  # Initialize possible moves

    def create_widgets(self):
        self.new_game = tk.Button(self, text="Nieuw Spel", command=self.new_game_click)
        self.new_game.place(x=46, y=26, width=109, height=23)

        self.help = tk.Button(self, text="Help", command=self.help_click)
        self.help.place(x=161, y=26, width=75, height=23)

        self.red_stone = ImageTk.PhotoImage(Image.open("resources/Red.png").resize((40, 42)))
        self.blue_stone = ImageTk.PhotoImage(Image.open("resources/Blue.png").resize((40, 42)))

        self.red_indicator = tk.Label(self, image=self.red_stone)
        self.red_indicator.place(x=283, y=67)

        self.blue_indicator = tk.Label(self, image=self.blue_stone)
        self.blue_indicator.place(x=283, y=115)

        self.red_score = tk.Label(self, text="2", font=("Microsoft Sans Serif", 20), fg="white", bg="green")
        self.red_score.place(x=329, y=78)

        self.blue_score = tk.Label(self, text="2", font=("Microsoft Sans Serif", 20), fg="white", bg="green")
        self.blue_score.place(x=329, y=126)

        self.red_turn = tk.Label(self, text="Rood aan zet", font=("Microsoft Sans Serif", 12, "bold"), fg="white", bg="green")
        self.red_turn.place(x=160, y=78)

        self.blue_turn = tk.Label(self, text="Blauw aan zet", font=("Microsoft Sans Serif", 12, "bold"), fg="white", bg="green")
        self.blue_turn.place(x=160, y=126)

        self.possible_moves_label = tk.Label(self, text="", font=("Microsoft Sans Serif", 8, "bold"), fg="white", bg="green")
        self.possible_moves_label.place(x=447, y=56)

        self.possible_moves_title = tk.Label(self, text="Mogelijke zetten", font=("Microsoft Sans Serif", 8, "bold"), fg="white", bg="green")
        self.possible_moves_title.place(x=433, y=36)

        self.button_4x4 = tk.Button(self, text="4x4", command=lambda: self.bord_size_click(4))
        self.button_4x4.place(x=46, y=57, width=75, height=23)

        self.button_6x6 = tk.Button(self, text="6x6", command=lambda: self.bord_size_click(6))
        self.button_6x6.place(x=46, y=86, width=75, height=23)

        self.button_8x8 = tk.Button(self, text="8x8", command=lambda: self.bord_size_click(8))
        self.button_8x8.place(x=46, y=113, width=75, height=23)

        self.button_12x12 = tk.Button(self, text="12x12", command=lambda: self.bord_size_click(12))
        self.button_12x12.place(x=46, y=142, width=75, height=23)

    def create_board_buttons(self):
        x, y = 130, 200
        for i in range(self.size):
            row = []
            color_row = []
            for j in range(self.size):
                button = tk.Button(self, width=4, height=2, command=lambda r=i, c=j: self.button_is_clicked(r, c))
                button.place(x=x, y=y, width=40, height=40)
                button.config(bg="white")
                row.append(button)
                color_row.append("white")
                x += 40
            self.board.append(row)
            self.board_colors.append(color_row)
            x = 130
            y += 40

        mid = self.size // 2
        self.set_stone(mid-1, mid-1, "Red")
        self.set_stone(mid, mid, "Red")
        self.set_stone(mid-1, mid, "Blue")
        self.set_stone(mid, mid-1, "Blue")

    def set_stone(self, row, col, color):
        if color == "Red":
            self.board[row][col].config(image=self.red_stone, width=40, height=40)
        elif color == "Blue":
            self.board[row][col].config(image=self.blue_stone, width=40, height=40)
        else:
            self.board[row][col].config(image="", width=4, height=2)
        self.board_colors[row][col] = color

    def mogelijk_zetten(self, t):
        move = "Blue" if t == "Red" else "Red"
        self.possible_moves.clear()

        for i in range(self.size):
            for j in range(self.size):
                if self.board_colors[j][i] == t:
                    directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
                    for dx, dy in directions:
                        x, y = i + dx, j + dy
                        if 0 <= x < self.size and 0 <= y < self.size and self.board_colors[y][x] == move:
                            while 0 <= x < self.size and 0 <= y < self.size:
                                if self.board_colors[y][x] == "white":
                                    self.possible_moves.append((y, x))
                                    break
                                elif self.board_colors[y][x] == t:
                                    break
                                x, y = x + dx, y + dy

    def highlight_possible_moves(self):
        for y, x in self.possible_moves:
            self.board[y][x].config(bg="lightgray")

    def flipping(self, row, col):
        directions = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]
        for dx, dy in directions:
            self.flip_direction(row, col, dx, dy)

    def flip_direction(self, row, col, dx, dy):
        x, y = col + dx, row + dy
        to_flip = []
        while 0 <= x < self.size and 0 <= y < self.size:
            if self.board_colors[y][x] == "white":
                break
            if self.board_colors[y][x] == self.turn:
                for r, c in to_flip:
                    self.set_stone(r, c, self.turn)
                break
            to_flip.append((y, x))
            x, y = x + dx, y + dy

    def tellen(self):
        red_score = sum(1 for row in self.board_colors for color in row if color == "Red")
        blue_score = sum(1 for row in self.board_colors for color in row if color == "Blue")
        self.red_score.config(text=str(red_score))
        self.blue_score.config(text=str(blue_score))

    def verwijder_mogelijke_zetten(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board_colors[row][col] == "white":
                    self.board[row][col].config(bg="white")

    def button_is_clicked(self, row, col):
        if (row, col) in self.possible_moves:  # Directly check 0-based indices
            self.set_stone(row, col, self.turn)
            self.flipping(row, col)
            self.turn = "Blue" if self.turn == "Red" else "Red"
            self.red_turn.config(text="Rood aan zet" if self.turn == "Red" else "")
            self.blue_turn.config(text="Blauw aan zet" if self.turn == "Blue" else "")
            self.verwijder_mogelijke_zetten()
            self.update_possible_moves()  # Update moves for the next turn
            self.tellen()

            if not self.possible_moves:
                if not self.check_for_any_moves():
                    self.end_game()

    def update_possible_moves(self):
        self.mogelijk_zetten(self.turn)
        if self.show_help:
            self.highlight_possible_moves()

    def check_for_any_moves(self):
        previous_turn = self.turn
        self.turn = "Red" if self.turn == "Blue" else "Blue"
        self.mogelijk_zetten(self.turn)
        has_moves = len(self.possible_moves) > 0
        self.turn = previous_turn
        return has_moves

    def end_game(self):
        red_score = int(self.red_score.cget("text"))
        blue_score = int(self.blue_score.cget("text"))
        winner = "Red" if red_score > blue_score else "Blue"
        messagebox.showinfo("Game Over", f"No Moves Left. {winner} Wins!")

    def update_possible_moves_label(self):
        if self.show_help:
            self.possible_moves_label.config(text="\n".join(f"{row + 1},{col + 1}" for row, col in self.possible_moves))
        else:
            self.possible_moves_label.config(text="")

    def new_game_click(self):
        self.destroy()
        Reversi().mainloop()

    def help_click(self):
        self.show_help = not self.show_help
        self.verwijder_mogelijke_zetten()
        if self.show_help:
            self.update_possible_moves()
        else:
            self.possible_moves.clear()
            self.update_possible_moves_label()

    def bord_size_click(self, size):
        self.size = size
        self.board.clear()
        self.board_colors.clear()
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button) and widget != self.new_game and widget != self.help:
                widget.destroy()
        self.create_board_buttons()
        self.update_possible_moves()
        self.blue_turn.config(text="Blauw aan zet")
        self.tellen()
        if size == 12:
            self.geometry("685x709")

if __name__ == "__main__":
    app = Reversi()
    app.mainloop()
MASSIMO
