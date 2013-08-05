import pygame
import constants

class Thing( pygame.rect.Rect ):
    
    def __init__( self, left, top, width, height, color ):
        '''
        '''
        pygame.rect.Rect.__init__( self, left, top, width, height )
        self.color = color
        self.stop()

    def stop( self ):
        self.stop_x()
        self.stop_y()

    def stop_x( self ):
        self.vel_x = 0

    def stop_y( self ):
        self.vel_y = 0

    def falling( self ):
        return self.vel_y > 0

    def rising( self ):
        return self.vel_y < 0

    def moving_right( self ):
        return self.vel_x > 0

    def moving_left( self ):
        return self.vel_x < 0

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
        return self.vel_y + constants.GRAVITY/2 < 0

    def falling( self ):
        return self.vel_y + constants.GRAVITY/2 > 0

class Player( Character ):

    def __init__( self, *args, **kwargs ):
        '''
        '''
        Character.__init__( self, *args, **kwargs )
        self.grounded = False

    def jump_event( self, target_location ):
        '''
        '''

        if self.grounded:
            target_x, target_y = target_location

            # NOTE: this needs to be tweaked very carefully
            # NOTE: this may need to be a lot more complicated
            self.vel_x = 50*(target_x - self.x)/15
            self.vel_y = 50*(target_y - self.y)/15
            
            self.grounded = False

        # TODO: in-air user controls
        else:
            pass

    def update( self, dt ):
        '''
        '''
        self.x += self.vel_x * dt

        if not self.grounded:
            self.y += (self.vel_y + constants.GRAVITY/2) * dt
            self.vel_y += constants.GRAVITY * dt

        if self.x < 0:
            self.vel_x = 0
            self.x = 0
        if self.x + self.width > constants.WALL:
            self.vel_x = 0
            self.x = constants.WALL - self.width

