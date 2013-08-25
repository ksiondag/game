import component
import constants as c
import convert
from manager import Manager, Event
import physics

class Jumpable( component.Component ):
    
    def __init__(self, thing, max_vx=c.MAX_VELOCITY, ax=0, ay=c.GRAVITY):
        component.Component.__init__( self, thing )
        self.max_vx = max_vx
        self.grounded = False
        self.ax = 0
        self.ay = c.GRAVITY

        Manager.Manager().register( Event.FIRE, self )
        Manager.Manager().register( Event.GROUNDED, self )
    
    def move_event( self, target_location ):

        if self.grounded:
            x0 = self.owner.x
            y0 = self.owner.bottom

            xt, yt = convert.location_pixels_to_meters(*target_location)

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

