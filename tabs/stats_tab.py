class StatsTab:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
        # Crear widgets para mostrar estadísticas
        stats_frame = ttk.LabelFrame(self.master, text="Estadísticas de Juego")
        stats_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Ejemplo de estadísticas a mostrar
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