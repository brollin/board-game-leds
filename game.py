from util import dim, lerp3

BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 200, 0)
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

        # uncomment to start in run mode
        # self.mode = 'run'
        # self.players = [TEAL, PURPLE, ORANGE, WHITE]
        # self.player_turn = 0

    def set_mode(self, mode):
        self.mode = mode
        self.frame = 0

    def blink(self, color, offset=-15):
        """
        Blink a color from off to on via triangle wave over one second. offset: 0 means it will go
        from black to full color. A negative number means it will start from a partial color and go
        to a full color
        """
        if self.frame <= self.pixel_config.fps / 2:
            x = self.frame
        else:
            x = self.pixel_config.fps - self.frame
        return lerp3(x, offset, self.pixel_config.fps / 2, BLACK, color)

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
            player_end = min(player_start + player_width, self.pixel_config.count) if len(self.players) < 4 else self.pixel_config.count
            for i in range(player_start, player_end):
                self.pixel_config.pixels[i] = self.blink(self.available_colors[self.new_color_index])

        elif self.mode == 'start':
            # TODO fancier start
            if self.frame == 0:
                # if there are still more players, advance to next player
                if self.player_turn < len(self.players) - 1:
                    self.player_turn += 1
                # if no more players, go to run mode
                else:
                    self.set_mode('run')
                    self.player_turn = 0
                    return

            for i in range(0, self.pixel_config.count):
                self.pixel_config.pixels[i] = self.blink(self.players[self.player_turn], offset=0)

        elif self.mode == 'run':
            # TODO fancier run. expand color of current player
            player_start = 0
            player_width = round(self.pixel_config.count / len(self.players))
            for index, player in enumerate(self.players):
                for i in range(player_start, min(player_start + player_width, self.pixel_config.count)):
                    if index == self.player_turn:
                        self.pixel_config.pixels[i] = self.blink(player)
                    else:
                        self.pixel_config.pixels[i] = dim(player, 0.5)
                player_start += player_width

        elif self.mode == 'fanfare':
            # TODO implement
            # TODO when done go to setup mode
            pass

        self.pixel_config.pixels.show()
        self.frame = (self.frame + 1) % self.pixel_config.fps

    def on_short_press(self):
        if self.mode == 'setup':
            # setup mode short press advances color
            self.new_color_index = (self.new_color_index + 1) % len(self.available_colors)
            self.frame = 0
        elif self.mode == 'run':
            # run mode short press advances the turn to the next player
            self.player_turn = (self.player_turn + 1) % len(self.players)
            self.frame = 0

    def on_long_press(self):
        if self.mode == 'setup':
            # setup mode long press selects color
            self.players.append(self.available_colors[self.new_color_index])
            self.available_colors.pop(self.new_color_index)
            self.new_color_index = 0

            # start the game if we have run out of available colors
            if len(self.available_colors) == 0:
                self.set_mode('start')

        elif self.mode == 'run':
            # run mode long press goes to previous player's turn
            self.player_turn = (self.player_turn - 1) % len(self.players)

    def on_very_long_press(self):
        if self.mode == 'setup':
            # setup mode very long press exits setup mode
            self.set_mode('start')

        elif self.mode == 'run':
            # run mode very long press goes to fanfare mode
            self.set_mode('fanfare')
