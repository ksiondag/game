import pygame
import sys

BLACK = 0, 0, 0
WHITE = 255, 255, 255

class Character:
    
    def __init__( self, x, y ):
        '''
        '''
        self.pos_x = x
        self.pos_y = y

        self.tar_x = x
        self.tar_y = y

        self.vel_x = 0
        self.vel_y = 0

        self.acc_x = 0
        self.acc_y = 0

    def move_event( self, target_location ):
        '''
        '''
        self.tar_x, self.tar_y = target_location

        distance = (self.tar_x - self.pos_x)**2 + (self.tar_y - self.pos_y)**2
        distance = distance**0.5

        self.vel_x = 10*(self.tar_x - self.pos_x)/distance
        self.vel_y = 10*(self.tar_y - self.pos_y)/distance

    def update( self ):
        '''
        '''
        if self.vel_x != 0 and self.tar_x != self.pos_x:
            distance_x = (self.tar_x - self.pos_x) > 0
            velocity_x  = self.vel_x > 0

            if distance_x == velocity_x:
                self.pos_x += self.vel_x
            else:
                self.pos_x = self.tar_x
        else:
            self.vel_x = 0

        if self.vel_y != 0 and self.tar_y != self.pos_y:
            distance_y = (self.tar_y - self.pos_y) > 0
            velocity_y  = self.vel_y > 0

            if distance_y == velocity_y:
                self.pos_y += self.vel_y
            else:
                self.pos_y = self.tar_y
        else:
            self.vel_y = 0

    def display( self, screen ):
        '''
        '''
        pygame.draw.rect( screen, WHITE, (self.pos_x, self.pos_y, 20, 20) )

def main():
    '''
    '''
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Render Rectangle in Blank Fucking Screen')

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

        # Update the scren
        pygame.display.flip()

if __name__ == '__main__':
    main()

