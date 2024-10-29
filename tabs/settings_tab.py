class SettingsTab:
    def __init__(self, master, game_board):
        self.master = master
        self.game_board = game_board
        self.setup_ui()

    def setup_ui(self):
        # Frame para dificultad
        difficulty_frame = ttk.LabelFrame(self.master, text="Dificultad")
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
        custom_frame = ttk.LabelFrame(self.master, text="Configuración Personalizada")
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
        ttk.Button(self.master, text="Aplicar Cambios",
                   command=self.apply_settings).pack(pady=10)

    def apply_settings(self):
        # Implementar la lógica para aplicar los cambios
        pass