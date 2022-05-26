TEAL = (19, 241, 242)
# BLUE = (59, 94, 166)
PURPLE = (115, 21, 114)
# MAGENTA = (192, 0, 80)
RED = (255, 38, 54)
YELLOW = (255, 170, 26)
COLORS = [TEAL, PURPLE, RED, YELLOW]

class Game:
    mode = 'setup'
    players = []
    new_color_index = 0
    frame = 0

    def __init__(self, pixel_config) -> None:
        self.pixel_config = pixel_config

    def display(self):
        if self.mode == 'setup':
            player_width = round(self.pixel_config.count / max(len(self.players) + 1, 4))
            player_start = 0
            for player in self.players:
                for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                    self.pixel_config.pixels[i] = player
                player_start += player_width

            # show new player to set up
            for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                self.pixel_config.pixels[i] = COLORS[self.new_color_index]
                # TODO make new player blink
                # TODO omit already used colors

        elif self.mode == 'start':
            print('implement start mode')
        elif self.mode == 'run':
            print('implement run mode')

        self.pixel_config.pixels.show()
        self.frame = (self.frame + 1) % self.pixel_config.fps

    def on_short_press(self):
        if self.mode == 'setup':
            self.new_color_index = (self.new_color_index + 1) % len(COLORS)

    def on_long_press(self):
        if self.mode == 'setup':
            self.players.append(COLORS[self.new_color_index])

    def on_very_long_press(self):
        self.mode = 'start' if self.mode == 'setup' else 'run'
