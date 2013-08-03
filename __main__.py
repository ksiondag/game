import pygame
import sys

import thing
import constants

def check_collision( thing1, thing2 ):

    def push_left( vertical_overlap ):
        right_overlap = abs( thing1.right - thing2.left )

        if thing1.moving_right() and right_overlap < vertical_overlap:
            thing1.stop_x()
            thing1.right = thing2.left
            return True

        return False

    def push_right( vertical_overlap ):
        left_overlap = abs( thing1.left - thing2.right )

        if thing1.moving_left() and left_overlap < vertical_overlap:
            thing1.stop_x()
            thing1.left = thing2.right
            return True

        return False

    def push_up():
        # thing1 lands on thing2
        thing1.stop()
        thing1.bottom = thing2.top
        thing1.grounded = True

    def push_down():
        thing1.stop_y()
        thing1.top = thing2.bottom

    # Rectangles overlap, they have collided
    if thing1.colliderect( thing2 ):

        # check the nature of the collision, manipulate thing1 accordingly
        if thing1.falling():
            fall_overlap = abs( thing1.bottom - thing2.top )
            if not push_left(fall_overlap) and not push_right(fall_overlap):
                push_up()

        elif thing1.rising():
            rise_overlap = abs( thing1.top - thing2.bottom )
            if not push_left(rise_overlap) and not push_right(rise_overlap):
                push_down()


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
            check_collision( player, platform )

        # Display everything
        player.display( screen )
        for platform in platforms:
            platform.display( screen )

        # Update the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()

