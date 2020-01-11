import pygame

from modules import interface, layouts, client, game
from pygame.locals import *

# constants
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900

# constant BG
background_image_main = pygame.image.load("../drawable/backgrounds/main_menu5.jpg")
background_image_main = pygame.transform.scale(background_image_main, (WINDOW_WIDTH, WINDOW_HEIGHT))
background_image_levels = pygame.image.load("../drawable/backgrounds/main_menu5.jpg")
background_image_levels = pygame.transform.scale(background_image_levels, (WINDOW_WIDTH, WINDOW_HEIGHT))

# colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BRIGHT_GREY = (200, 200, 200)
COLOR_RED = (255, 0, 0)


def init_window(full_screen=False):  # set up pygame, the window, and the mouse cursor
    pygame.init()

    if full_screen:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
    else:
        window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    window_surface.blit(background_image_main, [0, 0])
    pygame.display.set_caption('Meow Hero')

    return window_surface


def draw_level_buttons(window_surface, player):
    buttons = list()

    for i in range(12):
        x = WINDOW_WIDTH / 2 + (i % 3) * (WINDOW_WIDTH / 8 + 40) + 50
        y = WINDOW_HEIGHT / 12 + int(i / 3) * (WINDOW_HEIGHT / 8 + 70)
        w, h = WINDOW_WIDTH / 8, WINDOW_HEIGHT / 6
        if i + 1 in player.levels:
            button = interface.Button((x, y, w, h), str(i + 1))
        else:
            button = interface.Button((x, y, w, h), str(i + 1), True)

        button.font = pygame.font.SysFont(None, 64)
        buttons.append(button)

    button_back = interface.Button((20, 20, WINDOW_WIDTH / 10, WINDOW_HEIGHT / 10), "Back")
    buttons.append(button_back)

    return buttons


def levels_menu(window_surface, player):
    buttons = draw_level_buttons(window_surface, player)

    boss_levels = [1, 4, 5, 6, 7, 9, 10, 12]

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()  # gets mouse position
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return

            if event.type == QUIT:
                print("Goodbye")
                game.terminate(player)

            for button in buttons:
                if button.is_over(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN and not button.is_off:
                        if button.text == "Back":
                            return
                        # print story
                        game.story_loop(window_surface, int(button.text), "pre", player)

                        # start game
                        if int(button.text) in boss_levels:
                            victory = game.boss_game_loop(window_surface, int(button.text), player)
                        else:
                            victory = game.game_loop(window_surface, int(button.text), player)

                        # print post-story
                        if victory:
                            game.story_loop(window_surface, int(button.text), "post", player)
                            buttons = draw_level_buttons(window_surface, player)

            window_surface.blit(background_image_levels, [0, 0])

            for button in buttons:
                button.draw(window_surface)

            pygame.display.update()


def main_menu(window_surface):  # show the "Main menu" screen
    # preparing text
    font_0 = pygame.font.SysFont("rachana", 140)

    font_1 = pygame.font.SysFont(None, 78)
    font_2 = pygame.font.SysFont(None, 42)

    # loading last player
    handler = open("../stats/last_player.txt", 'r')
    player_name = handler.read().strip()
    handler.close()

    # loading player info
    try:
        player = interface.load_player_by_path("../stats/players/" + player_name + ".json")
    except FileNotFoundError:
        player = interface.load_player_by_path("../stats/players/" + "Test Player" + ".json")

    # creating text and buttons
    greeting_text = interface.TextView(font_1, COLOR_BLACK, 15, 15, "Hello, " + player_name + "!")
    game_title_text = interface.TextView(font_0, COLOR_BLACK, WINDOW_WIDTH / 2, 50, "MEOW HERO")
    not_you_text_button = interface.TextView(font_2, COLOR_RED, WINDOW_WIDTH / 5, 90, "Not you, dude?")

    x = WINDOW_WIDTH / 2 + 100
    y_single, y_two, y_quit = WINDOW_HEIGHT / 4, WINDOW_HEIGHT / 2, 3 * WINDOW_HEIGHT / 4
    w, h = WINDOW_WIDTH / 3, WINDOW_HEIGHT / 8

    button_single = interface.Button((x, y_single, w, h), "1 Player")
    button_two = interface.Button((x, y_two, w, h), "2 Players")
    button_quit = interface.Button((x, y_quit, w, h), "Quit")

    button_stats = interface.Button((50, 140, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 7), "Stats")
    button_skins = interface.Button((260, 140, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 7), "Skins")
    button_future = interface.Button((470, 140, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 7), "Info")

    drawable = list()
    drawable.append(greeting_text)
    drawable.append(game_title_text)
    drawable.append(not_you_text_button)
    drawable.append(button_quit)
    drawable.append(button_two)
    drawable.append(button_single)
    drawable.append(button_stats)
    drawable.append(button_skins)
    drawable.append(button_future)

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                print("Goodbye")
                game.terminate(player)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    game.terminate(player)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_single.is_over(mouse_pos):
                    levels_menu(window_surface, player)
                elif button_two.is_over(mouse_pos):
                    client.two_players_mode(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
                elif button_quit.is_over(mouse_pos):
                    game.terminate(player)
                elif not_you_text_button.is_over(mouse_pos):
                    player = layouts.create_profile_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT)
                    greeting_text.text = "Hello, " + player.name + "!"
                elif button_stats.is_over(mouse_pos):
                    layouts.stats_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)
                elif button_skins.is_over(mouse_pos):
                    player = layouts.change_skin_layout(window_surface, player, WINDOW_WIDTH, WINDOW_HEIGHT)
                elif button_future.is_over(mouse_pos):
                    # I don't know why I need this button
                    layouts.future_layout(window_surface, WINDOW_WIDTH, WINDOW_HEIGHT)

        # drawing objects
        window_surface.blit(background_image_main, [0, 0])
        for elem in drawable:
            elem.draw(window_surface)

        pygame.display.update()


def main():
    while True:
        window = init_window(True)  # True if fullscreen
        main_menu(window)


if __name__ == "__main__":
    main()
