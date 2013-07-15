import pygame
import constants

class Thing:
    
    def __init__( self, x, y, width, height, color ):
        '''
        '''
        self.pos_x = x
        self.pos_y = y

        self.vel_x = 0
        self.vel_y = 0

        self.width  = width
        self.height = height

        self.color = color

    def collision_event( self, other ):
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
        pygame.draw.rect( screen, self.color, (self.pos_x, self.pos_y, 
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

            self.vel_x = (target_x - self.pos_x)/15
            self.vel_y = (target_y - self.pos_y)/10

        # TODO: in-air user controls
        else:
            pass

    def collision_event( self, other ):
        # TODO: when colliding with other object, react appropriately
        pass

    def update( self ):
        '''
        '''
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        if self.pos_y + self.height < constants.GROUND:
            self.vel_y += constants.GRAVITY
            self.grounded = False
        else:
            self.vel_x = 0
            self.vel_y = 0

            self.pos_y = constants.GROUND - self.height

            self.tar_x = self.pos_x
            self.tar_y = self.pos_y

            self.grounded = True
        
        if self.pos_x < 0:
            self.vel_x = 0
            self.pos_x = 0
        if self.pos_x + self.width > constants.WALL:
            self.vel_x = 0
            self.pos_x = constants.WALL - self.width

