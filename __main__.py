import board
from neopixel import NeoPixel
from paho.mqtt import client as mqtt_client
import paho.mqtt as mqtt
import random
import sys
import util
import signal
from effects import TrailEffect, FireEffect, RainbowEffect, ColorEffect, RainEffect
import os

# Constants for program

SHUTTER_NUM_COLUMNS = 10
SHUTTERR_LED_PER_COL = 47
SHUTTER_NUM_LEDS = SHUTTER_NUM_COLUMNS * SHUTTERR_LED_PER_COL

broker = 'localhost'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWD']

# must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# -- Program starts here --

# Configure LED strip
shutter_leds = NeoPixel(pixel_pin, SHUTTER_NUM_LEDS, auto_write=False)

# Effects that can be played
effects = [
    TrailEffect(),
    FireEffect(SHUTTER_NUM_COLUMNS, SHUTTERR_LED_PER_COL),
    RainbowEffect(SHUTTER_NUM_COLUMNS, SHUTTERR_LED_PER_COL),
    RainEffect(SHUTTER_NUM_COLUMNS, SHUTTERR_LED_PER_COL),
    ColorEffect((255, 0, 0), 'Red'),
    ColorEffect((0, 255, 0), 'Green'),
    ColorEffect((0, 0, 255), 'Blue'),
    ColorEffect((255, 255, 255), 'White'),
    ColorEffect((196, 0, 245), 'Purple'),
    ColorEffect((0, 179, 255), 'Teal'),
    ColorEffect((0, 15, 145), 'NavyBlue')
]

# Used by MQTT code to figure out the Effect by name
effect_names = list(map(lambda x: x.get_name(), effects))

# Settings of the led wall
current_effect = 0
brightness = 1
power = False

# For google home color thing
tmp_color_val = (0,0,0)
showing_tmp_color = False

def increment_effect():
    global current_effect

    current_effect += 1

    if current_effect >= len(effects):
        current_effect = 0

def set_brightness(value):
    global brightness
    brightness = max(.1, min(1, value))


def on_message(client, userdata, msg):
    global power, brightness, current_effect, tmp_color_val, showing_tmp_color

    data = msg.payload.decode()

    if msg.topic == 'shutterled/power':
        if data == 'ON':
            power = True
        else:
            power = False
    elif msg.topic == 'shutterled/brightness':
        if data == 'UP':
            set_brightness(brightness + .1)
        elif data == 'DOWN':
            set_brightness(brightness - .1)
        else:
            set_brightness(float(data))
    elif msg.topic == 'shutterled/effect':
        showing_tmp_color = False

        if data == 'NEXT':
            increment_effect()
        elif str(data).startswith("TMPCLR:") == True:
            s = str(data).replace("TMPCLR:", "").split(',')

            if len(s) != 3:
                return
        else:
            current_effect = effect_names.index(data)
    elif msg.topic == 'shutterled/tmpcolor':
        s = str(data).split(',')

        r = int(s[0])
        g = int(s[1])
        b = int(s[2])

        tmp_color_val = (r, g, b)
        showing_tmp_color = True


def on_connect(client, userdata, flags, rc):
    client.subscribe('shutterled/power')
    client.subscribe('shutterled/brightness')
    client.subscribe('shutterled/effect')
    client.subscribe('shutterled/tmpcolor')
    client.on_message = on_message

client = mqtt_client.Client(client_id)
client.username_pw_set(username, password)
client.on_connect = on_connect

client.connect(broker, port)
client.loop_start()

def signal_handler(sig, frame):
    client.loop_stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    while True:
        if power == True:
            if showing_tmp_color == True:
                shutter_leds.fill(util.brightness_adjust(tmp_color_val, brightness))
                shutter_leds.show()
            else:
                effects[current_effect].step(shutter_leds, brightness)
                shutter_leds.show()
        else:
            shutter_leds.fill((0,0,0))
            shutter_leds.show()

if __name__ == '__main__':
    main()