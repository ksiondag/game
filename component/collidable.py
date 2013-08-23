import component
import constants as c
from manager import Manager, Event

class Collidable( component.Component ):

    collidables = []
    
    def __init__( self, thing ):
        Component.__init__( self, thing )
        Collidable.collidables.append( self )
    
    def __del__( self ):
        Collidable.collidables.remove( self )
        Component.__del__( self )

class Pushable( component.Component ):

    def check_collision( self, other ):

        # Rectangles overlap, they have collided
        if self.colliderect( other ):
            right_overlap = abs( self.owner.right  - other.owner.left )
            left_overlap  = abs( self.owner.left   - other.owner.right )
            down_overlap  = abs( self.owner.bottom - other.owner.top )
            up_overlap    = abs( self.owner.top    - other.owner.bottom )

            min_overlap = min( right_overlap, left_overlap,
                               down_overlap,  up_overlap )

            if min_overlap == down_overlap:
                self.owner.bottom = other.owner.top
                Manager.Manager().add_event( Event(Event.UP),
                                             targets=[self.owner] )
            elif min_overlap == up_overlap:
                self.owner.top = other.owner.bottom
                Manager.Manager().add_event( Event( Event.DOWN ),
                                             targets=[self.owner] )
            elif min_overlap == left_overlap:
                self.owner.left = other.owner.right
                Manager.Manager().add_event( Event( Event.RIGHT ),
                                             targets=[self.owner] )
            elif min_overlap == right_overlap:
                self.owner.right = other.owner.left
                Manager.Manager().add_event( Event( Event.LEFT ),
                                             targets=[self.owner] )

    # Check collision with everything
    def update( self, dt ):
        for other in Collidable.collidables:
            if self.owner != other.owner:
                self.check_collision( other )

