import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and sets its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
    
        #Load the ship image and get its rect.
        self.image = pygame.image.load("C:\Work\Alien_invasion\shipimg.bmp")
        self.rect = self.image.get_rect()
    
        # Start new ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Store a decimal value for the ship horizontal position
        self.x = float(self.rect.x)
        # movements Flag
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """Update the ship's position based on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        """Update rect object from self.x"""
        self.rect.x = self.x
    
    def blitme(self):
        """Draw the ship at its current position"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
            