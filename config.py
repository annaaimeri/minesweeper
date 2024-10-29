class GameConfig:
    def __init__(self):
        self.board_size = 10
        self.mines_count = 15
        self.emojis = {
            'mine': '💥',
            'flag': '🚩',
            'covered': '⬜',
            'numbers': ['⬜', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣']
        }