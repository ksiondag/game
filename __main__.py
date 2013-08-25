import pygame
import sys

import constants as c
import component
import convert
import thing
from manager import Event, Manager

def main():
    '''
    '''
    pygame.init()
    manager = Manager.Manager()

    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Components Implemented')

    clock = pygame.time.Clock()

    # TODO: Setup the player component
    player = thing.Thing( 0.4, 0.2, 0.8, 1.6 )
    player.add_component( component.Movable( player ) )
    player.add_component( component.Jumpable( player ) )
    player.add_component( component.Pathable( player ) )
    player.add_component( component.Pushable( player ) )
    player.add_component( component.Rect( player, c.WHITE ) )

    platform = thing.Thing( 0, 0, convert.pixels_to_meters(c.WALL), 0.2 )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( 10.4, 8.8, 4. ,  .4 )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    platform = thing.Thing( 16.0, 5.2, 0.4, 4   )
    platform.add_component( component.Rect( platform, c.GREEN ) )
    platform.add_component( component.Collidable( platform ) )

    while True:
        # Update clock
        dt = clock.tick( c.FPS ) / 1000.

        # Clear the screen
        screen.fill( c.BLACK )

        # Check input
        # TODO: send a custom version of any event we pull in to the manager
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                manager.add_event( Event( Event.FIRE, 
                                   values = event.pos,
                                   targets = [player] ) )
            elif event.type == pygame.MOUSEMOTION:
                manager.add_event( Event( Event.AIM,
                                   values = event.pos,
                                   targets = [player] ) )
            elif event.type == pygame.QUIT:
                # TODO: delete everything
                print
                pygame.quit()
                sys.exit()

        Manager.Manager().send_all()
        thing.update_all( dt )
        thing.display_all( screen )

        pygame.display.flip()

if __name__ == '__main__':
    main()

