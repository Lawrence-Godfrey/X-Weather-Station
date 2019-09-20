import time
import sys

import bme280
import smbus2 as smbus
from luma.core.interface.serial import i2c
from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT
from luma.core.render import canvas
from luma.core.virtual import terminal
import os
from PIL import ImageFont

def make_font(name, size):
    font_path = '/usr/share/fonts/truetype/open-sans/'+name
    return ImageFont.truetype(font_path, size)

device = get_device()
term = terminal(device, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 12))

serial = i2c(port=1, address=0x3C)
addressbme = 0x76 #BME280 adress
bus = smbus.SMBus(1)

bme280.load_calibration_params(bus,addressbme)

def main(num_iterations=sys.maxsize):


    while num_iterations > 0:
        num_iterations -= 1
        
        bme280_data = bme280.sample(bus,addressbme)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        print(humidity, pressure, ambient_temperature)
        time.sleep(1)


        # for n in range(10):
        #     with canvas(device) as draw:
        #         term.println("INCORRECT!")
        #         term.puts("You swiped ")
                
        #     time.sleep(0.5)
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass