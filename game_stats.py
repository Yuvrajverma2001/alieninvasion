class GameStats:
    """Track Statics for alien invansion"""

    def __init__(self, ai_game):
        """Initialize Statics for alien invansion"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Alien Invansion in an active state
        self.game_active = False
        # High Score should never be reset
        self.high_score = 0
    def reset_stats(self):
        """"Initialize Stats for alien invansion"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1