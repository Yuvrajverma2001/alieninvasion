import sys
from time import sleep
import pygame
from settings import Settings
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien



class alieninvasion:
    """Overall class to manage game assets and behaviour"""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Aliens Invasion")
        
        # Creating an instance to store game statistics amd Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
    
        #Make the PLay Button
        self.play_button = Button(self, "Play")
               
        #Set the background color of the screen
        self.bg_color = (255, 255, 255)
        
    
    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()
                
                # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            # Draw the Score information
            self.sb.show_score()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            
            self.aliens.draw(self.screen)
            # Draw the play button if the game is inactive.
            if not self.stats.game_active:
                self.play_button.draw_button()
            
            # Make the most recently dran screen visible.
            pygame.display.flip()
    
    def _check_events(self):
        """Respond to keypress and mouse events."""        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                       
    def _check_keydown_events(self, event):
        """Respond to Keypress"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit(0)
        
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        #get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #Remove any bullets and aliens that have collided.
        #Check for any bullet thatbhave hit the alien.
        #If so get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            #Destroy the Existing Bullet and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            #Increase level.
            self.stats.level += 1
            self.sb.prep_level()
        
        if collisions:
            for aliens  in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
    def _update_screen(self):
        """update image on the screen, and flip the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Draw the Score information
        self.sb.show_score()
        
        pygame.display.flip
    
    def _create_fleet(self):
        """Create a fleet of aliens."""
        #Create an alien and find the nukmber of aliens in row
        #spacing b/w each line is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        #Determine the number of rows of alien that fit on screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - ( 3*alien_height) - ship_height)
        number_rows = available_space_y // (2* alien_height) 
    
        #create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
        #create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self.aliens.update()
        self._check_fleet_edges()
        
        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship Hit !!!!!")
            self._ship_hit()
            
        #Look for alien hitting the bottom of the screen
        self._check_aliens_bottom()
            
    def _check_fleet_edges(self):
        """Respond appropriately if any alien have reached and edge"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change its direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 1:
            #Decrement ship left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            #Get rid of any remaining alien and bullets
            self.aliens.empty()
            self.bullets.empty()
        
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
        
            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break      
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reset the game settings
            self.settings.intialize_dynamic_settings()

            #Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            
            #Hide the mouse cursor 
            pygame.mouse.set_visible(False)
                               
if __name__ == '__main__':
    #make a game instance and run the game.
    ai = alieninvasion()
    ai.run_game()
