import json
import os
import random
import pygame
from pygame.locals import *
from time import sleep

from . import interface
from modules.display_config import WINDOW_WIDTH, WINDOW_HEIGHT, COLOR_BLACK, COLOR_BRIGHT_GREY, COLOR_RED, COLOR_WHITE, \
    COLOR_BLUE

"""
Здесь рисую маленькие всплывающие окна
Сначала отрисовывается рамка, потом окно, потом кнопки
И прочее содержимое
"""


# return true if quit
def interruption_menu(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    pygame.mouse.set_visible(True)
    button_continue = interface.Button((WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 4,
                                        WINDOW_WIDTH / 3, WINDOW_HEIGHT / 8), "Continue")
    button_quit = interface.Button((WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2,
                                    WINDOW_WIDTH / 3, WINDOW_HEIGHT / 8), "Quit")

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
                             (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 5, WINDOW_WIDTH / 3, WINDOW_HEIGHT / 2))

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
        text_view = interface.TextView(font, COLOR_BLACK, WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 5 + i * 48,
                                       data[str(i + 1)][0] + "    " + str(data[str(i + 1)][1]))
        drawable.append(text_view)

    button_close = interface.Button(
        (WINDOW_WIDTH / 2 - 260 + WINDOW_WIDTH / 3 - WINDOW_WIDTH / 20, WINDOW_HEIGHT / 5 - 50,
         WINDOW_WIDTH / 20, WINDOW_HEIGHT / 20), "x")

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
                         (WINDOW_WIDTH / 2 - 268, WINDOW_HEIGHT / 5 - 58, WINDOW_WIDTH / 3 + 16,
                          3 * WINDOW_HEIGHT / 4 + 16))
        pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY,
                         (WINDOW_WIDTH / 2 - 260, WINDOW_HEIGHT / 5 - 50, WINDOW_WIDTH / 3, 3 * WINDOW_HEIGHT / 4))

        for elem in drawable:
            elem.draw(window_surface)

        button_close.draw(window_surface)

        pygame.display.update()


def victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, boss, score, new_record, new_skin):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 80)
    font2 = pygame.font.SysFont(None, 60)

    text_victory = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Level complete!")
    text_victory.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)

    if boss:
        text_formula = interface.TextView(font1, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6,
                                          "Score = (score+life*1000)*100/time")
    else:
        text_formula = interface.TextView(font1, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Score = score + life*1000")

    text_formula.rect.topleft = (WINDOW_WIDTH / 4 - 70, WINDOW_HEIGHT / 3 + 60)

    text_press_esc = interface.TextView(font2, COLOR_WHITE, 150, 2 * WINDOW_HEIGHT / 6, "Press ESC to continue")
    text_press_esc.rect.center = (4 * WINDOW_WIDTH / 5, 8 * WINDOW_HEIGHT / 9)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    text_victory.draw(window_surface)
    text_formula.draw(window_surface)
    text_formula.next_line(90)
    text_formula.draw_this(window_surface, "Your score is " + str(score))

    if new_record:
        sleep(0.5)
        new_top_sound = pygame.mixer.Sound('../sound/short_tracks/health.wav')
        new_top_sound.play()
        text_formula.color = COLOR_RED
        text_formula.next_line(100)
        text_formula.draw_this(window_surface, "New level record!")

    if new_skin:
        sleep(0.5)
        text_formula.color = COLOR_BLUE
        text_formula.next_line(100)
        text_formula.draw_this(window_surface, "New skin available!")

    text_press_esc.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def defeat_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    font0 = pygame.font.SysFont(None, 200)
    font1 = pygame.font.SysFont(None, 80)
    text_view_message = interface.TextView(font0, COLOR_WHITE, 150, 2 * WINDOW_HEIGHT / 6,
                                           "Game over, bro =(")
    text_view_message.draw(window_surface)
    text_view_press_esc = interface.TextView(font1, COLOR_WHITE, WINDOW_WIDTH / 2 - 200, 3 * WINDOW_HEIGHT / 5,
                                             "Press ESC to exit...")
    text_view_press_esc.draw(window_surface)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return


def get_player_record(name):
    path = '../stats/players/' + name + '.json'
    if os.path.isfile(path):
        print("Exist")
        return interface.load_player_by_path(path)
    else:
        print("Not exist")
        interface.create_empty_profile(name)
        return interface.load_player_by_path(path)


def process_input_finish(input_box, player):
    print(input_box.text)
    name = input_box.text.strip()
    if not name:
        done = True
        return done, player
    player = get_player_record(name)
    input_box.text = ''
    done = True
    return done, player


def create_profile_interface_elements(win_w, win_h):
    rect = pygame.Rect((0, 0), (2 * win_w / 3, win_h / 3))
    rect_border = pygame.Rect((0, 0), (2 * win_w / 3 + 10, win_h / 3 + 10))
    rect.center = (win_w / 2, win_h / 2)
    rect_border.center = (win_w / 2, win_h / 2)

    input_box = interface.InputBox((win_w / 4, 4 * win_h / 8, 220, 80))

    font0 = pygame.font.SysFont(None, 100)
    font1 = pygame.font.SysFont(None, 78)
    input_box.font = font1

    text_write_name = interface.TextView(font0, COLOR_BLACK, 150, 2 * win_h / 6, "Write your name here")
    text_write_name.rect.center = (win_w / 2, 2 * win_h / 5)

    button_done = interface.Button((2 * win_w / 3, 4 * win_h / 8,
                                    win_w / 15, win_h / 10), "Done")

    return rect, rect_border, input_box, text_write_name, button_done


# returning player
def create_profile_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT):
    player.save_current_state()
    clock = pygame.time.Clock()

    rect, rect_border, input_box, text_write_name, button_done = create_profile_interface_elements(WINDOW_WIDTH,
                                                                                                   WINDOW_HEIGHT)

    done = False
    while not done:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                done = True

            if button_done.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done, player = process_input_finish(input_box, player)

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == pygame.K_RETURN:  # if enter
                    done, player = process_input_finish(input_box, player)

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


