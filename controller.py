from manager import Event, Manager

class Controller( object ):

    _CONTROLLER = None
    
    @classmethod
    def Controller( cls ):
        if Controller._CONTROLLER is None:
            Controller._CONTROLLER = cls()
        return Controller._CONTROLLER
    
    def __init__( self ):
        self.player = None

        Manager.Manager().register( Event.CLICK, self )
        Manager.Manager().register( Event.SWIPE, self )

    def set_player( self, player ):
        self.player = player 

    def retrieve( self, event ):
        
        if event.name == Event.CLICK:
            pos, button = event.values
            return [Event( Event.FIRE, values = pos, targets = [self.player] )]
        elif event.name == Event.SWIPE:
            pos, rel = event.values
            return [Event( Event.AIM, values = pos, targets = [self.player] )]

        return []

