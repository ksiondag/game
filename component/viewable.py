import pygame

import component
from scrolling import Scrolling
import constants as c
from manager import Event, Manager

import physics

class Rect( component.Component ):
    
    def __init__( self, thing, color ):
        component.Component.__init__( self, thing )
        self.color = color
        self.update( 0 )

    def update( self, dt ):
        left = Scrolling().x_meters_to_pixels( self.owner.left )
        top = Scrolling().y_meters_to_pixels( self.owner.top )
        width = Scrolling().meters_to_pixels( self.owner.width )
        height = Scrolling().meters_to_pixels( self.owner.height )

        self.rect = pygame.rect.Rect( left, top, width, height )

    def display( self, screen ):
        pygame.draw.rect( screen, self.color, self.rect )

class Pathable( component.Component ):

    def __init__(self, thing, max_vx=c.MAX_VELOCITY, ax=0, ay=c.GRAVITY ):
        component.Component.__init__( self, thing )

        self.x0 = self.owner.x
        self.y0 = self.owner.bottom

        self.aim = 0, 0
        self.vxy = 0, 0
        self.max_vx = max_vx

        self.ax = ax
        self.ay = ay

        self.grounded = False

        Manager().register( Event.AIM,      self )
        Manager().register( Event.GROUNDED, self )
        Manager().register( Event.VELOCITY, self )

    def retrieve( self, event ):

        if event.name == Event.AIM:
            self.aim = event.values

        elif event.name == Event.GROUNDED:
            self.grounded, = event.values

            if self.grounded:
                self.x0 = self.owner.x
                self.y0 = self.owner.bottom

        elif event.name == Event.VELOCITY:
            self.vxy = event.values
            if not self.grounded:
                self.x0 = self.owner.x
                self.y0 = self.owner.bottom

        return []

    def display( self, screen ):

        if self.grounded:
            xt, yt = Scrolling().location_pixels_to_meters( *self.aim )
            vx, vy = physics.vxy( self.x0, xt, self.ax,
                                  self.y0, yt, self.ay,
                                  self.max_vx )
        else:
            vx, vy = self.vxy

        # TODO: display curve of jump
        times = [ i/10. for i in range(21) ]
        x_points = [physics.position( self.x0, vx, self.ax, t ) for t in times]
        y_points = [physics.position( self.y0, vy, self.ay, t ) for t in times]

        points = zip( x_points, y_points )
        points = [Scrolling().location_meters_to_pixels(*xy) for xy in points]

        pygame.draw.aalines( screen, c.RED, False, points )

