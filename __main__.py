import pygame
import sys

import thing
import constants

def check_collision( thing1, thing2 ):

    # Rectangles overlap if thing2 pushes on thing1 in all directions
    push_right = thing2.x + thing2.width  - thing1.x
    push_left  = thing1.x + thing1.width  - thing2.x
    push_down  = thing2.y + thing2.height - thing1.y
    push_up    = thing1.y + thing1.height - thing2.y

    # Rectangles overlap, they have collided
    if push_right > 0 and push_left > 0 and push_up > 0 and push_down > 0:
        print push_right, push_left, push_up, push_down
        # Path of least resistance to undo overlap
        min_push = min( push_right, push_left, push_up, push_down )

        # Elastic bounce off wall of thing2
        if push_right == min_push or push_left == min_push:
            thing1.vel_x = -thing1.vel_x

        # thing1 lands on thing2
        if push_up == min_push:
            print "Pushing up", thing1.vel_y
            if thing1.vel_y > 0:
                thing1.stop()
            thing1.y = thing2.y - thing1.height
            thing1.grounded = True

        # Elastic bounce off roof of thing2
        if push_down == min_push:
            print "Pushing down"
            thing1.vel_y = -thing1.vel_y

def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Platforms in Gravity Environment')

    clock = pygame.time.Clock()

    player = thing.Player( 300, 200, 20, 40, constants.WHITE )
    platforms = [ thing.Platform(           -10,     constants.GROUND-10,
                                 constants.WALL + 10,                 10,
                                 constants.GREEN ) ]
    platforms.append( thing.Platform( 260, 250, 100, 10, constants.GREEN ) )

    while True:
        # Update clock
        clock.tick( constants.FPS )

        # Clear the screen
        screen.fill( constants.BLACK )

        # Check input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.move_event( pygame.mouse.get_pos() )
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update everything
        player.update()
        for platform in platforms:
            platform.update()
            check_collision( player, platform )

        # Display everything
        player.display( screen )
        for platform in platforms:
            platform.display( screen )

        # Update the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()

