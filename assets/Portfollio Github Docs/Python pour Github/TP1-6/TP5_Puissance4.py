import tkinter as tk
from tkinter import messagebox
import random

ROWS = 6
COLUMNS = 7

class Puissance4:
    def __init__(self, root):
        self.root = root
        self.root.title("Puissance 4 contre IA")

        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn = "player"

        self.buttons = [tk.Button(root, text="toucher", font=("Arial", 10), command=lambda c=c: self.player_move(c)) for c in range(COLUMNS)]
        for c, button in enumerate(self.buttons):
            button.grid(row=0, column=c, sticky="nsew")

        self.cells = [[tk.Canvas(root, width=60, height=60, bg="blue", highlightthickness=1) for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.cells[r][c].grid(row=r+1, column=c)
                self.cells[r][c].create_oval(5, 5, 55, 55, fill="white", tags="token")

        self.reset_button = tk.Button(root, text="Rejouer", font=("Arial", 12), command=self.reset)
        self.reset_button.grid(row=ROWS + 1, column=0, columnspan=COLUMNS // 2, sticky="nsew")

        self.quit_button = tk.Button(root, text="Quitter", font=("Arial", 12), command=root.quit)
        self.quit_button.grid(row=ROWS + 1, column=COLUMNS // 2, columnspan=COLUMNS - (COLUMNS // 2), sticky="nsew")

    def player_move(self, col):
        if self.turn != "player":
            return

        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = "player"
            self.update_cell(row, col, "red")
            if self.check_victory(row, col, "player"):
                self.show_winner("Joueur (Rouge)")
                return
            elif self.is_board_full():
                self.show_draw()
                return
            self.turn = "ai"
            self.root.after(500, self.ai_move)  # Laisse le temps à l'utilisateur de voir

    def ai_move(self):
        valid_columns = [c for c in range(COLUMNS) if self.get_next_open_row(c) is not None]
        if not valid_columns:
            return
        col = random.choice(valid_columns)
        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = "ai"
            self.update_cell(row, col, "yellow")
            if self.check_victory(row, col, "ai"):
                self.show_winner("IA (Jaune)")
                return
            elif self.is_board_full():
                self.show_draw()
                return
            self.turn = "player"

    def get_next_open_row(self, col):
        for row in reversed(range(ROWS)):
            if self.board[row][col] is None:
                return row
        return None

    def update_cell(self, row, col, color):
        canvas = self.cells[row][col]
        canvas.delete("token")
        canvas.create_oval(5, 5, 55, 55, fill=color, tags="token")

    def check_victory(self, row, col, player):
        def count(dx, dy):
            total = 0
            r, c = row + dy, col + dx
            while 0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == player:
                total += 1
                r += dy
                c += dx
            return total

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if 1 + count(dx, dy) + count(-dx, -dy) >= 4:
                return True
        return False

    def is_board_full(self):
        return all(self.board[0][c] is not None for c in range(COLUMNS))

    def show_winner(self, winner_name):
        messagebox.showinfo("Victoire !", f"{winner_name} a gagné !")
        self.reset()

    def show_draw(self):
        messagebox.showinfo("Match nul", "La grille est pleine. Match nul !")
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn = "player"
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.cells[r][c].delete("token")
                self.cells[r][c].create_oval(5, 5, 55, 55, fill="white", tags="token")


if __name__ == "__main__":
    root = tk.Tk()
    game = Puissance4(root)
    root.mainloop()
