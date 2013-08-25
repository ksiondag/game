import pygame

class Component:
    #components = []

    def __init__( self, thing ):
        self.owner = thing
        #Component.components.append( self )

    def retrieve( self, event ):
        return []

    def update( self, dt ):
        pass

    def display( self, screen ):
        pass

