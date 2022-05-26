from util import lerp3

BLACK = (0, 0, 0)
TEAL = (19, 241, 242)
# BLUE = (59, 94, 166)
PURPLE = (115, 21, 114)
# MAGENTA = (192, 0, 80)
RED = (255, 38, 54)
YELLOW = (255, 170, 26)
COLORS = [TEAL, PURPLE, RED, YELLOW]

class Game:
    mode = 'setup'
    frame = 0
    players = []
    available_colors = COLORS
    new_color_index = 0

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
            # TODO
            # TODO when finished transitions to run mode
            pass
        elif self.mode == 'run':
            # TODO
            pass

        self.pixel_config.pixels.show()
        self.frame = (self.frame + 1) % self.pixel_config.fps

    def on_short_press(self):
        if self.mode == 'setup':
            self.new_color_index = (self.new_color_index + 1) % len(self.available_colors)

    def on_long_press(self):
        if self.mode == 'setup':
            self.players.append(self.available_colors[self.new_color_index])
            self.available_colors.pop(self.new_color_index)
            self.new_color_index = 0

    def on_very_long_press(self):
        if self.mode == 'setup':
            self.mode = 'start'
