import tkinter as tk
from tkinter import ttk, messagebox
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
        self.setup_settings_tab()
        self.setup_instructions_tab()
        self.setup_stats_tab()

    def setup_settings_tab(self):
        # Frame principal para configuración con dos columnas
        main_frame = ttk.Frame(self.settings_frame)
        main_frame.pack(fill='both', expand=True)

        # Columna izquierda: Configuración del juego
        game_config_frame = ttk.LabelFrame(main_frame, text="Configuración del Juego")
        game_config_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Dificultad
        difficulty_frame = ttk.LabelFrame(game_config_frame, text="Dificultad")
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
                            variable=self.difficulty_var,
                            command=self.toggle_custom_fields).pack(anchor="w", padx=5, pady=2)

        # Frame para configuración personalizada
        self.custom_frame = ttk.LabelFrame(game_config_frame, text="Configuración Personalizada")
        self.custom_frame.pack(padx=10, pady=5, fill="x")

        # Tamaño del tablero
        ttk.Label(self.custom_frame, text="Tamaño del tablero:").pack(anchor="w", padx=5)
        self.size_var = tk.StringVar(value="10")
        self.size_entry = ttk.Entry(self.custom_frame, textvariable=self.size_var, width=5)
        self.size_entry.pack(anchor="w", padx=5)

        # Número de minas
        ttk.Label(self.custom_frame, text="Número de minas:").pack(anchor="w", padx=5)
        self.mines_var = tk.StringVar(value="15")
        self.mines_entry = ttk.Entry(self.custom_frame, textvariable=self.mines_var, width=5)
        self.mines_entry.pack(anchor="w", padx=5)

        # Columna derecha: Temas
        theme_frame = ttk.LabelFrame(main_frame, text="Temas")
        theme_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        # Variable para el tema seleccionado
        self.theme_var = tk.StringVar(value="classic")

        # Crear un frame con scroll para los temas
        theme_canvas = tk.Canvas(theme_frame)
        theme_scrollbar = ttk.Scrollbar(theme_frame, orient="vertical", command=theme_canvas.yview)
        theme_scrollable_frame = ttk.Frame(theme_canvas)

        theme_scrollable_frame.bind(
            "<Configure>",
            lambda e: theme_canvas.configure(scrollregion=theme_canvas.bbox("all"))
        )

        theme_canvas.create_window((0, 0), window=theme_scrollable_frame, anchor="nw")
        theme_canvas.configure(yscrollcommand=theme_scrollbar.set)

        # Definición de temas con sus descripciones
        themes_data = {
            'classic': ("Clásico (💣 🚩 ⬜)",
                        "El clásico buscaminas con bombas y banderas"),
            'nature': ("Naturaleza (🌋 🌿 🟩)",
                       "Tema natural con volcanes y hojas"),
            'halloween': ("Halloween (👻 🎃 ⬛)",
                          "Tema de Halloween con fantasmas y calabazas"),
            'ocean': ("Océano (🐡 🏊 🌊)",
                      "Aventura submarina con peces y nadadores"),
            'space': ("Espacio (🛸 🚀 ⭐)",
                      "Exploración espacial con ovnis y cohetes"),
            'christmas': ("Navidad (🎅 🎄 ❄️)",
                          "Espíritu navideño con Papá Noel y árboles de navidad"),
            'fashion': ("Fashion (👠 👜 🎀)",
                        "Tema con zapatos y accesorios")
        }

        for theme_id, (theme_name, description) in themes_data.items():
            theme_container = ttk.Frame(theme_scrollable_frame)
            theme_container.pack(fill="x", padx=5, pady=2)

            theme_button = ttk.Radiobutton(
                theme_container,
                text=theme_name,
                value=theme_id,
                variable=self.theme_var
            )
            theme_button.pack(side="top", anchor="w")

            description_label = ttk.Label(
                theme_container,
                text=description,
                font=('TkDefaultFont', 8),
                foreground='gray'
            )
            description_label.pack(side="top", anchor="w", padx=20)

        theme_canvas.pack(side="left", fill="both", expand=True, padx=(5, 0))
        theme_scrollbar.pack(side="right", fill="y")

        # Preview frame
        preview_frame = ttk.LabelFrame(theme_frame, text="Vista Previa")
        preview_frame.pack(padx=10, pady=5, fill="x")

        self.preview_label = ttk.Label(preview_frame, text="")
        self.preview_label.pack(pady=10)

        # Botón para aplicar cambios
        ttk.Button(self.settings_frame, text="Aplicar Cambios",
                   command=self.apply_settings).pack(pady=10)

        # Inicializar estados
        self.toggle_custom_fields()
        self.theme_var.trace('w', self.update_preview)
        self.update_preview()

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

        Consejos:
        • Comienza por las esquinas o bordes
        • Usa la lógica para deducir la ubicación de las minas
        • No tengas miedo de usar las banderas
        • Si no estás seguro, toma tu tiempo
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

    def toggle_custom_fields(self):
        """Habilita/deshabilita los campos de configuración personalizada"""
        state = 'normal' if self.difficulty_var.get() == 'custom' else 'disabled'
        self.size_entry.config(state=state)
        self.mines_entry.config(state=state)

    def update_preview(self, *args):
        """Actualiza la vista previa del tema seleccionado"""
        theme = self.theme_var.get()
        preview_text = f"Mina: {self.game_board.config.themes[theme]['mine']}  "
        preview_text += f"Bandera: {self.game_board.config.themes[theme]['flag']}  "
        preview_text += f"Cubierto: {self.game_board.config.themes[theme]['covered']}"
        self.preview_label.config(text=preview_text)

    def apply_settings(self):
        """Aplica los cambios de configuración"""
        # Obtener el tema seleccionado
        new_theme = self.theme_var.get()

        # Obtener tamaño y minas según la dificultad
        difficulty = self.difficulty_var.get()
        if difficulty == "custom":
            try:
                size = int(self.size_var.get())
                mines = int(self.mines_var.get())
                if size < 5 or size > 20:
                    messagebox.showerror("Error", "El tamaño debe estar entre 5 y 20")
                    return
                if mines < 1 or mines > (size * size - 1):
                    messagebox.showerror("Error", "Número de minas inválido")
                    return
            except ValueError:
                messagebox.showerror("Error", "Valores inválidos")
                return
        else:
            # Configuraciones predefinidas
            configs = {
                "easy": (8, 10),
                "normal": (10, 15),
                "hard": (12, 25)
            }
            size, mines = configs[difficulty]

        # Actualizar configuración
        self.game_board.config.update_config(size=size, mines=mines, theme=new_theme)

        # Reiniciar el juego
        self.game_board.reset_game()

        messagebox.showinfo("Éxito", "Configuración actualizada correctamente")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmojisweepApp()
    app.run()