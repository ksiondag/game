import pygame

import constants as c
import convert
import physics

class Thing( object ):
    
    def __init__( self, left, bottom, width, height ):
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

        self.components = []

    @property
    def top( self ):
        return self.bottom + self.height

    @top.setter
    def top( self, value ):
        self.bottom = value - self.height

    @property
    def right( self ):
        return self.left + self.width

    @right.setter
    def right( self, value ):
        self.left = value - self.width

    @property
    def y( self ):
        return self.bottom + self.height/2.

    @y.setter
    def y( self, value ):
        self.bottom = value - self.height/2.

    @property
    def x( self ):
        return self.left + self.width/2.

    @x.setter
    def x( self, value ):
        self.left = value - self.width/2.

    def add_component( self, component ):
        self.components.append( component )
    
    def add_displayable( self, displayable ):
        self.add_component( displayable )
        self.displayables.append( displayable )

    def update( self, dt ):
        for component in self.components:
            component.update( dt )

    def display( self, screen ):
        for component in self.components:
            component.display( screen )

