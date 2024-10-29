import tkinter as tk
from tkinter import messagebox
import random


class Emojisweep:
    def __init__(self, master):
        self.frame = None
        self.master = master
        self.master.title("Buscaminas")
        self.size = 10  # Tamaño del tablero 10x10
        self.mines = 15  # Número de minas
        self.buttons = []
        self.mines_positions = set()
        self.game_over = False
        self.flags = set()
        self.revealed = set()

        # Emojis para el juego
        self.mine_emoji = "💥"
        self.flag_emoji = "🚩"
        self.covered_emoji = "⬜"
        self.numbers_emoji = ["⬜", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

        self.create_board()
        self.place_mines()

    def create_board(self):
        # Frame principal
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Crear botones
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(self.frame, width=2, height=1,
                                   font=('TkDefaultFont', 14),
                                   text=self.covered_emoji)
                button.grid(row=i, column=j)
                button.bind('<Button-1>', lambda e, row=i, col=j: self.click(row, col))
                button.bind('<Button-3>', lambda e, row=i, col=j: self.flag(row, col))
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        # Colocar minas aleatoriamente
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.mines_positions = set(random.sample(positions, self.mines))

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                r, c = row + i, col + j
                if (r, c) in self.mines_positions:
                    count += 1
        return count

    def reveal(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            return

        if (row, col) in self.revealed or (row, col) in self.flags:
            return

        self.revealed.add((row, col))

        if (row, col) in self.mines_positions:
            self.game_over = True
            self.reveal_all()
            messagebox.showinfo("Game Over", "¡Perdiste!")
            return

        adjacent = self.count_adjacent_mines(row, col)
        self.buttons[row][col].config(text=self.numbers_emoji[adjacent])

        if adjacent == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.reveal(row + i, col + j)

    def reveal_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.mines_positions:
                    self.buttons[i][j].config(text=self.mine_emoji)
                else:
                    adjacent = self.count_adjacent_mines(i, j)
                    self.buttons[i][j].config(text=self.numbers_emoji[adjacent])

    def click(self, row, col):
        if self.game_over:
            return
        if (row, col) not in self.flags:
            self.reveal(row, col)

    def flag(self, row, col):
        if self.game_over:
            return

        if (row, col) in self.revealed:
            return

        if (row, col) in self.flags:
            self.flags.remove((row, col))
            self.buttons[row][col].config(text=self.covered_emoji)
        else:
            self.flags.add((row, col))
            self.buttons[row][col].config(text=self.flag_emoji)

        # Verificar victoria
        if self.flags == self.mines_positions:
            messagebox.showinfo("¡Felicitaciones!", "¡Ganaste!")
            self.game_over = True


def main():
    root = tk.Tk()
    Emojisweep(root)
    root.mainloop()


if __name__ == "__main__":
    main()