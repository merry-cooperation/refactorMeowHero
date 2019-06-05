import pygame
import json

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


def stats_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    font = pygame.font.SysFont(None, 46)
    drawable = list()

    handler = open("../stats/high_score.json", 'r')
    data = json.load(handler)
    handler.close()

    for i in range(len(data)):
        text_view = interface.TextView(font, COLOR_BLACK, WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 5 + i*48,
                                       data[str(i+1)][0] + "    " + str(data[str(i+1)][1]))
        drawable.append(text_view)

    button_close = interface.Button(WINDOW_WIDTH / 2 - 260 + WINDOW_WIDTH / 3 - WINDOW_WIDTH / 20, WINDOW_HEIGHT / 5 - 50,
                              WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20, "x")

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return

            if button_close.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

        pygame.draw.rect(window_surface, COLOR_BLACK,
                         (WINDOW_WIDTH / 2 - 268, WINDOW_HEIGHT / 5 - 58, WINDOW_WIDTH / 3+16, 3 * WINDOW_HEIGHT / 4+16))
        pygame.draw.rect(window_surface, COLOR_GREY,
                         (WINDOW_WIDTH / 2 - 260, WINDOW_HEIGHT / 5 - 50, WINDOW_WIDTH / 3, 3*WINDOW_HEIGHT / 4))

        for elem in drawable:
            elem.draw(window_surface)

        button_close.draw(window_surface)

        pygame.display.update()
