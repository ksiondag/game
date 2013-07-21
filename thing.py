import pygame
import constants

class Thing:
    
    def __init__( self, x, y, width, height, color ):
        '''
        '''
        self.x = x
        self.y = y

        self.vel_x = 0
        self.vel_y = 0

        self.width  = width
        self.height = height

        self.color = color

    def stop( self ):
        self.vel_x = 0
        self.vel_y = 0

    def collide( self, other ):
        '''
        '''
        pass

    def update( self ):
        '''
        '''
        pass

    def display( self, screen ):
        '''
        '''
        pygame.draw.rect( screen, self.color, (self.x,     self.y, 
                                               self.width, self.height) )

class Platform( Thing ):
    pass

class Character( Thing ):
    pass

class Player( Character ):

    def __init__( self, *args, **kwargs ):
        '''
        '''
        Character.__init__( self, *args, **kwargs )
        self.grounded = False

    def move_event( self, target_location ):
        '''
        '''

        if self.grounded:
            target_x, target_y = target_location

            self.vel_x = (target_x - self.x)/15
            self.vel_y = (target_y - self.y)/10
            
            self.grounded = False

        # TODO: in-air user controls
        else:
            pass

    def collision_event( self, other ):
        # TODO: when colliding with other object, react appropriately
        pass

    def update( self ):
        '''
        '''
        self.x += self.vel_x
        self.y += self.vel_y

        if not self.grounded:
            self.vel_y += constants.GRAVITY
            self.grounded = False

        if self.x < 0:
            self.vel_x = 0
            self.x = 0
        if self.x + self.width > constants.WALL:
            self.vel_x = 0
            self.x = constants.WALL - self.width

