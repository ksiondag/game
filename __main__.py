import pygame
import sys

BLACK = 0, 0, 0
WHITE = 255, 255, 255

GRAVITY = 1.0
GROUND = 480
WALL = 640

class Character:
    
    def __init__( self, x, y ):
        '''
        '''
        self.pos_x = x
        self.pos_y = y

        self.vel_x = 0
        self.vel_y = 0

        self.width  = 20
        self.height = 20

        self.touching_ground = False

    def move_event( self, target_location ):
        '''
        '''

        if self.touching_ground:
            target_x, target_y = target_location

            self.vel_x = (target_x - self.pos_x)/15
            self.vel_y = (target_y - self.pos_y)/10

        # TODO: in-air user controls
        else:
            pass

    def update( self ):
        '''
        '''
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        if self.pos_y + self.height < GROUND:
            self.vel_y += GRAVITY
            self.touching_ground = False
        else:
            self.vel_x = 0
            self.vel_y = 0

            self.pos_y = GROUND - self.height

            self.tar_x = self.pos_x
            self.tar_y = self.pos_y

            self.touching_ground = True
        
        if self.pos_x < 0:
            self.vel_x = 0
            self.pos_x = 0
        if self.pos_x + self.width > WALL:
            self.vel_x = 0
            self.pos_x = WALL - self.width

    def display( self, screen ):
        '''
        '''
        pygame.draw.rect( screen, WHITE, (self.pos_x, self.pos_y, 
                                          self.width, self.height) )

def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Controlable Rectangle in Blank Screen')

    clock = pygame.time.Clock()

    character = Character( 300, 200 )

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

        # Move objects ...
        character.update()

        # Draw objects ...
        character.display( screen )

        # Update the screen
        pygame.display.flip()

if __name__ == '__main__':
    main()

