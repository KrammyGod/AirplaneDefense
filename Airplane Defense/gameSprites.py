'''

By: Mark Xue

Date: May 1, 2019

Description: This is a tower defense game module

For the complete verison (v2.0.0)

'''

import pygame
import random
import math

class Player(pygame.sprite.Sprite):
    '''
    This class defines the sprite for the player
    '''
    def __init__(self, screen):
        '''
        This initializer takes a screen surface as a parameter.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Loading the full turret and empty turret to have an animation.
        self.fullTurret = pygame.image.load('images/turret.png').convert_alpha()
        self.emptyTurret = pygame.image.load('images/emptyTurret.png').convert_alpha()

        
        # Load ready image and get rect attributes
        self.image = self.fullTurret
        self.original_image = self.image
        self.rect = self.image.get_rect()
        
        # 60 pixels right of endzone and centered.
        self.rect.left = 60
        self.rect.centery = screen.get_height() // 2
        
        self.screen = screen
    
    def rotate(self, xy_pos):
        '''
        This method will rotate the image based off the mouse's position.
        The arguements required are the mouse's x and y position
        This method is the same as the projectile's rotate method.
        '''
        # Get the x and y position from the tuple
        x_pos, y_pos = xy_pos
        
        x_distance = x_pos-self.rect.centerx
        y_distance = self.rect.centery-y_pos
        
        # Used to keep the image in its position.
        original_center = self.rect.center
        
        # Unknown reason why, but when x is negative, y_distance must flip
        # to get the correct image.
        if x_distance < 0:
            # Inverse tan of y/x
            rotate_degrees = math.atan(-y_distance / x_distance)
            # Convert to degrees
            rotate_degrees = math.degrees(rotate_degrees)
            rotate_degrees = 180-rotate_degrees
            
        # Error trapping ZeroDivisionError
        elif x_distance == 0:
            if y_distance > 0:
                rotate_degrees = 90
            else:
                rotate_degrees = -90
        
        # If x_position is positive
        else:
            # Inverse tan of y/x
            rotate_degrees = math.atan(y_distance/x_distance)
            # Convert to degrees
            rotate_degrees = math.degrees(rotate_degrees)
        
        # Rotate image based off degrees given
        self.image = pygame.transform.rotate(self.original_image, rotate_degrees)
        
        # Get new rect but keep position
        self.rect = self.image.get_rect()
        self.rect.center = original_center
    
    def shoot(self):
        '''
        This method changes the image to the empty turret after it shoots a
        missile.
        '''
        self.image = self.emptyTurret
        self.original_image = self.image
    
    def reload(self):
        '''
        This method reloads the turret after the missile is back and puts the
        first image back to self.image.
        '''
        self.image = self.fullTurret
        self.original_image = self.image
        
    def move(self, y_direction):
        '''
        This method will be called to move the player 5 pixels (when the key
        is pressed down)
        '''
        self.rect.centery += y_direction
    
    def update(self):
        '''
        This method will check to make sure the player doesn't go off screen.
        '''
        if self.rect.top <= 60:
            self.rect.top = 65
        if self.rect.bottom >= self.screen.get_height() - 10:
            self.rect.bottom = self.screen.get_height() - 15
            
class Plane(pygame.sprite.Sprite):
    '''
    This class defines a plane sprite for the enemies trying to get to the
    left endzone.
    '''
    def __init__(self, screen, xy_pos, x_speed, y_speed):
        '''
        This initializer method takes 2 parameters:
        screen : the pygame surface object that will be used to make sure the 
                 plane only moves after it passes the right side of the screen.
        xy_pos : a tuple that defines the center of the plane.
        x_speed : defines self.dx (speed it moves at depending on the wave).
        y_speed : defines self.dy (up and down bouncing for harder levels).
        '''
        # Call the parent __init__() method.
        pygame.sprite.Sprite.__init__(self)
        
        # Load the image
        planes = [pygame.image.load('images/plane1.png').convert_alpha(), \
                  pygame.image.load('images/plane2.png').convert_alpha()]
        self.image = planes[random.randrange(2)]
        self.rect = self.image.get_rect()
        
        self.rect.center = xy_pos
        
        self.dx = x_speed
        self.dy = y_speed
        
        self.screen = screen
        
    def change_directionY(self):
        '''
        This method reverses the y direction when it hits the top or bottom
        endzone.
        '''
        self.dy = -self.dy
        self.rect.centery -= self.dy
        
    def update(self):
        '''
        This method will be automatically called to update the position
        of the plane.
        '''
        self.rect.centerx -= self.dx
        # Make sure only change y direction if passed right side of screen.
        if self.rect.left < self.screen.get_width():
            self.rect.centery -= self.dy
            
class Crosshair(pygame.sprite.Sprite):
    '''
    This class defines a crosshair sprite for the mouse's position.
    '''
    def __init__(self):
        '''
        This initializer method does not take any parameters.
        '''
        # Call the parent __init__() method.
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('images/crosshair.png').convert_alpha()
        self.rect = self.image.get_rect()
    
    def set_position(self, xy_pos):
        '''
        This method changes the position of the crosshair depending on the
        position of the mouse.
        '''
        self.rect.center = xy_pos
    
class Projectile(pygame.sprite.Sprite):
    '''
    This class defines the projectile sprite for the game.
    '''
    def __init__(self, screen, xy_pos):
        '''
        This initializer takes the screen and xy_pos as a parameter.
        xy_pos is the centerx and centery tuple that determines where the 
        projectile starts.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load the projectile.
        self.image = pygame.image.load('images/missile.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        self.dx = 20
        
        # Set starting position
        self.rect.center = xy_pos
        
        # Save original image to rotate
        self.original_image = self.image
        
        # Save the screen as an instance variable for rotation purposes
        self.screen = screen
        
    def set_position(self, xy_pos):
        '''
        This method changes the starting position of the missile.
        '''
        self.rect.center = xy_pos
        
    def set_speed(self, xy_pos):
        '''
        This method will define self.dy and possibly modify self.dx to move the 
        projectile.
        '''
        # Get x and y position from the tuple.
        x_pos, y_pos = xy_pos
        
        # Here we will be using y=mx+b equation. b is not needed since b is 
        # always the starting value, 0.
        distance_x = (x_pos - self.rect.centerx)
        distance_y = (y_pos - self.rect.centery)
        
        try:
            # The slope cannot account for distance x's direction, only y.
            slope = distance_y/abs(distance_x)
        except ZeroDivisionError:
            # If distance_x is 0, then dx should be 0 and only dy should be moving.
            if distance_y < 0:
                self.dy = -20
                self.dx = 0
            else:
                self.dy = 20
                self.dx = 0
            return
        
        # If the speed is higher than 20, then make the speed a maximum of 20.
        if slope * self.dx >= 20:
            self.dx = 20 / slope
        elif slope * self.dx <= -20:
            self.dx = -20 / slope
            
        # y = slope * x, y=mx
        self.dy = slope*self.dx
        
        # distance_x negative means dx must be negative (but cannot affect the
        # y=mx equation so its put after).
        if distance_x < 0:
            self.dx = -self.dx
        
    def rotate(self, xy_pos):
        '''
        This method rotates the picture to the correct direction the projectile
        is going in.
        '''
        '''
        This next snippet is slightly complicated, but it uses trigonometry to
        find the angle from the projectile to the mouse.
        tanA = opp/hypo, Therefore tanA = y_distance/x_distance
        '''
        # Get the x and y position from the tuple
        x_pos, y_pos = xy_pos
        
        x_distance = x_pos-self.rect.centerx
        y_distance = self.rect.centery-y_pos
        
        # Get original center to keep image in same place.
        original_center = self.rect.center
        
        # Unknown reason why, but when x is negative, y_distance must flip
        # to get the correct image.
        if x_distance < 0:
            # Inverse tan of y/x
            rotate_degrees = math.atan(-y_distance / x_distance)
            # Convert to degrees
            rotate_degrees = math.degrees(rotate_degrees)
            rotate_degrees = 180-rotate_degrees
            
        # Error trapping ZeroDivisionError
        elif x_distance == 0:
            if y_distance > 0:
                rotate_degrees = 90
            else:
                rotate_degrees = -90
        
        # If x_position is positive
        else:
            # Inverse tan of y/x
            rotate_degrees = math.atan(y_distance/x_distance)
            # Convert to degrees
            rotate_degrees = math.degrees(rotate_degrees)
        
        # Rotate image based off degrees given
        self.image = pygame.transform.rotate(self.original_image, rotate_degrees)
        
        # Get new rect but keep original position
        self.rect = self.image.get_rect()
        self.rect.center = original_center
        
    def update(self):
        '''
        This method will be called automatically to make the projectile move 
        forward.
        '''
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
class Explosion(pygame.sprite.Sprite):
    '''
    This class defines an explosion sprite that appears when the missile
    hits a plane or an endzone.
    '''
    def __init__(self, xy_pos, explosionType):
        '''
        This initializer method takes in xy_pos as a parameter to determine
        where the explosion appears
        explosionType : 0 or 1 defining which type of explosion it is
        0 being the missile on plane explosion
        1 being plane on left endzone explosion
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        if not explosionType:
            for i in range(23):
                self.images.append(pygame.image.load(f'images/explosions/Explosion{i}.gif').convert_alpha())
        else:
            for i in range(17):
                self.images.append(pygame.image.load(f'images/planeEffects/effect{i}.png').convert_alpha())            
        self.imageNum = 0
        
        self.image = self.images[self.imageNum]
        self.rect = self.image.get_rect()
        self.rect.center = xy_pos
        
    def update(self):
        '''
        This method will be automatically called to self destruct after explosion
        ends.
        '''
        self.image = self.images[self.imageNum]
        self.imageNum += 1
        if self.imageNum == len(self.images):
            self.kill()
            
class EndZone(pygame.sprite.Sprite):
    '''
    This class defines an endzone sprite that will be used around the window to
    detect if anything goes off the screen.
    '''
    def __init__(self, screen, x_coord, y_coord, horizontal):
        '''
        This initializer takes in 4 parameters
        screen : the pygame.Surface object used to get width and height
        x_coord : the left side x coordinate to make the endzone
        y_coord : the top side y coordinate to make the endzonw
        horizontal : a bool value, True means its the top or bottom, False means
                     left or right
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Create the endzone Surface object
        if horizontal:
            # Make this 30 pixels to prevent explosions from touching the 
            # scorekeeper label.
            self.image = pygame.Surface((screen.get_width(), 50))
        else:
            self.image = pygame.Surface((screen.get_width(), screen.get_height()))
        
        self.image = self.image.convert()
        
        self.rect = self.image.get_rect()
        
        # Set the endzone to the given coordinates
        self.rect.left = x_coord
        self.rect.top = y_coord

class ScoreKeeper(pygame.sprite.Sprite):
    '''
    This class defines a label sprite to display the score.
    '''
    def __init__(self, screen):
        '''
        This initializer loads the font "Star Jedi Rounded", and
        sets the starting score to 0
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score.
        self.font = pygame.font.Font("fonts/font.ttf", 30)
        self.score = 0
        self.lives = 20
        self.wave = 0
        
        # Number of spaces between each value
        self.spaces = 7
        
        self.screen = screen
        
    def add_score(self, value):
        '''
        This method adds a score for the player when a plane dies.
        The value parameter is the score they gain.
        This method will only be called if the plane dies to a missile or by
        hitting the player.
        '''
        self.score += value
        
    def subtract_life(self):
        '''
        This method subtracts a life from the player.
        '''
        self.lives -= 1
        
    def add_wave(self):
        '''
        This method adds a wave when called.
        '''
        self.wave += 1
        
    def check_lose(self):
        '''
        This method returns a bool value whether the player has lost all their
        lives or not.
        '''
        return self.lives == 0
 
    def update(self):
        '''
        This method will be called automatically to display the current score,
        wave, and lives at the top of the game window
        '''
        messages = [f"Lives:{self.lives}", f"Wave:{self.wave}", f"Score:{self.score}"]
        spaces = ' '*self.spaces
        message = spaces.join(messages)
        self.image = self.font.render(message, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.screen.get_width()/2, 15)
        if self.rect.left < 0:
            self.spaces -= 1
        elif self.rect.right > self.screen.get_width():
            self.spaces -= 1
            
class WaveLabel(pygame.sprite.Sprite):
    '''
    This class defines the large 'wave' label that appears every wave.
    '''
    def __init__(self, wave):
        '''
        This initializer takes the wave number as a parameter.
        '''
        # Call the parent __init__() function
        pygame.sprite.Sprite.__init__(self)
        
        self.font = pygame.font.Font('fonts/font.ttf', 100)
        
        self.image = self.font.render(f'Wave {wave}', True, (0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 110
        self.rect.top = 150
        
        # Used to add a wave number.
        self.wave = wave
        
    def add_wave(self):
        '''
        This method adds one to the wave number.
        '''
        self.wave += 1
        self.image = self.font.render(f'Wave {self.wave}', True, (0, 255, 255))
        
class Label(pygame.sprite.Sprite):
    '''
    This class defines a label sprite used to display text on start and end menu.
    '''
    def __init__(self, text, size, center=(0, 0), left=0, top=0):
        '''
        This initializer method takes 4 parameters
        center : (x, y) tuple that defines the center of the label
        text : the string to be displayed
        size : an integer representing the text size
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.font = pygame.font.Font('fonts/font.ttf', size)
        self.text = text
        self.image = self.font.render(text, True, (0, 255, 255))
        self.rect = self.image.get_rect()
        if left and top:
            self.rect.left = left
            self.rect.top = top
        elif center:
            self.rect.center = center
        
    def change_text(self, text):
        '''
        This method changes the label's text.
        '''
        self.image = self.font.render(text, True, (0, 255, 255))
        self.text = text
