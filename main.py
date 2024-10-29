import tkinter as tk
from tkinter import ttk
from game_board import GameBoard


class EmojisweepApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Emojisweep")
        self.setup_ui()

    def setup_ui(self):
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Crear frame principal del juego
        self.game_frame = ttk.Frame(self.notebook)
        self.game_frame.pack(fill='both', expand=True)

        # Crear frames para cada pestaña
        self.settings_frame = ttk.Frame(self.notebook)
        self.instructions_frame = ttk.Frame(self.notebook)
        self.stats_frame = ttk.Frame(self.notebook)

        # Agregar pestañas al notebook
        self.notebook.add(self.game_frame, text='Juego')
        self.notebook.add(self.settings_frame, text='Configuración')
        self.notebook.add(self.instructions_frame, text='Instrucciones')
        self.notebook.add(self.stats_frame, text='Estadísticas')

        # Inicializar componentes
        self.game_board = GameBoard(self.game_frame)
        self.setup_instructions_tab()
        self.setup_stats_tab()
        self.setup_settings_tab()

    def setup_instructions_tab(self):
        instructions = """
        Bienvenido a Emojisweep!

        Cómo jugar:
        • Click izquierdo: Revelar casilla
        • Click derecho: Colocar/quitar bandera

        Objetivo:
        Encuentra todas las minas sin detonar ninguna.
        Marca las minas con banderas y revela las casillas seguras.

        Pistas:
        • Los números indican cuántas minas hay alrededor
        • Usa las banderas sabiamente para marcar las minas
        • Si revelas una mina, ¡pierdes!
        """

        text_widget = tk.Text(self.instructions_frame, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert('1.0', instructions)
        text_widget.config(state='disabled')

    def setup_stats_tab(self):
        stats_frame = ttk.LabelFrame(self.stats_frame, text="Estadísticas de Juego")
        stats_frame.pack(padx=10, pady=5, fill="both", expand=True)

        stats = [
            ("Partidas jugadas:", "0"),
            ("Partidas ganadas:", "0"),
            ("Mejor tiempo:", "---"),
            ("Racha actual:", "0"),
            ("Mejor racha:", "0")
        ]

        for label, value in stats:
            frame = ttk.Frame(stats_frame)
            frame.pack(fill="x", padx=5, pady=2)
            ttk.Label(frame, text=label).pack(side="left")
            ttk.Label(frame, text=value).pack(side="right")

    def setup_settings_tab(self):
        # Frame para dificultad
        difficulty_frame = ttk.LabelFrame(self.settings_frame, text="Dificultad")
        difficulty_frame.pack(padx=10, pady=5, fill="x")

        self.difficulty_var = tk.StringVar(value="normal")
        difficulties = [
            ("Fácil (8x8, 10 minas)", "easy"),
            ("Normal (10x10, 15 minas)", "normal"),
            ("Difícil (12x12, 25 minas)", "hard"),
            ("Personalizado", "custom")
        ]

        for text, value in difficulties:
            ttk.Radiobutton(difficulty_frame, text=text, value=value,
                            variable=self.difficulty_var).pack(anchor="w", padx=5, pady=2)

        # Frame para personalización
        custom_frame = ttk.LabelFrame(self.settings_frame, text="Configuración Personalizada")
        custom_frame.pack(padx=10, pady=5, fill="x")

        # Tamaño del tablero
        ttk.Label(custom_frame, text="Tamaño del tablero:").pack(anchor="w", padx=5)
        self.size_var = tk.StringVar(value="10")
        ttk.Entry(custom_frame, textvariable=self.size_var, width=5).pack(anchor="w", padx=5)

        # Número de minas
        ttk.Label(custom_frame, text="Número de minas:").pack(anchor="w", padx=5)
        self.mines_var = tk.StringVar(value="15")
        ttk.Entry(custom_frame, textvariable=self.mines_var, width=5).pack(anchor="w", padx=5)

        # Botón para aplicar cambios
        ttk.Button(self.settings_frame, text="Aplicar Cambios",
                   command=self.apply_settings).pack(pady=10)

    def apply_settings(self):
        difficulty = self.difficulty_var.get()
        if difficulty == "custom":
            try:
                size = int(self.size_var.get())
                mines = int(self.mines_var.get())
                if size < 5 or size > 20:
                    tk.messagebox.showerror("Error", "El tamaño debe estar entre 5 y 20")
                    return
                if mines < 1 or mines > (size * size - 1):
                    tk.messagebox.showerror("Error", "Número de minas inválido")
                    return
                # Aquí implementaremos la actualización del tablero
            except ValueError:
                tk.messagebox.showerror("Error", "Valores inválidos")
        else:
            # Configuraciones predefinidas
            configs = {
                "easy": (8, 10),
                "normal": (10, 15),
                "hard": (12, 25)
            }
            size, mines = configs[difficulty]
            # Aquí implementaremos la actualización del tablero

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmojisweepApp()
    app.run()