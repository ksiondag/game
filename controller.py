from manager import Event, Manager
from component import Component
from scrolling import Scrolling

class _Controller( Component ):

    def __init__( self ):
        self.player = None

        Manager().register( Event.CLICK,  self )
        Manager().register( Event.SWIPE,  self )
        Manager().register( Event.PLAYER, self )

    def retrieve( self, event ):
        
        if event.name == Event.CLICK:
            pos, button = event.values
            pos = Scrolling().location_pixels_to_meters( *pos )
            return [Event( Event.FIRE, values = pos, targets = [self.player] )]
        elif event.name == Event.SWIPE:
            pos, rel = event.values
            return [Event( Event.AIM, values = pos, targets = [self.player] )]
        elif event.name == Event.PLAYER:
            self.player, = event.values

        return []

_CONTROLLER = None
    
def Controller():
    global _CONTROLLER
    if _CONTROLLER is None:
        _CONTROLLER = _Controller()
    return _CONTROLLER

