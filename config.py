class GameConfig:
    def __init__(self):
        self.board_size = 10
        self.mines_count = 15
        self.current_theme = 'classic'

        # Definición de temas disponibles
        self.themes = {
            'classic': {
                'mine': '💣',
                'flag': '🚩',
                'covered': '⬜',
                'explosion': '💥',
                'numbers': ['⬜', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'nature': {
                'mine': '🌋',
                'flag': '🌿',
                'covered': '🟩',
                'explosion': '🔥',
                'numbers': ['🟩', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'halloween': {
                'mine': '👻',
                'flag': '🎃',
                'covered': '⬛',
                'explosion': '💀',
                'numbers': ['⬛', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'ocean': {
                'mine': '🐡',
                'flag': '🏊',
                'covered': '🌊',
                'explosion': '🌊',
                'numbers': ['🌊', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'space': {
                'mine': '🛸',
                'flag': '🚀',
                'covered': '⭐',
                'explosion': '💫',
                'numbers': ['⭐', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'christmas': {
                'mine': '🎅',
                'flag': '🎄',
                'covered': '❄️',
                'explosion': '☃️',
                'numbers': ['❄️', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            },
            'fashion': {
                'mine': '👠',
                'flag': '👜',
                'covered': '🎀',
                'explosion': '💝',
                'numbers': ['🎀', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
            }
        }

        # Inicializar emojis con el tema por defecto
        self.emojis = self.themes[self.current_theme]

    def update_config(self, size=None, mines=None, theme=None):
        if size is not None:
            self.board_size = size
        if mines is not None:
            self.mines_count = mines
        if theme is not None and theme in self.themes:
            self.current_theme = theme
            self.emojis = self.themes[theme]