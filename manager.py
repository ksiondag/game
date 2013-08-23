class Event:
    
    AIM = 'aim'
    FIRE = 'fire'
    MOVE = 'move'
    GROUNDED = 'grounded'
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'

    def __init__( self, name, values=None, targets=None ):
        self.name = name
        self.values = values
        self.targets = targets

class Manager:

    _MANAGER = None

    @classmethod
    def Manager( cls ):
        if Manager._MANAGER is None:
            Manager._MANAGER = cls()
        return Manager._MANAGER

    def __init__( self ):
        self.listeners = {}
        self.events = []

    def add_event( self, event ):
        self.events.append( event )

    def register( self, event_name, component ):
        if event_name not in self.listeners:
            self.listeners[ event_name ] = []
        self.listeners[ event_name ].append( component )
    
    def send_immediately( self, event ):
        for component in self.listeners.get( event.name, [] ):
            if event.targets is None or component.owner in event.targets:
                component.retrieve( event )

    def send_all( self ):
        events = self.events
        self.events = []
        for event in events:
            self.send_immediately( event )
    
