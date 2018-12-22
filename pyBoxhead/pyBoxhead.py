''' Name: David Ye

    Date: May 31, 2017
    
    Description: A simple zombie survival game.
    
    Special thanks to: Sean Cooper - Original Creator of Boxhead, Boxhead Logo
                     Tim Schiesser - Contributor to BoxheadPSP, Sprite Creator
   Kevin MacLeod (incompetech.com) - Composer of Background Music (The Escalation)
                       Mike Koenig - Explosion Sound Effect, Gun Sound Effects
                                     Zombie Demon Spawn (Wave Sound) Effect
                      Audio Blocks - Game Over Sound Effect, Screaming Sound Effect
     and most importantly, Mr. Rao - Support and Guidance
                      
    Change Log
    v0.1 = Background intializating, creation in photoshop.
    v0.2 = Background and boundaries properly working, Player Movement
    v0.3 = Add bullets, make sure that bullets properly shoot
    v0.4 = Add zombies, and random spawning 
    v0.5 = Add explosions that spawn when bullet/zombies collide
    v0.6 = Add collision detection; player on zombie collison; zombie on wall collision
           Bullet on zombie collision. In all cases; call explosions 
    v0.7 = Add health bars and wavekeeper. 
    v0.8 = Add Sound effects and background music 
    v0.9 = Add Introduction Screen 
    v1.0 = Final Public Beta - CURRENT STABLE BUILD
'''
# I - Import and Initialize
import pygame, pyBoxheadSprites, random
pygame.init()
pygame.mixer.init()

def intro_screen():
    ''' This function is used to display a introductory screen, creating a
    game loop before the main game loop'''
    # D - Display configuration
    pygame.display.set_caption("pyBoxhead Public Beta")
    screen = pygame.display.set_mode((638, 553))      
    
    # E - Entities      
    
    # Creates a list of joysticks
    joysticks = []
    for joystick_no in range(pygame.joystick.get_count()):
        stick = pygame.joystick.Joystick(joystick_no)
        stick.init()
        joysticks.append(stick)    
    
    # Original Background
    background = pygame.image.load("introscreen.png")
    background = background.convert()
    screen.blit(background, (0, 0))  
    
    # Begin Game Sound-Effect
    begin_game = pygame.mixer.Sound("guncock.wav")
    begin_game.set_volume(1)
    # Action (broken into ALTER steps)
    
    # A - Assign Values
    clock = pygame.time.Clock()
    keepGoing = True
    
    #L - Loop
    while keepGoing:
        
        # T - timer to set frame rate
        clock.tick(30)
        
        # E - Event Handling ; Player uses joystick only
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                return joysticks, screen, keepGoing
            if event.type == pygame.JOYHATMOTION or event.type == pygame.JOYBUTTONDOWN: 
                begin_game.play()
                return joysticks, screen, keepGoing
            
        # R - Refresh Display
        pygame.display.flip()
    
        
                
