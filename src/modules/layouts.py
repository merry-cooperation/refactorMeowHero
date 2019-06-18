import json
import os
import random

import pygame
from pygame.locals import *

from . import interface

"""
Здесь рисую маленькие всплывающие окна
Сначала отрисовывается рамка, потом окно, потом кнопки
И прочее содержимое
"""

# colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BRIGHT_GREY = (200, 200, 200)
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

            pygame.draw.rect(window_surface, COLOR_BLACK,
                             (WINDOW_WIDTH / 2 + 100 - 5, WINDOW_HEIGHT / 5 - 5,
                              WINDOW_WIDTH / 3 + 10, WINDOW_HEIGHT / 2 + 10))
            pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY,
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
        pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY,
                         (WINDOW_WIDTH / 2 - 260, WINDOW_HEIGHT / 5 - 50, WINDOW_WIDTH / 3, 3*WINDOW_HEIGHT / 4))

        for elem in drawable:
            elem.draw(window_surface)

        button_close.draw(window_surface)

        pygame.display.update()


def victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):

    rect = pygame.Rect((0, 0), (2*WINDOW_WIDTH/3, 2*WINDOW_HEIGHT/3))
    rect_border = pygame.Rect((0, 0), (2*WINDOW_WIDTH/3+10, 2*WINDOW_HEIGHT/3+10))
    rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    rect_border.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

    font0 = pygame.font.SysFont(None, 140)
    text_victory = interface.TextView(font0, COLOR_BLACK, 150, 2*WINDOW_HEIGHT / 6, "Congratulations!")
    text_victory.rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    text_victory.draw(window_surface)

    # TODO: draw another information here

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def defeat_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    font0 = pygame.font.SysFont(None, 200)
    font1 = pygame.font.SysFont(None, 80)
    text_view_message = interface.TextView(font0, COLOR_WHITE, 150, 2*WINDOW_HEIGHT / 6,
                                           "Game over, bro =(")
    text_view_message.draw(window_surface)
    text_view_press_esc = interface.TextView(font1, COLOR_WHITE, WINDOW_WIDTH / 2 - 200, 3*WINDOW_HEIGHT / 5,
                                             "Press ESC to exit...")
    text_view_press_esc.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


# returning player
def create_profile_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT):
    player.save_current_state()
    clock = pygame.time.Clock()

    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    input_box = interface.InputBox(WINDOW_WIDTH/4, 4*WINDOW_HEIGHT/8, 220, 80)

    font0 = pygame.font.SysFont(None, 100)
    font1 = pygame.font.SysFont(None, 78)
    input_box.font = font1

    text_write_name = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Write your name here")
    text_write_name.rect.center = (WINDOW_WIDTH / 2, 2*WINDOW_HEIGHT / 5)

    button_done = interface.Button(2*WINDOW_WIDTH / 3, 4*WINDOW_HEIGHT / 8,
                                   WINDOW_WIDTH / 15, WINDOW_HEIGHT / 10, "Done")
    done = False
    while not done:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                done = True

            if button_done.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(input_box.text)
                    name = input_box.text.strip()
                    if not name:
                        done = True
                        continue
                    path = '../stats/players/' + name + '.json'
                    if os.path.isfile(path):
                        print("Exist")
                        player = interface.load_player_by_path(path)
                    else:
                        print("Not exist")
                        interface.create_empty_profile(name)
                        player = interface.load_player_by_path(path)
                    input_box.text = ''
                    done = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == pygame.K_RETURN:  # if enter
                    print(input_box.text)
                    name = input_box.text.strip()
                    if not name:
                        done = True
                        continue
                    path = '../stats/players/' + name + '.json'
                    if os.path.isfile(path):
                        print("Exist")
                        player = interface.load_player_by_path(path)
                    else:
                        print("Not exist")
                        interface.create_empty_profile(name)
                        player = interface.load_player_by_path(path)
                    input_box.text = ''
                    done = True

            input_box.handle_event(event)

        input_box.update()

        pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
        pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

        text_write_name.draw(window_surface)
        input_box.draw(window_surface)
        button_done.draw(window_surface)

        pygame.display.update()

        clock.tick(30)

    return player


def change_skin_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 100)
    text_skins = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Will be able later")
    text_skins.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    text_skins.draw(window_surface)

    # TODO: icons here pls

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def future_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 100)
    text_future = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Will be able later")
    text_future.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    text_future.draw(window_surface)

    # TODO: ???

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def two_players_victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, score, time):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 80)
    text_victory = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Nice game!")
    text_victory.rect.center = (WINDOW_WIDTH / 2, 2*WINDOW_HEIGHT / 8)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    handler = open("../stats/multiplayer_score.json", 'r')
    data = json.load(handler)
    handler.close()

    text_victory.draw(window_surface)

    score_and_time_text = interface.TextView(font1, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6)
    score_and_time_text.rect.center = (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 3 + 30)

    score_and_time_text.draw_this(window_surface, "Your score is " + str(score))
    score_and_time_text.next_line(82)
    score_and_time_text.draw_this(window_surface, "Your time is " + str(time))
    score_and_time_text.next_line(82)

    handler = open("../stats/multiplayer_score.json", 'w')

    if score > data["Top score"] and time > data["Top time"]:
        score_and_time_text.draw_this(window_surface, "New top score and time!")
        data["Top score"] = score
        data["Top time"] = time
    elif score > data["Top score"]:
        score_and_time_text.draw_this(window_surface, "New top score!")
        data["Top score"] = score
    elif time > data["Top time"]:
        score_and_time_text.draw_this(window_surface, "New top time!")
        data["Top time"] = time

    json.dump(data, handler)
    handler.close()

    score_and_time_text.next_line(82)
    score_and_time_text.draw_this(window_surface, "Top score: " + str(data["Top score"]))
    score_and_time_text.next_line(82)
    score_and_time_text.draw_this(window_surface, "Top time: " + str(data["Top time"]))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def giving_port_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    port = random.randint(10000, 14000)

    font0 = pygame.font.SysFont(None, 140)
    text_victory = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Your port is " + str(port))
    text_victory.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    pygame.display.update()

    button_done = interface.Button(2 * WINDOW_WIDTH / 3, 5 * WINDOW_HEIGHT / 8 + 60,
                                   WINDOW_WIDTH / 6, WINDOW_HEIGHT / 8, "We are ready!")

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                exit(0)
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return port

            if button_done.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return port

            pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
            pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

            text_victory.draw(window_surface)

            button_done.draw(window_surface)
            pygame.display.update()
