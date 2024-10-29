import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime
from config import GameConfig


class GameBoard:
    def __init__(self, master):
        self.master = master
        self.config = GameConfig()
        self.setup_game()
        self.create_top_frame()
        self.create_board()
        self.place_mines()

    def setup_game(self):
        """Inicializa las variables del juego"""
        self.size = self.config.board_size
        self.mines = self.config.mines_count
        self.buttons = []
        self.mines_positions = set()
        self.game_over = False
        self.flags = set()
        self.revealed = set()
        self.start_time = None
        self.timer_running = False
        self.elapsed_time = 0

    def create_top_frame(self):
        """Crea el frame superior con el contador de minas y el temporizador"""
        if hasattr(self, 'top_frame'):
            self.top_frame.destroy()

        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=5)

        # Contador de minas
        self.mines_label = tk.Label(
            self.top_frame,
            text=f"💣 {self.mines}",
            font=('TkDefaultFont', 12, 'bold')
        )
        self.mines_label.pack(side=tk.LEFT, padx=20)

        # Temporizador
        self.timer_label = tk.Label(
            self.top_frame,
            text="⏱️ 0:00",
            font=('TkDefaultFont', 12, 'bold')
        )
        self.timer_label.pack(side=tk.RIGHT, padx=20)

    def create_board(self):
        """Crea el tablero de juego con botones"""
        if hasattr(self, 'frame'):
            self.frame.destroy()

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=5)

        # Crear botones
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(
                    self.frame,
                    width=2,
                    height=1,
                    font=('TkDefaultFont', 14),
                    text=self.config.emojis['covered']
                )
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind('<Button-1>', lambda e, row=i, col=j: self.click(row, col))
                button.bind('<Button-3>', lambda e, row=i, col=j: self.flag(row, col))
                row.append(button)
            self.buttons.append(row)

    def reset_game(self):
        """Reinicia completamente el juego"""
        # Detener el temporizador si está corriendo
        self.timer_running = False

        # Limpiar el tablero
        if hasattr(self, 'frame'):
            for row in self.buttons:
                for button in row:
                    button.destroy()

        # Reiniciar variables
        self.buttons = []
        self.setup_game()

        # Recrear la interfaz
        self.create_top_frame()
        self.create_board()
        self.place_mines()

    def place_mines(self):
        """Coloca las minas aleatoriamente en el tablero"""
        positions = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.mines_positions = set(random.sample(positions, self.mines))

    def start_timer(self):
        """Inicia el temporizador"""
        if not self.timer_running:
            self.start_time = datetime.now()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        """Actualiza el temporizador"""
        if self.timer_running and not self.game_over:
            now = datetime.now()
            self.elapsed_time = (now - self.start_time).seconds
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"⏱️ {minutes}:{seconds:02d}")
            self.master.after(1000, self.update_timer)

    def count_adjacent_mines(self, row, col):
        """Cuenta el número de minas adyacentes a una casilla"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                r, c = row + i, col + j
                if (0 <= r < self.size and
                        0 <= c < self.size and
                        (r, c) in self.mines_positions):
                    count += 1
        return count

    def reveal(self, row, col):
        """Revela una casilla y sus adyacentes si es necesario"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return

        if (row, col) in self.revealed or (row, col) in self.flags:
            return

        # Iniciar el temporizador en el primer click
        if not self.revealed:
            self.start_timer()

        self.revealed.add((row, col))

        if (row, col) in self.mines_positions:
            self.game_over = True
            self.timer_running = False
            self.reveal_all()
            messagebox.showinfo("Game Over", "¡Has perdido! 💥")
            return

        adjacent = self.count_adjacent_mines(row, col)
        self.buttons[row][col].config(text=self.config.emojis['numbers'][adjacent])

        # Si no hay minas adyacentes, revelar casillas cercanas
        if adjacent == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    self.reveal(row + i, col + j)

        # Verificar victoria
        self.check_victory()

    def reveal_all(self):
        """Revela todas las casillas del tablero"""
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.mines_positions:
                    self.buttons[i][j].config(text=self.config.emojis['mine'])
                else:
                    adjacent = self.count_adjacent_mines(i, j)
                    self.buttons[i][j].config(text=self.config.emojis['numbers'][adjacent])

    def click(self, row, col):
        """Maneja el click izquierdo en una casilla"""
        if self.game_over:
            return
        if (row, col) not in self.flags:
            self.reveal(row, col)

    def flag(self, row, col):
        """Maneja el click derecho para colocar/quitar banderas"""
        if self.game_over:
            return

        if (row, col) in self.revealed:
            return

        if (row, col) in self.flags:
            self.flags.remove((row, col))
            self.buttons[row][col].config(text=self.config.emojis['covered'])
            self.mines_label.config(text=f"💣 {self.mines - len(self.flags)}")
        else:
            self.flags.add((row, col))
            self.buttons[row][col].config(text=self.config.emojis['flag'])
            self.mines_label.config(text=f"💣 {self.mines - len(self.flags)}")

        # Verificar victoria
        self.check_victory()

    def check_victory(self):
        """Verifica si el jugador ha ganado"""
        if (self.flags == self.mines_positions and
                len(self.revealed) == self.size * self.size - self.mines):
            self.game_over = True
            self.timer_running = False
            messagebox.showinfo("¡Felicitaciones!",
                                f"¡Has ganado! 🎉\nTiempo: {self.elapsed_time} segundos")