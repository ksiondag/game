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
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Components Implemented')

    clock = pygame.time.Clock()

    # TODO: Setup the player component
    player = thing.Thing( 0.4, 0, 0.8, 1.6 )
    player.add_component( component.Pushable( player ) )
    player.add_component( component.Rect( player, c.WHITE ) )
    player.add_component( component.Movable( player ) )
    player.add_component( component.Jumpable( player ) )

    #platforms = [thing.Platform( -10, c.GROUND-10, c.WALL + 20, 10, c.GREEN )]
    #platforms.append( thing.Platform( 260, 250, 100, 10, c.GREEN ) )
    #platforms.append( thing.Platform( 400, 250, 10, 100, c.GREEN ) )

    while True:
        # Update clock
        dt = clock.tick( c.FPS ) / 1000.

        # Clear the screen
        screen.fill( c.BLACK )

        # Check input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                jump_event = Event( Event.FIRE, 
                                    values = pygame.mouse.get_pos(),
                                    targets = [player] )
                Manager.Manager().send_immediately( jump_event )
                                                    
            if event.type == pygame.QUIT:
                # TODO: delete everything
                print
                pygame.quit()
                sys.exit()

        # Update everything
        #for platform in platforms:
            #platform.update( dt )
            #player.check_collision( platform )
        player.update( dt )
        Manager.Manager().send_all()

        # Display everything
        player.display( screen )
        #for platform in platforms:
            #platform.display( screen )

        # Update the screen
        pygame.display.flip()
        

if __name__ == '__main__':
    main()