def main():
    '''This function defines the 'mainline logic' for our pyPong game.'''
    
    # The introductory screen is called. Joysticks, display configuration
    # and keepGoing state is received from the intro_screen function.
    
    joysticks, screen, keepGoing = intro_screen()
    
    # E - Entities
    
    background = pygame.image.load("boxheadbg.png")
    background = background.convert()
    screen.blit(background, (0, 0))
    
    # Background Music
    background_music = pygame.mixer.music.load("escalation.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) 
    
    # Sound Effects
    gameover_voice = pygame.mixer.Sound("gameover.wav")
    gameover_voice.set_volume(1)
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    explosion_sound.set_volume(0.8)
    gun_shot = pygame.mixer.Sound("gunshot.wav")
    gun_shot.set_volume(0.3)
    player_death = pygame.mixer.Sound("gameoverdeath.wav")
    player_death.set_volume(1)
    next_wave = pygame.mixer.Sound("waveeffect.wav")
    next_wave.set_volume(1)
    
    
    # Single appearing sprites instantiated.
    player = pyBoxheadSprites.Player(screen)
    endzone = pyBoxheadSprites.EndZone(screen)
    health_level = pyBoxheadSprites.PlayerKeeper()
    wall_level = pyBoxheadSprites.WallKeeper()
    wave_level = pyBoxheadSprites.WaveKeeper()
    game_over = pyBoxheadSprites.GameOver()
    
    #Sprite group for sprites that appear more than once are created.
    zombieGroup = pygame.sprite.Group()
    bulletGroup = pygame.sprite.Group()
    explosionGroup = pygame.sprite.Group()
    
    # Sprites that appear on the screen and do not change location are grouped together.
    stationarySprites = pygame.sprite.OrderedUpdates(endzone, health_level, wall_level, wave_level)
    allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player)
    
    # A - Action (broken into ALTER steps)

    # A - Assign values to key variables
    clock = pygame.time.Clock()
    zombies_killed = 0
    # Initial zombie spawning chance set, explained during event handling.
    spawning_chance = 50
    # Variables created to keep track whether this is the first time the player
    # has killed the pre-requisite amount of zombies required for the next wave.
    firstWaveAchievement = True
    secondWaveAchievement = True
    thirdWaveAchievement = True
    fourthWaveAchievement = True
    fifthWaveAchievement = True
    sixthWaveAchievement = True
    # keepGoing is passed from intro_screen, and is not found here.
    # if the user exits in the intro screen, main gameloop is skipped. 
    # If they decide to play, main game loop executes
    
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
  
    #  L - Loop
    while keepGoing:
         
        # T - Timer to set frame rate
        clock.tick(30)
      
        # E - Event handling, Player uses joystick only
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.JOYHATMOTION:
                # Tuple of the d-pad selection is passed to the change direction func.
                player.change_direction(event.value)
            if event.type == pygame.JOYBUTTONDOWN:  
                # If the player presses any button on the controller, a bullet
                # is created and added to the bullet list. allSprites is recreated
                # to add the bullets.
                bullet = pyBoxheadSprites.Bullet(screen, player.rect.centerx, player.rect.bottom)
                bulletGroup.add(bullet)
                allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup)
                gun_shot.play()
         
        # Zombie Spawning Mechanics Below
        # For every time the game loop refreshes, a random number is generated.
        # If the number 7 is selected, a zombie is spawned. 
        
        # To keep track of the chance of zombie spawning, every time a zombie is 
        # killed, it is tracked. The more that are killed, the more that the 
        # range is reduced, increasing zombie spawn chances.
        
        if random.randrange(1, spawning_chance) == 7:
            # Zombie x position is randomly generated to make sure that the
            # player cannot predict where the zombies spawn.
            x_pos = random.randrange(20, 620)
            zombie = pyBoxheadSprites.Zombie(screen, x_pos)
            # Zombie is added to the zombie group.
            zombieGroup.add(zombie)
            allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup)
        
        
        # Based on the number of zombies killed, the spawning range is reduced
        # and the wave increase sound effect is played, along with the
        # new wave level being displayed to the user.
        if zombies_killed == 20 and firstWaveAchievement:
            spawning_chance = 45
            wave_level.wave_increase()
            next_wave.play()
            firstWaveAchievement = False
        if zombies_killed == 35 and secondWaveAchievement:
            spawning_chance = 40
            wave_level.wave_increase()  
            next_wave.play()
            secondWaveAchievement = False
        if zombies_killed == 50 and thirdWaveAchievement:
            spawning_chance = 35
            wave_level.wave_increase()  
            next_wave.play()
            thirdWaveAchievement = False
        if zombies_killed == 75 and fourthWaveAchievement:
            spawning_chance = 30
            wave_level.wave_increase()
            next_wave.play()
            fourthWaveAchievement = False 
        if zombies_killed == 100 and fifthWaveAchievement:
            spawning_chance = 25
            wave_level.wave_increase()
            next_wave.play()
            fifthWaveAchievement = False
        if zombies_killed == 125 and sixthWaveAchievement:
            spawning_chance = 20
            wave_level.wave_increase()
            next_wave.play()
            sixthWaveAchievement = False            

        # Collision Detection (Bullet on Zombie)
        # Explosion is created at zombie location, zombie and bullet are killed.
        for bullet in bulletGroup:
            zombie_bullet_hitList = pygame.sprite.spritecollide(bullet, zombieGroup, False)
            for items in zombie_bullet_hitList:
                explosion = pyBoxheadSprites.Explosion(screen, bullet.rect.centerx, bullet.rect.centery)
                explosionGroup.add(explosion)
                allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup)
                explosion_sound.play()
                items.kill()
                bullet.kill()
                zombies_killed += 1
                
        #Collision Detection (Wall on Zombie)
        # Explosion is created at zombie location, zombie is killed.
        for zombie in zombieGroup:
            if zombie.rect.colliderect(endzone):
                explosion = pyBoxheadSprites.Explosion(screen, zombie.rect.centerx, zombie.rect.centery)
                explosionGroup.add(explosion)
                allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup)
                explosion_sound.play()
                zombie.kill()
                wall_level.wall_hit()
        
        #Collision Detection (Player on Zombie)
        # Explosion is created at zombie location, zombie is killed, player takes damage.
        for zombie in zombieGroup:
            if zombie.rect.colliderect(player):
                explosion = pyBoxheadSprites.Explosion(screen, zombie.rect.centerx, zombie.rect.centery)
                explosionGroup.add(explosion)
                allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup)
                explosion_sound.play()
                zombie.kill()  
                health_level.player_hit()
                
        # If the health_level meets the death condition, explosion is created
        # at player location, kill the player, play player death sound effect,
        # stop the main game loop.
        if health_level.death():
            explosion = pyBoxheadSprites.Explosion(screen, player.rect.centerx, player.rect.centery)
            explosionGroup.add(explosion)
            # This time when rebuilding allsprites, add game_over sprite.
            allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup, game_over)
            player_death.play()
            player.kill()
            keepGoing = False
        
        # If the wall_level meets the death condition, add game_over sprites 
        # when rebuilding all sprites, play game over sound effect, stop main game loop.
            allSprites = pygame.sprite.OrderedUpdates(stationarySprites, player, zombieGroup, bulletGroup, explosionGroup, game_over)  
            gameover_voice.play()
            keepGoing = False            
                
        
        # R - Refresh display
        # Background must be blitted because of layering issues
        screen.blit(background, (0, 0))
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)       
        pygame.display.flip()
        
          
     # Unhide the mouse pointer
    pygame.mouse.set_visible(True)
  
     # Close the game window, fade out music
    pygame.mixer.music.fadeout(3000) 
    pygame.time.delay(3000)
    pygame.quit()     
      
 # Call the main function
main()