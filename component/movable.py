import component
import constants as c
import convert
from manager import Manager, Event
import physics

class Movable( component.Component ):

    def __init__( self, thing, ax=0, ay=c.GRAVITY ):
        component.Component.__init__( self, thing )

        self.t = 0
        self.x0 = self.owner.x
        self.y0 = self.owner.bottom

        self.vx = 0
        self.vy = 0

        self.ax = ax
        self.ay = ay

        Manager.Manager().register( Event.VELOCITY,  self )
        Manager.Manager().register( Event.UP,        self )
        Manager.Manager().register( Event.DOWN,      self )
        Manager.Manager().register( Event.LEFT,      self )
        Manager.Manager().register( Event.RIGHT,     self )

    def stop_x( self ):
        vx = 0
        vy = physics.velocity( self.vy, self.ay, self.t )
        return Event( Event.VELOCITY, (vx,vy), targets=[self.owner] )

    def stop_y( self ):
        vx = physics.velocity( self.vx, self.ax, self.t )
        vy = 0
        return Event( Event.VELOCITY, (vx,vy), targets=[self.owner] )

    def stop( self ):
        vx, vy = 0, 0
        return Event( Event.VELOCITY, (vx,vy), targets=[self.owner] )
    
    def grounded_event( self ):
        self.stop()
        values = True,
        return self.stop(), Event(Event.GROUNDED, values, targets=[self.owner])

    def retrieve( self, event ):

        if event.name == Event.VELOCITY:
            self.t = 0
            self.x0 = self.owner.x
            self.y0 = self.owner.bottom
            self.vx, self.vy = event.values
        elif event.name == Event.UP:
            return self.grounded_event()
        elif event.name == Event.DOWN:
            return (self.stop_y(),)
        elif event.name == Event.RIGHT or event.name == Event.LEFT:
            return (self.stop_x(),)
        
        return []
    
    def calculate_x( self, dt ):
        self.owner.x = physics.position( self.x0, self.vx, self.ax, self.t )

        if self.owner.left < 0:
            self.owner.left = 0
            Manager.Manager().add_event( self.stop_x() )
        if self.owner.right > convert.pixels_to_meters(c.WALL):
            self.owner.right = convert.pixels_to_meters(c.WALL)
            Manager.Manager().add_event( self.stop_x() )

    def calculate_y( self, dt ):
        self.owner.bottom = physics.position(self.y0, self.vy, self.ay, self.t)

        if self.owner.bottom < 0:
            self.owner.bottom = 0
            Manager.Manager().add_events( self.grounded_event() )
    
    def update( self, dt ):
        self.t += dt
        self.calculate_y( dt )
        self.calculate_x( dt )

