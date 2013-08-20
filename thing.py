import pygame
import sys

import constants as c
import convert
import physics

class Thing( pygame.rect.Rect ):
    
    def __init__( self, left, top, width, height, color ):
        '''
        '''
        #left, top = convert.location_meters_to_pixels( left, top )
        #width = convert.meters_to_pixels( width )
        #height = convert.meters_to_pixels( height )

        pygame.rect.Rect.__init__( self, left, top, width, height )

        self.color = color
        self.stop()

    _left = pygame.rect.Rect.left
    _right = pygame.rect.Rect.right
    _top = pygame.rect.Rect.top
    _bottom = pygame.rect.Rect.bottom

    @property
    def left( self ):
        #return pixels_to_meters( self._left )
        return convert.pixels_to_meters( self._left )

    @left.setter
    def left( self, value ):
        self._left = convert.meters_to_pixels( value )

    @property
    def right( self ):
        return convert.pixels_to_meters( self._right )

    @right.setter
    def right( self, value ):
        self._right = convert.meters_to_pixels( value )

    @property
    def x( self ):
        return convert.pixels_to_meters( self.centerx )

    @x.setter
    def x( self, value ):
        self.centerx = convert.meters_to_pixels( value )

    @property
    def top( self ):
        return convert.vertical_pixels_to_meters( self._top )

    @top.setter
    def top( self, value ):
        self._top = convert.vertical_meters_to_pixels( value )

    @property
    def bottom( self ):
        return convert.vertical_pixels_to_meters( self._bottom )

    @bottom.setter
    def bottom( self, value ):
        self._bottom = convert.vertical_meters_to_pixels( value )

    @property
    def y( self ):
        return convert.vertical_pixels_to_meters( self.centery )

    @y.setter
    def y( self, value ):
        self.centery = convert.vertical_meters_to_pixels( value )

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
        return self.vel_y + c.GRAVITY/2 > 0

    def falling( self ):
        return self.vel_y + c.GRAVITY/2 < 0

class Player( Character ):

    def __init__( self, *args, **kwargs ):
        '''
        '''
        Character.__init__( self, *args, **kwargs )
        self.grounded = False
        self.max_velocity = 10.

        self.t = 0
        self.x0 = self.x
        self.y0 = self.bottom
        self.vy0 = 0

    def stop_x( self ):
        self.x0 = self.x
        Thing.stop_x( self )

    @property
    def vel_y( self ):
        if self.grounded:
            return 0
        return physics.velocity( self.vy0, c.GRAVITY, self.t )

    # TODO
    @vel_y.setter
    def vel_y( self, value ):
        pass

    def calculate_y( self, dt ):
        #self.y += dt*(self.vel_y + 0.5*c.GRAVITY*dt)
        #self.vel_y += dt*c.GRAVITY

        if not self.grounded:
            self.bottom = physics.position(self.y0,self.vy0,c.GRAVITY,self.t)

    def calculate_x( self, dt ):
        self.x = physics.position( self.x0, self.vel_x, 0, self.t )

        if self.left < 0:
            self.left = 0
        if self.right > convert.pixels_to_meters(c.WALL):
            self.right = convert.pixels_to_meters(c.WALL)

    def jump_event( self, target_location ):
        '''
        '''

        # TODO: all of this can be optimized
        if self.grounded:
            self.x0 = self.x
            self.y0 = self.bottom
            self.t = 0

            tar_x, tar_y = convert.location_pixels_to_meters(*target_location)

            # Find y velocity, time
            self.vy0 = physics.vy( self.bottom, tar_y, c.GRAVITY )
            time_y = physics.ty( self.bottom, tar_y, self.vy0, c.GRAVITY )

            # Find x velocity, time
            self.vel_x = physics.vx( self.x, tar_x, time_y, self.max_velocity )
            time_x = physics.tx( self.x, tar_x, self.vel_x, time_y )

            # Correct y velocity to land on target y at time x
            if time_x > time_y:
                self.vy0 = physics.vy2(self.bottom, tar_y, c.GRAVITY, time_x)

            self.grounded = False

        # TODO: in-air user controls
        else:
            pass

    def update( self, dt ):
        '''
        '''
        self.t += dt
        self.calculate_y( dt )
        self.calculate_x( dt )

    def display( self, screen ):
        Character.display( self, screen )
        if self.grounded:
            target_location = pygame.mouse.get_pos()

            x0 = self.x
            y0 = self.bottom

            tar_x, tar_y = convert.location_pixels_to_meters(*target_location)

            # Find y velocity, time
            vy0 = physics.vy( self.bottom, tar_y, c.GRAVITY )
            time_y = physics.ty( self.bottom, tar_y, vy0, c.GRAVITY )

            # Find x velocity, time
            vel_x = physics.vx( self.x, tar_x, time_y, self.max_velocity )
            time_x = physics.tx( self.x, tar_x, vel_x, time_y )

            # Correct y velocity to land on target y at time x
            if time_x > time_y:
                vy0 = physics.vy2(y0, tar_y, c.GRAVITY, time_x)
        else:
            x0 = self.x0
            y0 = self.y0
            vy0 = self.vy0
            vel_x = self.vel_x

        # TODO: display curve of jump
        times = [ i/10. for i in range(21) ]
        x_points = [ physics.position( x0, vel_x, 0, t ) for t in times ]
        y_points = [ physics.position( y0, vy0, c.GRAVITY, t ) for t in times ]

        points = zip( x_points, y_points )
        points = [ convert.location_meters_to_pixels(x, y) for x, y in points ]

        pygame.draw.aalines( screen, c.RED, False, points )

