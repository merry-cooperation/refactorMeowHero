import pygame


class Button:
    def __init__(self, image, x, y, w, h, text='Hello'):
        # TODO: send image path, not image
        self.image = image
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.text = text

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.w+4, self.h+4), 0)

        window.blit(self.image, [int(self.x), int(self.y)])

        font = pygame.font.SysFont(None, 42)
        text = font.render(self.text, 1, (0, 0, 0))
        window.blit(text, (self.x+(self.w/2-text.get_width()/2), self.y+(self.h/2-text.get_height()/2)))

    def is_over(self, pos):  # pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        return False


class InputBox:
    pass


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

    button = Button(image, 50, 100, 50, 100, "tesst")

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
    sys.exit


if __name__ == '__main__':
    main()