# returning player
def change_skin_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 120)

    text_title = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Select skin")
    text_title.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)

    skin_levels = [1, 6, 8, 9, 10, 12]
    buttons = list()

    for i, skin in enumerate(skin_levels):
        if skin in player.skins:
            button = interface.Button((WINDOW_WIDTH / 5 + (i % 3) * (WINDOW_WIDTH / 6 + 40) + 50,
                                       WINDOW_HEIGHT / 3 + int(i / 3) * (WINDOW_HEIGHT / 8 + 70),
                                       WINDOW_WIDTH / 8, WINDOW_HEIGHT / 6), str(skin))
            button.font = pygame.font.SysFont(None, 64)
        else:
            button = interface.Button((WINDOW_WIDTH / 5 + (i % 3) * (WINDOW_WIDTH / 6 + 40) + 50,
                                       WINDOW_HEIGHT / 3 + int(i / 3) * (WINDOW_HEIGHT / 8 + 70),
                                       WINDOW_WIDTH / 8, WINDOW_HEIGHT / 6), str(skin), True)
            button.font = pygame.font.SysFont(None, 64)

        buttons.append(button)

    while True:
        mouse_pos = pygame.mouse.get_pos()  # gets mouse position
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return player

        for button in buttons:
            if button.is_over(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN and not button.is_off:
                    player.current_skin = int(button.text)
                    print("Current skin is", player.current_skin)
                    return player

        pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
        pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

        text_title.draw(window_surface)

        for button in buttons:
            button.draw(window_surface)

        pygame.display.update()


def credits_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 120)
    font1 = pygame.font.SysFont(None, 70)
    text_title = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Developers")
    text_title.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)

    pygame.draw.rect(window_surface, COLOR_BLACK, rect_border)
    pygame.draw.rect(window_surface, COLOR_BRIGHT_GREY, rect)

    text_title.draw(window_surface)

    text_future = interface.TextView(font1, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6)
    text_future.rect.center = (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 3)

    text_future.next_line(82)
    text_future.draw_this(window_surface, "Vladislav Cepelev (teamlead)")
    text_future.next_line(82)
    text_future.draw_this(window_surface, "Alexander Zorkin (programmer)")
    text_future.next_line(82)
    text_future.draw_this(window_surface, "Rufina Rafikova (programmer/storywriter)")
    text_future.next_line(82)
    text_future.draw_this(window_surface, "Anastasia Politova (game designer)")

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYUP:
                return
            if event.type == MOUSEBUTTONDOWN:
                return


def two_players_victory_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT, score, time):
    rect = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3, 2 * WINDOW_HEIGHT / 3))
    rect_border = pygame.Rect((0, 0), (2 * WINDOW_WIDTH / 3 + 10, 2 * WINDOW_HEIGHT / 3 + 10))
    rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    rect_border.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    font0 = pygame.font.SysFont(None, 140)
    font1 = pygame.font.SysFont(None, 80)
    font2 = pygame.font.SysFont(None, 60)

    text_victory = interface.TextView(font0, COLOR_BLACK, 150, 2 * WINDOW_HEIGHT / 6, "Nice game!")
    text_victory.rect.center = (WINDOW_WIDTH / 2, 2 * WINDOW_HEIGHT / 8)

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

    score_and_time_text.color = COLOR_RED
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
    score_and_time_text.color = COLOR_BLACK

    json.dump(data, handler)
    handler.close()

    score_and_time_text.next_line(82)
    score_and_time_text.draw_this(window_surface, "Top score: " + str(data["Top score"]))
    score_and_time_text.next_line(82)
    score_and_time_text.draw_this(window_surface, "Top time: " + str(data["Top time"]))

    text_press_esc = interface.TextView(font2, COLOR_WHITE, 150, 2 * WINDOW_HEIGHT / 6, "Press ESC to exit")
    text_press_esc.rect.center = (4 * WINDOW_WIDTH / 5, 7 * WINDOW_HEIGHT / 8)
    text_press_esc.draw(window_surface)

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

    button_done = interface.Button((2 * WINDOW_WIDTH / 3, 5 * WINDOW_HEIGHT / 8 + 60,
                                    WINDOW_WIDTH / 6, WINDOW_HEIGHT / 8), "We are ready!")

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
