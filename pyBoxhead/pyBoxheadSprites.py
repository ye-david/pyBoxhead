''' Name: David Ye

    Date: May 31, 2017
    
    Description: Sprite file for pyBoxhead.
    
    Thank you to the following sprite creators:
    
    Boxhead Sprites originally created by: Tim Schiesser (Photobucket: scorpus57)
    Explosion Sprites: Found in ICS3U Donations Folder, Cropped by Mr. Rao
    Bullet Sprite: From chrismalnu.wordpress.com
    Zombie Font: Captain Redemption, created by Octotype
    Boxhead Logo: Sean Cooper
    Python Logo: Python Software Foundation
    
'''
# Import OS in order to access explosion directory.
import pygame, os

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the Player'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameters.  
        It loads the player image.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Load player sprite.
        self.image = pygame.image.load("player.png")
        # Conversion not used to maintain transparency
        self.rect = self.image.get_rect()
        self.__screen = screen
        
        # Initial player X location is at half the screen width, 200px down
        self.rect.center = (self.__screen.get_width()/2, 200)
 
        # Set initial x and y vector.
        self.__dx = 0
        self.__dy = 0 

    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the 
        x element from it, and uses this to set the players x direction.'''
        
        self.__dx = xy_change[0]
        # DY values are changed from pos to neg, and vice versa. This is because
        # pygame goes from 0 up, and not the other way around.
        self.__dy = xy_change[1] * -1 
         
    def update(self):
        ''' This method will be called automatically to reposition the player sprite
        on the screen.'''
        
        #Check if player has reached side edges. If not, keep moving
        # player in the same x direction. If yes, don't change x position at all.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
            self.rect.centerx += self.__dx*4
        else:
            self.__dx = 0
        # Check if player has reach bottom edge. If not, keep moving player in
        # same y direction. If yes, don't change y position at all.
        if self.rect.top < 60:
            self.rect.top = 60
        elif self.rect.bottom > self.__screen.get_height()-102:
            self.rect.bottom = self.__screen.get_height()-102
        else:
            self.rect.centery += self.__dy*4        
        
class Bullet(pygame.sprite.Sprite):
    '''This class defines the sprite for the Bullet'''
    def __init__(self, screen, player_x, player_y):
        '''This initializer takes a screen surface, and player center x coords,
        and the player's rect bottom coord. '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Load bullet png.
        self.image = pygame.image.load("bullet.png")
        # Conversion not used to maintain transparency
        self.rect = self.image.get_rect()
        self.__screen = screen
        # Bullet center position is set to the center x of the player, and
        # y is set to the coord of the players rect.bottom
        self.rect.centery = player_y
        self.rect.centerx = player_x
 
        # Set initial y vector.
        self.__dy = 3 

    def update(self):
        ''' This method will be called automatically to keep the bullet moving
        on the screen'''
        
        # If the bullet hasn't reached the bottom of the screen, keep the
        # bullet moving. Else, kill the bullet sprite.
        if self.rect.bottom > self.__screen.get_height()-110: 
            self.kill()        
        else:
            self.rect.centery += self.__dy*6

