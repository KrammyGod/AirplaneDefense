'''

By: Mark Xue

Date: May 3, 2019

Description: This program is a tower defense game.


AIRPLANE DEFENSE V2.0.0
------------------------------------------------------------------------------
This is a tower defense inspired game:
The goal of the game is to survive as many waves of airplanes as possible, 
with each wave having increasing speed, and reach the highest score possible.

How to play this game:

Controls:
W, S, Q, and mouse control

Pressing down W moves your player up and S moves it down.
Use your mouse to move the cursor and left click to shoot down the airplanes 
trying to reach the left side (your tower).
Press Q anytime during the game to pause the game. 
Left click anywhere or press Q again to unpause.

If the planes hit your tank they will also die

If the planes reach your tower, they will blow up and you will lose a life.

You have a total of 20 lives.

Scoring:
10 points will be awarded for every hit with the missile
5 points if you kill them with your tank
No points will be rewarded if they blow up when hitting the tower.

'''
             
# I - Import and Initialize
import pygame
import gameSprites
import random
import os
pygame.init()

#Center screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

def instructionsScreen(crosshair, screen):
    '''
    This function is used to display the instructions picture to teach the user
    how to play the game.
    '''
    controls = pygame.image.load('images/instructions.png')
    group = pygame.sprite.Group(crosshair)
    keepGoing = True
    pygame.mouse.set_visible(False)
    
    while keepGoing:
        xy_position = pygame.mouse.get_pos()
        crosshair.set_position(xy_position)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            # Exit when user left clicks
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                keepGoing = False
            
        screen.blit(controls, (0, 0))
        group.draw(screen)
        pygame.display.flip()
        
