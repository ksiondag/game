import pygame
import sys

import constants
import physics

class Thing( pygame.rect.Rect ):
    
    def __init__( self, left, top, width, height, color ):
        '''
        '''
        #left, top = physics.location_meters_to_pixels( left, top )
        #width = physics.meters_to_pixels( width )
        #height = physics.meters_to_pixels( height )

        pygame.rect.Rect.__init__( self, left, top, width, height )

        self.color = color
        self.stop()

    _left = pygame.rect.Rect.left
    _right = pygame.rect.Rect.right
    _top = pygame.rect.Rect.top
    _bottom = pygame.rect.Rect.bottom
    
    _x = pygame.rect.Rect.x
    _y = pygame.rect.Rect.y

    @property
    def left( self ):
        #return pixels_to_meters( self._left )
        return physics.pixels_to_meters( self._left )

    @left.setter
    def left( self, value ):
        self._left = physics.meters_to_pixels( value )

    @property
    def right( self ):
        #return pixels_to_meters( self._right )
        return physics.pixels_to_meters( self._right )

    @right.setter
    def right( self, value ):
        self._right = physics.meters_to_pixels( value )

    @property
    def x( self ):
        return physics.pixels_to_meters( self._x )

    @x.setter
    def x( self, value ):
        self._x = physics.meters_to_pixels( value )

    @property
    def top( self ):
        return physics.vertical_pixels_to_meters( self._top )

    @top.setter
    def top( self, value ):
        self._top = physics.vertical_meters_to_pixels( value )

    @property
    def bottom( self ):
        return physics.vertical_pixels_to_meters( self._bottom )

    @bottom.setter
    def bottom( self, value ):
        self._bottom = physics.vertical_meters_to_pixels( value )

    @property
    def y( self ):
        return physics.vertical_pixels_to_meters( self._y )

    @y.setter
    def y( self, value ):
        self._y = physics.vertical_meters_to_pixels( value )

    def stop( self ):
        self.stop_x()
        self.stop_y()

    def stop_x( self ):
        self.vel_x = 0

    def stop_y( self ):
        self.vel_y = 0

    def falling( self ):
        return self.vel_y < 0

    def rising( self ):
        return self.vel_y > 0

    def moving_left( self ):
        return self.vel_x < 0

    def moving_right( self ):
        return self.vel_x > 0

    def check_collision( self, other ):

        def left( vertical_overlap ):
            right_overlap = abs( self.right - other.left )

            if self.moving_right() and right_overlap < vertical_overlap:
                self.stop_x()
                self.right = other.left
                return True

            return False

        def right( vertical_overlap ):
            left_overlap = abs( self.left - other.right )

            if self.moving_left() and left_overlap < vertical_overlap:
                self.stop_x()
                self.left = other.right
                return True

            return False

        def up():
            # self lands on other
            self.stop()
            self.bottom = other.top
            self.grounded = True

        def down():
            self.stop_y()
            self.top = other.bottom

        # Rectangles overlap, they have collided
        if self.colliderect( other ):

            # check the nature of the collision, manipulate self accordingly
            if self.falling():
                fall_overlap = abs( self.bottom - other.top )
                if not left(fall_overlap) and not right(fall_overlap):
                    up()

            elif self.rising():
                rise_overlap = abs( self.top - other.bottom )
                if not left(rise_overlap) and not right(rise_overlap):
                    down()

    def update( self, dt ):
        pass

    def display( self, screen ):
        pygame.draw.rect( screen, self.color, self )

class Platform( Thing ):
    pass

class Character( Thing ):
    def rising( self ):
        return self.vel_y + constants.GRAVITY/2 > 0

    def falling( self ):
        return self.vel_y + constants.GRAVITY/2 < 0

class Player( Character ):

    def __init__( self, *args, **kwargs ):
        '''
        '''
        Character.__init__( self, *args, **kwargs )
        self.grounded = False
        #self.max_velocity = 40

    def jump_event( self, target_location ):
        '''
        '''

        if self.grounded:
            tar_x, tar_y = physics.location_pixels_to_meters(*target_location)

            # NOTE: this needs to be tweaked very carefully
            # NOTE: this may need to be a lot more complicated
            #self.vel_x = tar_x - self.x
            #self.vel_y = tar_y - self.y

            diff_y = tar_y - self.bottom
            if diff_y > 0:
                self.vel_y = (-2*constants.GRAVITY*diff_y)**(0.5)

            self.grounded = False

        # TODO: in-air user controls
        else:
            pass

    def update( self, dt ):
        '''
        '''
        if not self.grounded:
            self.y += self.vel_y*dt + 0.5*constants.GRAVITY*dt*dt
            self.vel_y += constants.GRAVITY*dt

