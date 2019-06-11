import json

import pygame


class Button:
    def __init__(self, x, y, w, h, text='Hello', is_off=False):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.text = text
        self.is_active = False
        self.is_off = is_off

        self.image = pygame.image.load('../drawable/buttons/red_button.png')
        self.image_active = pygame.image.load('../drawable/buttons/red_button_light.png')
        self.image_off = pygame.image.load('../drawable/buttons/gray_button.png')

        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.image_active = pygame.transform.scale(self.image_active, (self.w, self.h))
        self.image_off = pygame.transform.scale(self.image_off, (self.w, self.h))

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.w+4, self.h+4), 0)

        if self.is_off:
            window.blit(self.image_off, [int(self.x), int(self.y)])
        elif self.is_active:
            window.blit(self.image_active, [int(self.x), int(self.y)])
        else:
            window.blit(self.image, [int(self.x), int(self.y)])

        font = pygame.font.SysFont(None, 42)
        text = font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.x+(self.w/2-text.get_width()/2), self.y+(self.h/2-text.get_height()/2)))

    def is_over(self, pos):  # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                self.is_active = True
                return True
        self.is_active = False
        return False


class TextView:
    def __init__(self, font, color, x, y, text=""):
        self.font = font
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.text = text

        self.COLOR_ACTIVE = (255, 0, 0)
        self.COLOR_INACTIVE = (180, 0, 0)

        self.text_object = self.font.render(self.text, 1, self.color)
        self.rect = self.text_object.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, window):
        self.text_object = self.font.render(self.text, 1, self.color)
        window.blit(self.text_object, self.rect)

    def draw_this(self, window, buffer):
        self.text_object = self.font.render(buffer, 1, self.color)
        window.blit(self.text_object, self.rect)

    def next_line(self, size):
        self.rect.move_ip(0, size+2)

    def is_over(self, pos):  # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.rect.left and pos[0] < self.rect.right:
            if pos[1] > self.rect.top and pos[1] < self.rect.bottom:
                self.color = self.COLOR_ACTIVE
                return True
        self.color = self.COLOR_INACTIVE
        return False


class Player:
    def __init__(self, player_name, score, levels, skins):
        self.name = player_name
        self.score = score
        self.levels = levels
        self.skins = skins

    def save_current_state(self):
        data = dict()
        data["name"] = self.name
        data["score"] = self.score
        data["levels"] = self.levels
        data["skins"] = self.skins
        handler = open("../stats/players/" + self.name + ".json", 'w')
        json.dump(data, handler)
        handler.close()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = (180, 0, 0)  # red colors
        self.COLOR_ACTIVE = (255, 0, 0)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.font = pygame.font.Font(None, 32)  # by default
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if event.key == pygame.K_RETURN:
                #     print(self.text)
                #     self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, window):
        # Blit the text.
        window.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, 2)


# module testing
def main():
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600

    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [1000, 600]
    bg = [255, 255, 255]
    window_surface = pygame.display.set_mode(size)

    screen = pygame.display.set_mode(size)

    image = pygame.image.load('../../drawable/buttons/red_button.png')
    image = pygame.transform.scale(image, (int(WINDOW_WIDTH/3), int(WINDOW_HEIGHT/8)))

    button = Button(image, 50, 100, 50, 100, "test")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.is_over(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

        screen.fill(bg)

        button.draw(window_surface)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    sys.exit(0)


def timer_test():
    pygame.init()
    screen = pygame.display.set_mode((128, 128))
    clock = pygame.time.Clock()

    counter, text = 10, '10'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3) if counter > 0 else 'boom!'
            if e.type == pygame.QUIT: break
        else:
            screen.fill((255, 255, 255))
            screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
            pygame.display.flip()
            clock.tick(60)
            continue
        break


def input_box_test():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    input_box_test()


def load_player_by_path(path):
    handler = open(path, 'r')
    data = json.load(handler)
    player = Player(data['name'], data['score'], data['levels'], data['skins'])
    handler.close()
    return player


def create_empty_profile(nickname):
    handler = open("../stats/players/" + nickname + ".json", 'w')
    data = {"name": nickname, "score": 0, "levels": [1], "skins": [1]}
    json.dump(data, handler)
    handler.close()
