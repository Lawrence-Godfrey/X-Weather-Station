import time
import bme280
import smbus2 as smbus
from luma.core.interface.serial import i2c
from demo_opts import get_device
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os
import numpy as np
import adafruit_veml6075
import busio 
import board

bus = smbus.SMBus(1)

#setup the OLED display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

#setup BME280
addressbme = 0x76 #BME280 adress
bme280.load_calibration_params(bus,addressbme)


#setup TSL4531
bus.write_byte_data(0x29, 0x00 | 0x80, 0x03)
# TSL45315 address, 0x29(41)
# Select Configuration register, 0x01(1), with Command register, 0x80(128)
#		0x00(00)	Multiplier 1x, Tint : 400ms
bus.write_byte_data(0x29, 0x01 | 0x80, 0x00)

#setup VEML6075
veml = adafruit_veml6075.VEML6075(busio.I2C(board.SCL, board.SDA), integration_time=100)

#create csv file
f = open('weather_data.csv','w')
def main():
    print("Dew Point | Absolute altitude | UV light | visible light")
    
    #create column headings
    f.write("time(s),temperature,atmospheric pressure,humidity,dewpoint,altitude,UV,lux\n")
    tstart = time.time()
    while (1):
        
        #get data from BME280
        bme280_data = bme280.sample(bus,addressbme)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature

        # calculate dew point
        T_wet_bulb = ambient_temperature*(np.arctan(0.151977*((humidity+8.313659)**0.5))) + np.arctan(ambient_temperature+humidity) - np.arctan(humidity-1.676331) + (0.00391838*((humidity)**1.5))*np.arctan(0.023101*humidity) - 4.686035
        sat_water_vapour_press = 6.1121*np.exp((18.678*T_wet_bulb)/(257.14+T_wet_bulb))
        actual_vapour_press = sat_water_vapour_press - (pressure)*0.00066*(1+0.00115*T_wet_bulb)*(ambient_temperature-T_wet_bulb)
        T_dew_point = (257.13*np.log(actual_vapour_press/6.1121))/(18.678-np.log(actual_vapour_press/6.1121))

        # calculate cloud base level
        spread = ambient_temperature - T_dew_point
        height = ((spread/2.5)*1000)*0.3048

        # get lux
        # TSL45315 address, 0x29(41)
        # Read data back from 0x04(4), with Command register, 0x80(128)
        # 2 bytes, LSB first
        data = bus.read_i2c_block_data(0x29, 0x04 | 0x80, 2)

        # Convert the data to lux
        luminance = data[1] * 256 + data[0]

        line1 = "{0:.1f}".format(T_dew_point)
        line2 = "{0:.1f}".format(height)
        line3 = "{0:.3f}".format(veml.uv_index)
        line4 = "{0:.1f}".format(luminance)

        # print data to display
        with canvas(device) as draw:
            draw.text((5, 5), "Dew Point: " + line1 + " C", fill="purple")
            draw.text((5, 15), "Cloud Height: " + line2 + " m", fill="purple")
            draw.text((5, 35), "UV: " + line3, fill="purple")
            draw.text((5, 45), "Lum: " + line4 + " lux", fill="purple")
            
        # print data to console
        print(line1 + " Degrees Celcius | " + line2 + " meters | " + line3 + " | " + line4 + " LUX")  
                
        # include this if you only want to save data for a certain amount of time
        #hours = 
        #if(time.time()-tstart > 3600*hours):
        #    f.close()

        # save data to csv file
        f.write("{0:.0f}".format(time.time()-tstart) + "," + str(ambient_temperature) + "," +str(humidity)+ "," + str(pressure) + "," +line1+","+line2+","+line3+","+line4+"\n") 
        
        time.sleep(0.5)
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        f.close() 
        pass