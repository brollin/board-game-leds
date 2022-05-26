from util import lerp3

BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
TEAL = (19, 241, 242)
BLUE = (0, 0, 255)
PURPLE = (115, 21, 114)
WHITE = (255, 255, 255)
COLORS = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, WHITE]

class Game:
    mode = 'setup'
    frame = 0
    players = []
    available_colors = COLORS
    new_color_index = 0
    player_turn = -1

    def __init__(self, pixel_config) -> None:
        self.pixel_config = pixel_config

    def blink(self, color):
        """
        Blink a color from off to on via triangle wave over one second
        """
        if self.frame <= self.pixel_config.fps / 2:
            x = self.frame
        else:
            x = self.pixel_config.fps - self.frame
        return lerp3(x, 0, self.pixel_config.fps / 2, BLACK, color)

    def display(self):
        if self.mode == 'setup':
            player_start = 0
            player_width = round(self.pixel_config.count / max(len(self.players) + 1, 4))
            # show colors for players so far
            for player in self.players:
                for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                    self.pixel_config.pixels[i] = player
                player_start += player_width

            # show a blinking new color for the next player
            for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                self.pixel_config.pixels[i] = self.blink(self.available_colors[self.new_color_index])

        elif self.mode == 'start':
            if self.frame == 0:
                # if there are still more players, advance to next player
                if self.player_turn < len(self.players):
                    self.player_turn += 1
                # if no more players, go to run mode
                else:
                    self.mode = 'run'
                    self.player_turn = 0

            for i in range(0, self.pixel_config.count):
                self.pixel_config.pixels[i] = self.blink(self.players[self.player_turn])

        elif self.mode == 'run':
            player_start = 0
            player_width = round(self.pixel_config.count / len(self.players))
            for index, player in enumerate(self.players):
                for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                    self.pixel_config.pixels[i] = self.blink(player) if index == self.player_turn else player
                player_start += player_width
            # TODO make sure that blinking, bright colors are not too annoying

        self.pixel_config.pixels.show()
        self.frame = (self.frame + 1) % self.pixel_config.fps

    def on_short_press(self):
        if self.mode == 'setup':
            self.new_color_index = (self.new_color_index + 1) % len(self.available_colors)
        elif self.mode == 'run':
            self.player_turn = (self.player_turn + 1) % len(self.players)

    def on_long_press(self):
        if self.mode == 'setup':
            self.players.append(self.available_colors[self.new_color_index])
            self.available_colors.pop(self.new_color_index)
            self.new_color_index = 0

            # start the game if we have run out of available colors
            if len(self.available_colors) == 0:
                self.mode = 'start'

    def on_very_long_press(self):
        if self.mode == 'setup':
            self.mode = 'start'
