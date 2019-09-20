# Simple software which uses various X-chips from [XinaBox]: https://www.xinabox.cc to read in the current temperature, humidity and atmospheric pressure and display it on an OLED display.

### Items used
 - [CC03]: https://www.xinabox.cc/collections/core/products/cc03 microcontroller
 - [OD01]: https://www.xinabox.cc/collections/output/products/oD01 OLED Display 
 - [IP02]: https://www.xinabox.cc/collections/interfaces-1/products/ip01 
 - [SW01]: https://www.xinabox.cc/collections/sensor/products/sw01
 - [BR01]: https://www.xinabox.cc/collections/bridges/products/br01
 - Raspberry Pi 3B+ 

 When using the Raspberry Pi, the sensors and display are connected using the BR01 Bridge, which can be easily connected to the GPIO pins on the Pi. 
 If you don't want to use the Pi, the CC03 microcontroller can be used instead, which requires a USB connection for power. 


requires:
 - luma libraries 
    - sudo apt install python-dev python-pip libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 libtiff5
    - sudo -H pip install --upgrade luma.oled
 - bme280 python library
    - sudo apt-get install build-essential python-pip python-dev python-smbus git
    - git clone https://github.com/adafruit/Adafruit_Python_GPIO.git

