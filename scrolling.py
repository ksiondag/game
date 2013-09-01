from component import Component
import constants as c

from manager import Event, Manager

class _Scroller( Component ):

    def __init__( self ):
        self.player = None
        self.cursor = None

        self.min_left = 0
        self.left = 0

        self.min_bottom = 0
        self.bottom = 0

        Manager().register( Event.PLAYER, self )

    def set_player( self, player ):
        self.player = player

    def retrieve( self, event ):

        if event.name == Event.PLAYER:
            self.player, = event.values

        return []
    
    def update( self, dt ):
        if self.cursor is None and self.player is None:
            return
        
        if self.cursor is None:
            center = self.player.x

        else:
            center = (self.player.x + self.cursor.x)/2

        self.left = center - self.pixels_to_meters( c.PIXEL_WIDTH )/2.

        if self.left < self.min_left:
            self.left = self.min_left

    def meters_to_pixels( self, meters ):
        return 25.*meters

    def pixels_to_meters( self, pixels ):
        return pixels/25.

    def x_meters_to_pixels( self, meters ):
        return 25.*(meters - self.left)

    def x_pixels_to_meters( self, pixels ):
        return self.left + pixels/25.

    def y_pixels_to_meters( self, pixels ):
        return self.bottom + self.pixels_to_meters( c.PIXEL_HEIGHT - pixels )

    def y_meters_to_pixels( self, meters ):
        return c.PIXEL_HEIGHT - self.meters_to_pixels( meters - self.bottom )

    def location_pixels_to_meters( self, pixel_x, pixel_y ):
        x = self.x_pixels_to_meters( pixel_x )
        y = self.y_pixels_to_meters( pixel_y )

        return x, y

    def location_meters_to_pixels( self, x, y ):
        pixel_x = self.x_meters_to_pixels( x )
        pixel_y = self.y_meters_to_pixels( y )

        return pixel_x, pixel_y

_SCROLLING = None

def Scrolling():
    global _SCROLLING
    if _SCROLLING is None:
        _SCROLLING = _Scroller()
    return _SCROLLING

