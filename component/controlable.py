import component
import constants as c
import convert
from manager import Manager, Event
import physics

class Jumpable( component.Component ):
    
    def __init__( self, thing, max_velocity=c.MAX_VELOCITY ):
        component.Component.__init__( self, thing )
        self.max_velocity = max_velocity
        self.grounded = False
        self.ax = 0
        self.ay = 0

        Manager.Manager().register( Event.FIRE, self )
        Manager.Manager().register( Event.GROUNDED, self )
    
    def move_event( self, target_location ):

        if self.grounded:
            x0 = self.owner.x
            y0 = self.owner.bottom

            xt, yt = convert.location_pixels_to_meters(*target_location)

            # Find y velocity, time
            vy = physics.vp_max( y0, yt, self.ay )
            ty = physics.tp( y0, yt, vy, self.ay )

            # Find x velocity, time
            vx = physics.vp( x0, xt, self.ax, ty, self.max_velocity )

            # Correct y velocity to land on target y at time x
            if abs(vx) > self.max_velocity:
                if vx > 0:
                    vx = self.max_velocity
                else:
                    vx = -self.max_velocity
                tx = physics.tp( x0, xt, vx, self.ax )
                vy = physics.vp( y0, yt, self.ay, tx )

            move_event = Event( Event.MOVE, 
                                values = (vx, vy, self.ax, self.ay),
                                targets = [self.owner] )
            grounded_event = Event( Event.GROUNDED,
                                    values = (False, self.ax, self.ay),
                                    targets = [self.owner] )
            
            Manager.Manager().send_immediately( move_event )
            Manager.Manager().send_immediately( grounded_event )

        # TODO: in-air user controls
        else:
            pass

    def retrieve( self, event ):

        if event.name == Event.GROUNDED:
            self.grounded, self.ax, self.ay = event.values
        
        elif event.name == Event.FIRE:
            self.move_event( event.values )

    def update( self, dt ):
        pass

