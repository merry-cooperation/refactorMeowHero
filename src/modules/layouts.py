import pygame

from . import interface
from pygame.locals import *

# colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (160, 160, 160)
COLOR_RED = (255, 0, 0)


# return true if quit
def interruption_menu(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    pygame.mouse.set_visible(True)
    button_continue = interface.Button(WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 4,
                                     WINDOW_WIDTH / 3, WINDOW_HEIGHT / 8, "Continue")
    button_quit = interface.Button(WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2,
                                  WINDOW_WIDTH / 3, WINDOW_HEIGHT / 8, "Quit")

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    return False

            if button_continue.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_visible(False)
                    return False

            if button_quit.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            # я заебался это под экран подгонять
            pygame.draw.rect(window_surface, COLOR_BLACK,
                             (WINDOW_WIDTH / 2 + 100 - 5, WINDOW_HEIGHT / 5 - 5, WINDOW_WIDTH / 3 + 10, WINDOW_HEIGHT / 2 + 10))
            pygame.draw.rect(window_surface, COLOR_GREY,
                             (WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/5, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2))

            button_continue.draw(window_surface)
            button_quit.draw(window_surface)

            pygame.display.update()
