import pygame

class Component:

    def __init__( self, thing, priority=-1 ):
        self.owner = thing

    def retrieve( self, event ):
        pass

    def update( self, dt ):
        pass

    def display( self, screen ):
        pass