def pauseScreen(crosshair, screen, background):
    '''
    This function is used to pause the game
    '''
    click = gameSprites.Label("left click anywhere to continue", 30, center=(screen.get_width()/2, 20))
    # Change into picture and fade in+out
    pause = pygame.image.load('images/pause.png').convert()
    group = pygame.sprite.OrderedUpdates(click, crosshair)
    keepGoing = True
    screen.blit(background, (0, 0))
    alpha = 255
    add = -5
    
    # Assign key variables
    clock = pygame.time.Clock()    
    
    while keepGoing:
        # 30 frames loaded per second
        clock.tick(30)
        xy_position = pygame.mouse.get_pos()
        crosshair.set_position(xy_position)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click.kill()
                keepGoing = False
            # Exit when user left clicks
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                click.kill()
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    click.kill()
                    keepGoing = False
                    
        pause.set_alpha(alpha)
        alpha += add
        if alpha <= 0:
            add = 5
        elif alpha >= 255:
            add = -5
        screen.blit(background, (0, 0))
        screen.blit(pause, (8, screen.get_height()//2-39))
        group.draw(screen)
        pygame.display.flip()

def startMenu():
    '''
    This function is the start menu of the game.
    '''
    # Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Airplane Defense')
    
    # Entities
    background = pygame.image.load('images/background.png').convert()
    # Save rect attributes to check for mouse on buttons collision
    startButton = pygame.draw.rect(background, (0, 255, 255), (349, 165, 105, 25), 1)
    hacksToggle = pygame.draw.rect(background, (0, 255, 255), (349, 265, 200, 25), 1)
    controlsButton = pygame.draw.rect(background, (0, 255, 255), (349, 215, 180, 25), 1)
    screen.blit(background, (0, 0))
    
    pygame.mixer.music.load('sounds/musicEarth.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)    
    
    '''
    For all the correct comments, these are just copy and pasted code from
    the game function.
    '''
    # Load same things for training grounds before game starts
    leftEndzone = gameSprites.EndZone(screen, -screen.get_width(), 0, False)
    rightEndzone = gameSprites.EndZone(screen, screen.get_width(), 0, False)
    topEndzone = gameSprites.EndZone(screen, 0, 0, True)
    bottomEndzone = gameSprites.EndZone(screen, 0, screen.get_height(), True)
    scoreKeeper = gameSprites.ScoreKeeper(screen)
    player = gameSprites.Player(screen)
    missile = gameSprites.Projectile(screen, (-30, 10))
    crosshair = gameSprites.Crosshair()
    # Preload explosion effects so it doesn't lag when actual explosion comes
    explosionTemp = gameSprites.Explosion((0, 0), 0)
    del explosionTemp
    explosionTemp = gameSprites.Explosion((0, 0), 1)
    del explosionTemp
    missileSprites = pygame.sprite.Group()
    endzoneSprites = pygame.sprite.Group(leftEndzone, rightEndzone, topEndzone,\
                                         bottomEndzone)
        
    # Start button and border definitions
    start = gameSprites.Label('start', 30, left=350, top=150)
    startBorderx = range(startButton.left, startButton.right + 1)
    startBordery = range(startButton.top, startButton.bottom + 1)
    # Control instruction button and border definitions
    controls = gameSprites.Label('controls', 30, left=350, top=200)
    controlsBorderx = range(controlsButton.left, controlsButton.right + 1)
    controlsBordery = range(controlsButton.top, controlsButton.bottom + 1)
    # Hack toggle and border definitions
    hack = gameSprites.Label('Hacks: off', 30, left=350, top=250)
    hackBorderx = range(hacksToggle.left, hacksToggle.right + 1)
    hackBordery = range(hacksToggle.top, hacksToggle.bottom + 1)
    title = gameSprites.Label('List of highscores:', 30, left=120, top=70)
    
    # Check highscore file for list of highscores
    y_pos = 100
    highscores = []    
    try:
        file = open('highscores.txt', 'r')
        # pygame.font.render does not aceept \n so it must be done manually.
        for line in file:
            highscores.append(gameSprites.Label(line.strip(), 30, left=120, top=y_pos))
            y_pos += 30
            if y_pos == 370:
                break
        file.close()
    except FileNotFoundError:
        highscores = gameSprites.Label('You deleted highscores.txt :(', 20, left=120, top=100)
        
        
    allSprites = pygame.sprite.OrderedUpdates(highscores, start, title, hack,\
                                              controls, player, crosshair,\
                                              scoreKeeper)        
    
    # ACTION
    
    # Assign key variables
    clock = pygame.time.Clock()
    
    # Hacks is computer playing the game.
    hacks = False
    moved = False
    keepGoing = True
    reload = 15
    pygame.mouse.set_visible(False)
    xy_position = pygame.mouse.get_pos()
    
    # Loop
    while keepGoing:
        
        # Time
        clock.tick(30)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, hacks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    # Check if player clicks start
                    if xy_position[0] in startBorderx and xy_position[1] in startBordery:
                        return True, hacks
                    # Check if player clicks instructions button
                    if xy_position[0] in controlsBorderx and xy_position[1] in controlsBordery:
                        instructionsScreen(crosshair, screen)
                        screen.blit(background, (0, 0))
                        break
                    # Check if player toggles hacks
                    if xy_position[0] in hackBorderx and xy_position[1] in hackBordery:
                        if hacks:
                            hack.change_text('Hacks: off')
                            pygame.mixer.music.set_volume(0.3)
                            hacks = False
                        else:
                            hack.change_text('Hacks: on')
                            pygame.mixer.music.set_volume(0)
                            hacks = True
        
        # Player movement        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(-10)
        if keys[pygame.K_s]:
            player.move(10)        
            
        xy_position = pygame.mouse.get_pos()
        crosshair.set_position(xy_position)
        
        # Shoot a missile
        if pygame.mouse.get_pressed()[0] and not moved:
            player.shoot()
            missile = gameSprites.Projectile(screen, player.rect.center)
            missile.set_speed(xy_position)
            missile.rotate(xy_position)
            allSprites.add(missile)
            missileSprites.add(missile)
            moved = True
        
        # Check for collision of missile with endzone    
        collision = pygame.sprite.groupcollide(missileSprites, endzoneSprites, True, False)
        if collision:
            missile = list(collision)[0]
            explosion = gameSprites.Explosion(missile.rect.center, 0)
            allSprites.add(explosion)
            missile.kill()
            
        # Set up reload speed
        if moved:
            reload -= 1
            if reload == 0:
                moved = False
                player.reload()
                reload = 15
        player.rotate(xy_position)
        
        # Refresh display       
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)         
        pygame.display.flip()

def gameOver(scoreKeeper):
    '''
    This function is the endgame screen.
    '''
    # Display
    screen = pygame.display.set_mode((640, 480))    
    pygame.display.set_caption("Airplane Defense")
    
    # Entities
    background = pygame.image.load('images/background.png').convert()
    # Save rect attributes to check for collision with mouse on button
    button = pygame.draw.rect(background, (0, 255, 255), (220, 395, 160, 25), 1)
    screen.blit(background, (0, 0))
    
    crosshair = gameSprites.Crosshair()
    
    highscores = []
    try:
        file = open('highscores.txt', 'r')
        for line in file:
            # Slice the position so it only contains the score and append it to
            # highscores list
            highscores.append(int(line[3:]))
        highscores.append(scoreKeeper.score)
        # Create a new list that orders the new highscores.
        newHighscores = []
        for i in range(len(highscores)):
            high = max(highscores)
            newHighscores.append(high)
            highscores.remove(high)
        file.close()
        # Overwrite to make new highscores.
        file = open('highscores.txt', 'w')
        placement = 1
        for highscore in newHighscores:
            file.write(f'{placement}. {highscore}\n')
            placement += 1
            if placement == 10:
                break
    except FileNotFoundError:
        # Create new highscores.txt file if it doesn't exsist.
        file = open('highscores.txt', 'w')
        file.write(f'1. {scoreKeeper.score}\n')
        for i in range(2, 10):
            file.write(f'{i}. 0\n')
    file.close()
    
    labelBorderx = range(button.left, button.right + 1)
    labelBordery = range(button.top, button.bottom + 1)
    
    label1 = gameSprites.Label('game over!', 90, center=(screen.get_width()/2, 160))
    label2 = gameSprites.Label('your score has been recorded', 30, left=25, top=220)
    label3 = gameSprites.Label('continue', 30, left=220, top=380)
    label4 = gameSprites.Label(f'Score: {scoreKeeper.score} Wave: {scoreKeeper.wave}', 30, center=(screen.get_width()/2, 305))
    allSprites = pygame.sprite.OrderedUpdates(label1, label2, label3, label4, crosshair)
    
    # ACTION
    # Assign key variables
    clock = pygame.time.Clock()
    
    # Loop
    while True:
        # Timer to set frame rate
        clock.tick(30)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        # If the mouse click is on the label
        xy_position = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if xy_position[0] in labelBorderx and xy_position[1] in labelBordery:
                return
            
        crosshair.set_position(xy_position)
        
        # Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

def game(hacks):
    '''
    This function is the game loop.
    '''
    # Display
    screen = pygame.display.set_mode((640, 480))    
    pygame.display.set_caption("Airplane Defense")
     
    # Entities
    background = pygame.image.load('images/background.png').convert()
    screen.blit(background, (0, 0))
    
    pygame.mixer.music.load('sounds/musicLife.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)    
    
    missileExplosionSound = pygame.mixer.Sound('sounds/explosion.wav')
    missileExplosionSound.set_volume(0.3)
    
    planeExplosionSound = pygame.mixer.Sound('sounds/ono.wav')
    
    # Set up endzones that are outside of the screen.
    leftEndzone = gameSprites.EndZone(screen, -screen.get_width(), 0, False)
    rightEndzone = gameSprites.EndZone(screen, screen.get_width(), 0, False)
    topEndzone = gameSprites.EndZone(screen, 0, 0, True)
    bottomEndzone = gameSprites.EndZone(screen, 0, screen.get_height(), True)
    
    player = gameSprites.Player(screen)
    
    missile = gameSprites.Projectile(screen, (-30, 10))
    
    crosshair = gameSprites.Crosshair()
    
    scoreKeeper = gameSprites.ScoreKeeper(screen)
    
    waveLabel = gameSprites.WaveLabel(scoreKeeper.wave+1)  
    
    # Missile sprite group to check for all missiles on the screen.
    missileSprites = pygame.sprite.Group()
    
    # Endzone group to check for collision
    endzoneSprites = pygame.sprite.Group(leftEndzone, rightEndzone, topEndzone,\
                                         bottomEndzone)
    
    # Plane group to check for collision
    planeSprites = pygame.sprite.Group()
    
    # Add them to allSprites group to display.
    allSprites = pygame.sprite.LayeredUpdates(player, crosshair, scoreKeeper)
    
    # ACTION

    # Assign
    # This variable is used to make sure it only takes the position of the first
    # mouse click.
    moved = False
    
    clock = pygame.time.Clock()
    keepGoing = True
    
    # speed_up modifies the speed of the plane as the wave increases
    speed_up = 0
    # Time gives a 2 second pause before starting the next wave.
    timer = 60
    # Add planes (in increments of 100) by increasing the x coord range 
    increase_plane = 0
    
    # This sets up the reload speed for the rocket (15 frames = 0.5 seconds)
    reload = 15
    
    # Hide the mouse cursor to display crosshair.
    pygame.mouse.set_visible(False)
 
    # Loop
    while keepGoing:
     
        # Time
        clock.tick(30)
     
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pauseScreen(crosshair, screen, background)
                    screen.blit(background, (0, 0))

        # Get coordinates of mouse to later use to rotate player and missile
        xy_position = pygame.mouse.get_pos()
        
        if hacks:
            # Auto move
            if planeSprites:
                if abs(planeSprites.sprites()[0].rect.centery - player.rect.centery) < 10:
                    pass
                elif planeSprites.sprites()[0].rect.centery - player.rect.centery > 0:
                    player.move(10)
                elif planeSprites.sprites()[0].rect.centery - player.rect.centery < 0:
                    player.move(-10)
        else:
            # Move player using keys W and S
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.move(-10)
            if keys[pygame.K_s]:
                player.move(10)
        
        # Set position of crosshair
        crosshair.set_position(xy_position)
        
        if hacks:
            # Shoot missile whenever possible with hacks on
            if not moved:
                # Auto aim enabled
                # Set up missile sprite.
                if planeSprites:
                    missile = gameSprites.Projectile(screen, player.rect.center)
                    # Make cpu smarter by moving towards the closest plane but 
                    # shooting at the further plane
                    if len(planeSprites) >= 2 and abs(planeSprites.sprites()[0].rect.centery - player.rect.centery) > 25:
                        missile.set_speed(planeSprites.sprites()[1].rect.center)
                        missile.rotate(planeSprites.sprites()[1].rect.center)
                    else:
                        missile.set_speed(planeSprites.sprites()[0].rect.center)
                        missile.rotate(planeSprites.sprites()[0].rect.center)
                    # Change player image to already shot.
                    player.shoot()            
                    # Add the missile sprite to display + update
                    allSprites.add(missile)
                    missileSprites.add(missile)
                    
                    moved = True            
        else:
            # Check if mouse click to shoot missile.
            if pygame.mouse.get_pressed()[0] and not moved:
                # Change player image to already shot.
                player.shoot()
                
                # Set up missile sprite.
                missile = gameSprites.Projectile(screen, player.rect.center)
                missile.set_speed(xy_position)
                missile.rotate(xy_position)
                
                # Add the missile sprite to display + update
                allSprites.add(missile)
                missileSprites.add(missile)
                
                moved = True
            
        # Check for collision of missile with planes.
        collision = pygame.sprite.groupcollide(missileSprites, planeSprites, False, False)
        if collision:
            for plane in list(collision.values())[0]:
                scoreKeeper.add_score(10)
                # Kill each plane.
                plane.kill()
                
                missileExplosionSound.play()
                explosion = gameSprites.Explosion(plane.rect.center, 0)
                allSprites.add(explosion)
            # Take the first key of the dictionary (the missile) and kill it
            missile = list(collision)[0]
            missile.kill()
            missile.set_position((-30, 10))
        
        # Check for collision of player with planes.
        collision = pygame.sprite.spritecollide(player, planeSprites, False)
        if collision:
            for plane in collision:
                scoreKeeper.add_score(5)
                # Kill each plane sprite.
                plane.kill()
                
                missileExplosionSound.play()
                explosion = gameSprites.Explosion(plane.rect.center, 0)
                allSprites.add(explosion)
            
        # Check for collision of planes with left endzone
        collision = pygame.sprite.spritecollide(leftEndzone, planeSprites, False)
        for plane in collision:
            # Subtract life from player
            scoreKeeper.subtract_life()
            
            # Kill each plane sprite.
            plane.kill()
            
            planeExplosionSound.play()
            explosion = gameSprites.Explosion(plane.rect.center, 1)
            allSprites.add(explosion)
        
        # Check for collision of planes with top endzone
        collision = pygame.sprite.spritecollide(topEndzone, planeSprites, False)
        for plane in collision:
            # Reverse y-direction of plane.
            plane.change_directionY()
            
        # Check for collision of planes with bottom endzone
        collision = pygame.sprite.spritecollide(bottomEndzone, planeSprites, False)
        for plane in collision:
            # Reverse y-direction of plane.
            plane.change_directionY()
            
        # Check for collision of missile with endzone
        collision = pygame.sprite.groupcollide(missileSprites, endzoneSprites, True, False)
        if collision:
            # Get the missile object that collided with the endzone
            missile = list(collision)[0]
            
            missileExplosionSound.play()
            explosion = gameSprites.Explosion(missile.rect.center, 0)
            allSprites.add(explosion)
            
            missile.kill()
            
        # If all planes are destroyed, one wave is completed
        if not planeSprites:
            timer -= 1
            allSprites.add(waveLabel)
            allSprites.move_to_front(waveLabel)
            # If 2 seconds are up.
            if not timer:
                waveLabel.kill()
                # Add one to wave number
                scoreKeeper.add_wave()
                waveLabel.add_wave()
                
                wave = []
                for x in range(screen.get_width(), screen.get_width()+1000+\
                               increase_plane*50, 100):
                    # Make the planes bounce up and down after it reaches third
                    # wave
                    if scoreKeeper.wave >= 3:
                        bounce = random.randint(-3, 3)
                    else:
                        bounce = 0
                    # Generate random spawning y-coordinates
                    y = random.randint(75, screen.get_height() - 25)
                    wave.append(gameSprites.Plane(screen, (x, y), 5+speed_up//2, bounce))
                speed_up += 1
                increase_plane += 1
                
                # Set maximum speed up 
                if speed_up > 10:
                    speed_up = 10
                    
                # Add the waves to respective sprite groups
                planeSprites.add(wave)
                allSprites.add(wave)
                # Reset timer.
                timer = 60
        
        # Set up reload speed.
        if moved:
            reload -= 1
            if reload == 0:
                moved = False
                player.reload()
                reload = 15
                
        if scoreKeeper.check_lose():
            keepGoing = False
            
        if hacks:
            # Auto aim player rotation
            if planeSprites:
                if len(planeSprites) >= 2 and abs(planeSprites.sprites()[0].rect.centery - player.rect.centery) > 25:
                    player.rotate(planeSprites.sprites()[1].rect.center)
                else:
                    player.rotate(planeSprites.sprites()[0].rect.center)
        else:
            # Get x and y coordinates of mouse to rotate turret in correct direction 
            player.rotate(xy_position)
                    
        # Refresh screen
        allSprites.clear(screen, background)
        screen.blit(background, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

        if not moved:
            pygame.draw.line(screen, (220, 220, 220), player.rect.center, xy_position)
        
    return scoreKeeper

def main():
    '''
    This function defines the 'mainline logic' for the game.
    '''
    keepGoing = True
    while keepGoing:
        keepGoing, hacks = startMenu()
        
        if keepGoing:
            scoreKeeper = game(hacks)
            # Make sure only record score if it is greater than 0
            if scoreKeeper.score:
                gameOver(scoreKeeper)
    
    # Close the game window
    pygame.quit()    
         
# Call the main function
main()
