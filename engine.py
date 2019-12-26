import sys
import pygame


class Engine():
    def __init__(self, title):
        """
        Default constructor for Engine class, handles pygame window
        and rendering
        """

        self.handle_sysargs()
        self.init(title)

    def handle_sysargs(self):
        """
        Sets game class variables to the values based on any cli clags
        """

        # init all sys args to their defaults
        self.debug_mode = False
        self.show_fps = False

        # loop through received sys args and set values as needed
        for argument in sys.argv:
            if argument == "--debug":
                self.debug_mode = True
                self.show_fps = True

    def init(self, title):
        """
        Initializes pygame
        """

        # Init basic engine variables
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.TITLE = title
        self.TARGET_FPS = 60

        # Color constants
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        # Init the font and image cache
        self.font_cache = {}
        self.text_cache = {}
        self.image_cache = {}

        # Init pygame
        pygame.init()
        pygame_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if self.debug_mode:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame_flags)
        else:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame_flags | pygame.FULLSCREEN)
        self.display = pygame.Surface((1280, 720))
        self.clock = pygame.time.Clock()

        # Init timing variables
        self.fps = 0
        self.frames = 0
        self.delta = 0
        self.SECOND = 1000
        self.UPDATE_TIME = self.SECOND / self.TARGET_FPS
        self.before_time = pygame.time.get_ticks()
        self.before_sec = self.before_time

    def tick(self):
        after_time = pygame.time.get_ticks()
        self.delta = (after_time - self.before_time) / self.UPDATE_TIME

        if after_time - self.before_sec >= self.SECOND:
            self.fps = self.frames
            self.frames = 0
            self.before_sec += self.SECOND
        self.before_time = pygame.time.get_ticks()

        # self.clock.tick(self.TARGET_FPS)
        self.clock.tick(0)

    """
    Rendering Functions
    Many of these are really redundant because they serve as wrappers for already
    simple functions, but it serves the greater purpose of keeping a lot of the
    extra pygame code out of the way, so that the main class only focuses on the
    basic logic of the game itself
    """

    def clear_screen(self):
        pygame.draw.rect(self.display, self.BLACK, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), False)

    def flip_buffer(self):
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()
        self.frames += 1

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.display, color, rect, True)

    def fill_rect(self, color, rect):
        # pygame.draw.rect(self.screen, color, rect, False)
        pygame.draw.rect(self.display, color, (int(rect[0]), int(rect[1]), rect[2], rect[3]))

    def fill_rect_transparent(self, color, alpha, rect):
        s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        s.fill((color[0], color[1], color[2], alpha))
        self.display.blit(s, (rect[0], rect[1]))

    def draw_circle(self, color, center, radius, width):
        pygame.draw.circle(self.display, color, center, radius, width)

    def render_text(self, text, pos, size=14, color=(255, 255, 255)):
        """
        Renders text to the screen
        pos = (x, y) and if x and y = "CENTERED" then we center the text on that axis
        """

        # If the font / text object for the passed string isn't in the cache, make it
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.SysFont("Serif", size)
        # This variable prevents us from using the same text object for the same string at a different size
        text_id = text + "&sz=" + str(size) + "&colo=" + str(color)
        if text_id not in self.text_cache:
            self.text_cache[text_id] = self.font_cache[size].render(text, False, color)

        draw_x = 0
        draw_y = 0

        if pos[0] == "CENTERED":
            draw_x = (self.SCREEN_WIDTH / 2) - (self.text_cache[text_id].get_rect().w / 2)
        else:
            draw_x = pos[0]
        if pos[1] == "CENTERED":
            draw_y = (self.SCREEN_HEIGHT / 2) - (self.text_cache[text_id].get_rect().h / 2)
        else:
            draw_y = pos[1]

        self.display.blit(self.text_cache[text_id], (draw_x, draw_y))

    def render_image(self, shortname, pos, alpha=False):
        """
        Renders an image to the screen
        pos = (x, y) and if x and y = "CENTERED" then we center the image on that axis
        """

        # If the image for the passed string isn't in the cache, load it
        if shortname not in self.image_cache:
            if alpha:
                self.image_cache[shortname] = pygame.image.load("res/" + shortname + ".png").convert_alpha()
            else:
                self.image_cache[shortname] = pygame.image.load("res/" + shortname + ".png").convert()

        draw_x = 0
        draw_y = 0

        if pos[0] == "CENTERED":
            draw_x = (self.SCREEN_WIDTH / 2) - (self.image_cache[shortname].get_rect().w / 2)
        else:
            draw_x = pos[0]
        if pos[1] == "CENTERED":
            draw_y = (self.SCREEN_HEIGHT / 2) - (self.image_cache[shortname].get_rect().h / 2)
        else:
            draw_y = pos[1]

        draw_x = int(draw_x)
        draw_y = int(draw_y)

        self.display.blit(self.image_cache[shortname], (draw_x, draw_y))

    def render_fps(self):
        if self.show_fps:
            self.render_text("FPS: " + str(self.fps), (0, 0))

    def quit(self):
        """
        It quits the game
        """
        pygame.quit()
