import component
import constants as c
from manager import Manager, Event
import physics

class Movable( component.Component ):

    def __init__( self, thing, ax=0, ay=c.GRAVITY ):
        component.Component.__init__( self, thing )

        self.vx = 0
        self.vy = 0

        self.ax = ax
        self.ay = ay

        Manager().register( Event.VELOCITY,  self )
        Manager().register( Event.UP,        self )
        Manager().register( Event.DOWN,      self )
        Manager().register( Event.LEFT,      self )
        Manager().register( Event.RIGHT,     self )

    def stop_x( self ):
        vx = 0
        vy = self.vy
        return Event( Event.VELOCITY, (vx,vy), targets=[self.owner] )

    def stop_y( self ):
        vx = self.vx
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
            self.vx, self.vy = event.values
        elif event.name == Event.UP:
            return self.grounded_event()
        elif event.name == Event.DOWN:
            return (self.stop_y(),)
        elif event.name == Event.RIGHT or event.name == Event.LEFT:
            return (self.stop_x(),)
        
        return []
    
    def calculate_x( self, dt ):
        self.owner.x = physics.position( self.owner.x, self.vx, self.ax, dt )
        self.vx = physics.velocity( self.vx, self.ax, dt )

    def calculate_y( self, dt ):
        y = self.owner.bottom
        self.owner.bottom = physics.position( y, self.vy, self.ay, dt )
        self.vy = physics.velocity( self.vy, self.ay, dt )

    def update( self, dt ):
        self.calculate_y( dt )
        self.calculate_x( dt )

class Jumpable( component.Component ):
    
    def __init__(self, thing, max_vx=c.MAX_VELOCITY, ax=0, ay=c.GRAVITY):
        component.Component.__init__( self, thing )
        self.max_vx = max_vx
        self.grounded = False
        self.ax = 0
        self.ay = c.GRAVITY

        Manager().register( Event.FIRE, self )
        Manager().register( Event.GROUNDED, self )
    
    def move_event( self, target_location ):

        if self.grounded:
            x0 = self.owner.x
            y0 = self.owner.bottom

            xt, yt = target_location

            vxy = physics.vxy( x0, xt, self.ax, y0, yt, self.ay, self.max_vx )

            move_event = Event( Event.VELOCITY,
                                values = vxy,
                                targets = [self.owner] )
            
            grounded_event = Event( Event.GROUNDED,
                                    values = (False,),
                                    targets = [self.owner] )

            return move_event, grounded_event

        # TODO: in-air user controls
        else:
            pass
        
        return []

    def retrieve( self, event ):

        if event.name == Event.GROUNDED:
            self.grounded, = event.values
        
        elif event.name == Event.FIRE:
            return self.move_event( event.values )
        
        return []

