import random
from util import brightness_adjust, fade, mult_rgb
from neopixel import NeoPixel

class TrailEffect:
    def __init__(self, increment = 5):
        self.t = 0
        self.increment = increment

    def step(self, pixels: NeoPixel, brightness: float):
        pixels[0] = brightness_adjust(fade(self.t), brightness)
        self.t += self.increment

        for i in reversed(range(1, len(pixels))):
            pixels[i] = pixels[i - 1]
    
    def get_name(self):
        return 'Trail'

class FireEffect:
    def __init__(self, n_cols: int, n_per_col: int, fire_spread: float = 3.5) -> None:
        self.t = 0
        
        self.n_cols = n_cols
        self.n_per_col = n_per_col
        self.fire_spread = fire_spread

    def step(self, pixels: NeoPixel, brightness: float):
        # Generate random "firey" looking colors for each pixel in each column
        for col in range(0, self.n_cols):
            pixels[col*self.n_per_col] = brightness_adjust(fade(random.randint(5, 30)), brightness)
        
        # Shift all leds up in each column
        for col in range(0, self.n_cols):
            for i in reversed(range(self.n_per_col*col+1, self.n_per_col*(col+1))):
                # Still might use later
                # row = (i - self.n_per_col*col) / self.n_per_col

                #           Slowly make the pixels dimmer to mimic fire
                pixels[i] = mult_rgb(pixels[i - 1], .95)

        for col in range(0, self.n_cols):
            # Start and end index for the for loop
            start_index = col*self.n_per_col
            end_index = (col+1)*self.n_per_col

            for i in range(start_index, end_index):
                # The chance of the led getting turned off increases as you go up
                chance = (i - start_index) / self.n_per_col

                # Random chance part
                if chance > random.random() * self.fire_spread:
                    pixels[i] = (0, 0, 0)

    def get_name(self):
        return 'Fire'
    
class RainbowEffect:
    def __init__(self, n_cols: int, n_per_col: int, increment: int = 5) -> None:
        self.t = 0
        
        self.n_cols = n_cols
        self.n_per_col = n_per_col
        self.increment = increment

    def step(self, pixels: NeoPixel, brightness: float):
        # Generate rainbow colors in the first pixel of each column
        for col in range(0, self.n_cols):
            pixels[col*self.n_per_col] = brightness_adjust(fade(self.t), brightness)

        # Increment the hue
        self.t += self.increment
        
        # Shift the leds in each column up
        for col in range(0, self.n_cols):
            for i in reversed(range(self.n_per_col*col+1, self.n_per_col*(col+1))):
                pixels[i] = pixels[i - 1]
    
    def get_name(self):
        return 'Rainbow'

class ColorEffect:
    def __init__(self, color, name: str) -> None:
        self.color = color
        self.name = name

    def step(self, pixels: NeoPixel, brightness: float):
        # Show a solid color
        pixels.fill(brightness_adjust(self.color, brightness))

    def get_name(self):
        return self.name
    
class RainEffect:
    def __init__(self, n_cols: int, n_per_col: int) -> None:
        self.t = 0
        
        self.n_cols = n_cols
        self.n_per_col = n_per_col

    def step(self, pixels: NeoPixel, brightness: float):
        for col in range(0, self.n_cols):
            if random.random() < .035:
                color = brightness_adjust(fade(random.randint(150, 265)), brightness)
                for i in range ((col+1)*self.n_per_col-(1+5), (col+1)*self.n_per_col-1):
                    pixels[i] = color
        
        # Shift all leds up in each column
        for col in range(0, self.n_cols):
            for i in range(self.n_per_col*col+1, self.n_per_col*(col+1)):
                pixels[i - 1] = pixels[i]
            pixels[self.n_per_col*(col+1) - 1] = (0, 0, 0)

    def get_name(self):
        return 'Rain'