class Zombie(pygame.sprite.Sprite):
    ''' This class defines the sprite for the Zombie'''
    def __init__(self, screen, zombie_x):
        '''This initializer takes a screen surface, and a randomly generated x
        coordinate as parameters. '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Load the zombie sprite.
        self.image = pygame.image.load("zombie.png")
        # Conversion not used to maintain transparency
        self.rect = self.image.get_rect()
        self.__screen = screen
        
        # Initial Zombie y position is set to the bottom of the screen edge,
        # x position is randomly generated, so that the player cannot predict
        # where the zombie spawns
        self.rect.bottom = self.__screen.get_height()-102
        self.rect.centerx = zombie_x
 
        # Set initial y vector. Y vector is negative since the sprite is moving
        # from bottom to top
        self.__dy = -1

    def update(self):
        ''' This method will be called automatically to reposition the zombie sprite
        on the screen.'''
        
        # Check if zombie sprite has reached the top wall. If reached top wall,
        # do not let it go further. If havent reached top, keep moving the zombie.
        
        if self.rect.top < 30:
            self.rect.top = 30
        else:
            self.rect.centery += self.__dy*1.25
            
            
class Explosion(pygame.sprite.Sprite):
    ''' This class defines the explosion sprite.'''
    def __init__(self, screen, object_x, object_y):
        '''This initializer takes a screen surface, and the object x and y as
        parameters.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        # Explosion List, adds all 17 frames of the explosion to a list
        self.__explosions = []
        for current_frame in range(1,17):
            explosions = pygame.image.load(os.path.join("explosions","explosion" + str(current_frame) + ".png"))
            self.__explosions.append(explosions)
        # counter is created to keep track of the number of frames that have been displayed.
        self.__counter = 0       
        
        # initial image is loaded.    
        self.image = pygame.image.load(os.path.join("explosions","explosion1.png"))
        # Conversion not used to maintain transparency
        
        # explosion location is at object coords.
        self.rect = self.image.get_rect()
        self.__screen = screen
        self.rect.centery = object_y
        self.rect.centerx = object_x
        
    def update(self):
        ''' The update method cycles through all 16 frames of the explosion
        until the last frame is reached, then it kills itself'''
        if self.__counter < 16:
            self.image = self.__explosions[self.__counter]
            self.__counter += 1
        else:
            self.kill()
            
class EndZone (pygame.sprite.Sprite):
    def __init__(self, screen):
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel wide black line.
        self.__screen = screen
        self.image = pygame.Surface((self.__screen.get_width(), 30))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
class PlayerKeeper(pygame.sprite.Sprite):
    def __init__(self):
        '''This initializer loads the custom font "Captain Redemption", and
        sets the starting Player Health to 100'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting health.
        self.__font = pygame.font.Font("zombiefont.ttf", 64)
        self.__player_health = 100
        
    def player_hit(self):
        '''This method when called subtracts 10 from the players health'''
        self.__player_health -= 10
     
    def death(self):
        '''This method returns whether the player has died or not'''
        if self.__player_health <= 0:
            return True
        else:
            return False
 
    def update(self):
        '''This method will be called automatically to display 
        the current health at the bottom of the game window.'''
        message = "Player Health: %d" % (self.__player_health)
        self.image = self.__font.render(message, 1, (193, 1, 1))
        self.rect = self.image.get_rect()
        self.rect.center = (153, 498)      

class WallKeeper(pygame.sprite.Sprite):
    def __init__(self):
        '''This initializer loads the custom font "Captain Redemption", and
        sets the starting wall Health to 100'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting health.
        self.__font = pygame.font.Font("zombiefont.ttf", 64)
        self.__wall_health = 100
        
    def wall_hit(self):
        '''This method subtracts 5 from the health of the wall'''
        self.__wall_health -= 5
     
    def death(self):
        '''This method returns wheter the wall has been demolished or not'''
        if self.__wall_health <= 0:
            return True
        else:
            return False
 
    def update(self):
        '''This method will be called automatically to display 
        the current health of the wall at the bottom of the game window.'''
        message = "Wall Health: %d" % (self.__wall_health)
        self.image = self.__font.render(message, 1, (193, 1, 1))
        self.rect = self.image.get_rect()
        self.rect.center = (172, 535)     
        
class WaveKeeper(pygame.sprite.Sprite):
    def __init__(self):
        '''This initializer loads the custom font "Captain Redemption", and
        sets the starting Zombie Wave to 1'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting wave.
        self.__font = pygame.font.Font("zombiefont.ttf", 64)
        self.__wave = 1
        
    def wave_increase(self):
        '''This method adds one to the score for current wave'''
        self.__wave += 1
 
    def update(self):
        '''This method will be called automatically to display 
        the current wave at the bottom of the game window.'''
        message = "Current Wave: %d" % (self.__wave)
        self.image = self.__font.render(message, 1, (193, 1, 1))
        self.rect = self.image.get_rect()
        self.rect.center = (508, 531)

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        '''This initializer loads the custom font "Captain Redemption", and
        sets the game over message'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the game over message.
        self.__font = pygame.font.Font("zombiefont.ttf", 115)
    
        message = "GAME OVER"
        self.image = self.__font.render(message, 1, (255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (326, 245)    
 