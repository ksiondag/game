import pygame
import sys

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN =   0, 255,   0

GRAVITY = 1.0
GROUND = 480
WALL = 640

class Thing:
    
    def __init__( self, x, y, width, height, color ):
        '''
        '''
        self.pos_x = x
        self.pos_y = y

        self.vel_x = 0
        self.vel_y = 0

        self.width  = width
        self.height = height

        self.color = color

    def collision_event( self, other ):
        '''
        '''
        pass

    def update( self ):
        '''
        '''
        pass

    def display( self, screen ):
        '''
        '''
        pygame.draw.rect( screen, self.color, (self.pos_x, self.pos_y, 
                                               self.width, self.height) )

class Platform( Thing ):
    pass

class Character( Thing ):
    pass

class Player( Character ):

    def __init__( self, *args, **kwargs ):
        '''
        '''
        Character.__init__( self, *args, **kwargs )
        self.grounded = False

    def move_event( self, target_location ):
        '''
        '''

        if self.grounded:
            target_x, target_y = target_location

            self.vel_x = (target_x - self.pos_x)/15
            self.vel_y = (target_y - self.pos_y)/10

        # TODO: in-air user controls
        else:
            pass

    def collision_event( self, other ):
        # TODO: when colliding with other object, react appropriately
        pass

    def update( self ):
        '''
        '''
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        if self.pos_y + self.height < GROUND:
            self.vel_y += GRAVITY
            self.grounded = False
        else:
            self.vel_x = 0
            self.vel_y = 0

            self.pos_y = GROUND - self.height

            self.tar_x = self.pos_x
            self.tar_y = self.pos_y

            self.grounded = True
        
        if self.pos_x < 0:
            self.vel_x = 0
            self.pos_x = 0
        if self.pos_x + self.width > WALL:
            self.vel_x = 0
            self.pos_x = WALL - self.width


def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Controlable Rectangle in Gravity Environment')

    clock = pygame.time.Clock()

    character = Player( 300, 200, 20, 40, WHITE )
    platforms = [Platform( 0, GROUND - 10, WALL, 10, GREEN )]

    while True:
        # Update clock
        clock.tick(50)

        # Clear the screen
        screen.fill( BLACK )

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

