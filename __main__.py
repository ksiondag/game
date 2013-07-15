import pygame
import sys

import thing
import constants

def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Controlable Rectangle in Gravity Environment')

    clock = pygame.time.Clock()

    character = thing.Player( 300, 200, 20, 40, constants.WHITE )
    platforms = [ thing.Platform(             0,constants.GROUND-10,
                                 constants.WALL,                 10,
                                 constants.GREEN ) ]

    while True:
        # Update clock
        clock.tick(50)

        # Clear the screen
        screen.fill( constants.BLACK )

        # Check input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                character.move_event( pygame.mouse.get_pos() )
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Character update and display
        character.update()
        character.display( screen )

        # Platforms update and display
        for platform in platforms:
            platform.update()
            platform.display( screen )

        # Update the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()

