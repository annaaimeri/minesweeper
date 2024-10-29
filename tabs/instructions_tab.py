class InstructionsTab:
    def __init__(self, master):
        self.master = master
        self.setup_ui()

    def setup_ui(self):
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

        text_widget = tk.Text(self.master, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert('1.0', instructions)
        text_widget.config(state='disabled')