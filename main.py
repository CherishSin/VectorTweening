# Import and initialize the pygame library
import pygame
from pygame.locals import *
from draw_character import draw_character
from load_characters import *
pygame.init()

# Set up the drawing window

clock = pygame.time.Clock()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 500
WIDTH = 720
GAME_HEIGHT = 500
GAME_WIDTH = 720
FPS = 120

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))


def main():
    """
    Main Function
    """
    pygame.display.set_caption("Game")
    game_characters = load_characters('./characters.yaml')
    game(game_characters)


def game(game_characters):
    """
    The game loop
    """
    running = True
    while running:

        #game_characters['dude'].x += 1
        #game_characters['dude'].y += .5
        #game_characters['dude'].roll += 2

        game_characters['lady'].x = 300
        game_characters['lady'].y = 225
        game_characters['lady'].scale = 3.5
        game_characters['lady'].activate_animation('bend', 3)


        # print(test_polygon.translated_coords())
        # draw background
        pygame.draw.rect(game_surface, Color(0, 30, 88), Rect(0, 0, GAME_WIDTH, GAME_HEIGHT))

        draw_character(game_surface, game_characters, 'lady')

        # Do the screen flipping/buffering stuff
        clock.tick(FPS)
        pygame.transform.scale(game_surface, (WIDTH, HEIGHT), display_surface)
        pygame.display.flip()

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()

