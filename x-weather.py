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
import numpy as np

def make_font(name, size):
    font_path = '/usr/share/fonts/truetype/open-sans/'+name
    return ImageFont.truetype(font_path, size)

device = get_device()
term = terminal(device, ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 12))

serial = i2c(port=1, address=0x3C)
addressbme = 0x76 #BME280 adress
bus = smbus.SMBus(1)

bme280.load_calibration_params(bus,addressbme)

def main():
    print("Dew Point | Absolute altitude")
    while (1):
   
        bme280_data = bme280.sample(bus,addressbme)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature

        #calculate dew point
        T_wet_bulb = ambient_temperature*(np.arctan(0.151977*((humidity+8.313659)**0.5))) + np.arctan(ambient_temperature+humidity) - np.arctan(humidity-1.676331) + (0.00391838*((humidity)**1.5))*np.arctan(0.023101*humidity) - 4.686035
        sat_water_vapour_press = 6.1121*np.exp((18.678*T_wet_bulb)/(257.14+T_wet_bulb))
        actual_vapour_press = sat_water_vapour_press - (pressure)*0.00066*(1+0.00115*T_wet_bulb)*(ambient_temperature-T_wet_bulb)
        T_dew_point = (257.13*np.log(actual_vapour_press/6.1121))/(18.678-np.log(actual_vapour_press/6.1121))

        #calculate cloud base level
        spread = ambient_temperature - T_dew_point
        height = ((spread/2.5)*1000)*0.3048

        line1 = "{0:.1f} Degrees Celcius".format(T_dew_point)
        line2 = "{0:.1f} meters".format(height)

        with canvas(device) as draw:
            draw.text((5, 5), "Dew Point", fill="purple")
            draw.text((5, 15), line1, fill="purple")
            draw.text((5, 35), "Absolute Altitude", fill="purple")
            draw.text((5, 45), line2, fill="purple")
            

        print(line1 + " | " + line2)  

        #term.puts(line)
                
        time.sleep(0.5)
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass