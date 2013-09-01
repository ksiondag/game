import pygame

class Component:

    def __init__( self, thing ):
        self.owner = thing

    def retrieve( self, event ):
        return []

    def update( self, dt ):
        pass

    def display( self, screen ):
        pass

