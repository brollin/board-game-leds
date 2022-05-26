import time
import board
import digitalio
from game import Game
from pixelconfig import PixelConfig

button = digitalio.DigitalInOut(board.GP1)
button.switch_to_input(pull=digitalio.Pull.DOWN)

pixel_config = PixelConfig()
game = Game(pixel_config)

button_down_frames = 0
while True:
    if button.value:
        button_down_frames += 1
        # debugging output
        if button_down_frames % 5 == 0:
            print(button_down_frames)
        if button_down_frames > 90:
            game.on_very_long_press()
            # TODO fix overflow button down frames
            button_down_frames = 0
    else:
        if button_down_frames > 20:
            game.on_long_press()
        elif button_down_frames > 0:
            game.on_short_press()
        button_down_frames = 0

    game.display()
    time.sleep(1 / pixel_config.fps)

