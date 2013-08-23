import component
import constants as c
import convert
from manager import Manager, Event
import physics

class Movable( component.Component ):

    def __init__( self, thing, max_velocity=c.MAX_VELOCITY ):
        component.Component.__init__( self, thing )

        self.t = 0
        self.x0 = self.owner.x
        self.y0 = self.owner.bottom

        self.vx = 0
        self.vy = 0

        self.ax = 0
        self.ay = c.GRAVITY

        Manager.Manager().register( Event.MOVE, self )
        Manager.Manager().register( Event.UP, self )
        Manager.Manager().register( Event.DOWN, self )
        Manager.Manager().register( Event.LEFT, self )
        Manager.Manager().register( Event.RIGHT, self )

    def stop_x( self ):
        self.x0 = self.owner.x
        self.vx = 0

    def stop_y( self ):
        self.x0 = self.owner.x
        self.y0 = self.owner.bottom
        self.vy = 0
        self.t = 0

    def stop( self ):
        self.stop_x()
        self.stop_y()
    
    def grounded_event( self ):
        self.stop()
        values = True, self.ax, self.ay
        self.ax = 0
        self.ay = 0
        return Event( Event.GROUNDED, values, targets=[self.owner] )

    def retrieve( self, event ):

        if event.name == Event.MOVE:
            self.t = 0
            self.x0 = self.owner.x
            self.y0 = self.owner.bottom
            self.vx, self.vy, self.ax, self.ay = event.values
        elif event.name == Event.UP:
            Manager.Manager().send_immediately( self.grounded_event() )
        elif event.name == Event.DOWN:
            self.stop_y()
        elif event.name == Event.RIGHT:
            self.stop_x()
        elif event.name == Event.LEFT:
            self.stop_x()
    
    def calculate_x( self, dt ):
        self.owner.x = physics.position( self.x0, self.vx, self.ax, self.t )

        if self.owner.left < 0:
            self.owner.left = 0
            self.stop_x()
        if self.owner.right > convert.pixels_to_meters(c.WALL):
            self.owner.right = convert.pixels_to_meters(c.WALL)
            self.stop_x()

    def calculate_y( self, dt ):
        self.owner.bottom = physics.position( self.y0, self.vy, self.ay, self.t )

        if self.owner.bottom < 0:
            self.owner.bottom = 0
            Manager.Manager().add_event( self.grounded_event() )
    
    def update( self, dt ):
        self.t += dt
        self.calculate_y( dt )
        self.calculate_x( dt )

