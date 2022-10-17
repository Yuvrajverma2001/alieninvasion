class Settings:
    """A class to store all the settings for alienInvasion"""
    
    def __init__(self):
        """Initialize the game settings"""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (255,255,255)
        #bullet setting
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0,0,0) 
        self.bullets_allowed = 5       
        #ship setting
        self.ship_speed = 1
        self.ship_limit = 3
        #alien setting
        self.alien_speed = 1.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 0.5
        #How quickly game speed up
        self.speedup_scale = 1.1
        # How Quickly the alien point values increases
        self.score_scale = 1.5
        
        # How quicly the alien point values increases
        self.score_scale = 1.5
        self.intialize_dynamic_settings()
        
    def intialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #Scoring
        self.alien_points = 50
        # fleet_direction of 1 represents right ; -1 represents left
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)