import pygame
import sys

import component
import constants as c
from controller import Controller
import convert
import thing
from manager import Event, Manager

def quit( event ):
    # TODO: delete everything
    print
    pygame.quit()
    sys.exit()

def click( event ):
    Manager.Manager().add_event(Event(Event.CLICK, (event.pos, event.button)))

def swipe( event ):
    Manager.Manager().add_event( Event( Event.SWIPE, (event.pos, event.rel) ) )

def ignore( event ):
    return

EVENT_DICT = {
    pygame.QUIT:            quit,
    pygame.MOUSEBUTTONDOWN: click,
    pygame.MOUSEMOTION:     swipe,
}

def event_translator( events ):
    for event in events:
        EVENT_DICT.get( event.type, ignore )( event )

def main():
    '''
    '''
    pygame.init()

    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Components Implemented')

    clock = pygame.time.Clock()

    # TODO: Setup the player component
    player = thing.Thing( 0.4, 0.2, 0.8, 1.6 )
    player.add_component( component.Movable( player ) )
    player.add_component( component.Jumpable( player ) )
    player.add_component( component.Pushable( player ) )
    player.add_component( component.Pathable( player ) )
    player.add_component( component.Rect( player, c.WHITE ) )

    Controller.Controller().set_player( player )
    manager = Manager.Manager()

    platform = thing.Thing( 0, -0.2, 100, 0.2 )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( 10.4, 8.8, 4. ,  .4 )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( 16.0, 5.2, 0.4, 4   )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( -0.1, 0.0, 0.1, 20  )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( 100., 0.0, 0.1, 20  )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    while True:
        # Update clock
        dt = clock.tick( c.FPS ) / 1000.

        # Clear the screen
        screen.fill( c.BLACK )

        # Check input from pygame events
        event_translator( pygame.event.get() )

        Manager.Manager().send_all()
        thing.update_all( dt )
        thing.display_all( screen )

        pygame.display.flip()

if __name__ == '__main__':
    main()

