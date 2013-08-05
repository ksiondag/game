import pygame
import sys

import thing
import constants


def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Platforms in Gravity Environment')

    clock = pygame.time.Clock()

    player = thing.Player( 10, constants.GROUND-50, 20, 40, constants.WHITE )
    platforms = [ thing.Platform(                -10, constants.GROUND-10,
                                 constants.WALL + 20,                  10,
                                 constants.GREEN ) ]
    platforms.append( thing.Platform( 260, 250, 100, 10, constants.GREEN ) )
    platforms.append( thing.Platform( 400, 250, 10, 100, constants.GREEN ) )

    while True:
        # Update clock
        dt = clock.tick( constants.FPS ) / 1000.

        # Clear the screen
        screen.fill( constants.BLACK )

        # Check input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.jump_event( pygame.mouse.get_pos() )
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update everything
        player.update( dt )
        for platform in platforms:
            platform.update( dt )
            player.check_collision( :latform )

        # Display everything
        player.display( screen )
        for platform in platforms:
            platform.display( screen )

        # Update the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()

