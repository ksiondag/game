class Event( object ):

    # Set events
    PLAYER = 'player'
    
    # Controller events
    CLICK = 'click'
    SWIPE = 'swipe'

    # Action events
    AIM = 'aim'
    FIRE = 'fire'

    # Manipulation events
    VELOCITY = 'velocity'
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'

    # State events
    GROUNDED = 'grounded'

    def __init__( self, name, values=None, targets=None ):
        self.name = name
        self.values = values
        self.targets = targets

    def __str__( self ):
        return '%s (%s)' % ( self.name, self.values )

class _Manager( object ):

    def __init__( self ):
        self.listeners = {}
        self.events = []

    def add_event( self, event ):
        self.events.append( event )

    def add_events( self, events ):
        self.events.extend( events )

    def register( self, event_name, component ):
        if event_name not in self.listeners:
            self.listeners[ event_name ] = []
        self.listeners[ event_name ].append( component )
    
    def send_immediately( self, event ):
        for component in self.listeners.get( event.name, [] ):
            if event.targets is None or component.owner in event.targets:

                events = component.retrieve( event )

                for event in events:
                    self.send_immediately( event )

    def send_all( self ):
        events = self.events
        self.events = []
        for event in events:
            self.send_immediately( event )

_MANAGER = None

def Manager():
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = _Manager()
    return _MANAGER

