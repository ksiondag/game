import pygame

import component
import convert
import constants as c

class Rect( component.Component ):
    
    def __init__( self, thing, color, priority=100 ):
        component.Component.__init__( self, thing, priority )
        self.color = color
        self.update( 0 )

    def update( self, dt ):
        left = convert.meters_to_pixels( self.owner.left )
        top = convert.vertical_meters_to_pixels( self.owner.top )
        width = convert.meters_to_pixels( self.owner.width )
        height = convert.meters_to_pixels( self.owner.height )

        self.rect = pygame.rect.Rect( left, top, width, height )

    def display( self, screen ):
        pygame.draw.rect( screen, self.color, self.rect )

class Pathable( component.Component ):

    def __init__(self, thing, priority=100, max_velocity=c.MAX_VELOCITY ):
        component.Component.__init__( self, thing, display_priority )

        self.x0 = self.owner.x
        self.y0 = self.owner.bottom

        self.ax = 0
        self.ay = 0

        self.grounded = False

        # TODO: register for event receival
    
    def retrieve( self, event ):

        if event.name == Event.GROUNDED:
            self.grounded, self.ax, self.ay = event.values
        elif event.name == Event.AIM:
            pass
    
    def display( self, screen ):
        '''
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
        x_points = [ physics.position( x0, vx, self.ax, t ) for t in times ]
        y_points = [ physics.position( y0, vy, self., t ) for t in times ]

        points = zip( x_points, y_points )
        points = [ convert.location_meters_to_pixels(x, y) for x, y in points ]

        pygame.draw.aalines( screen, c.RED, False, points )
        '''

