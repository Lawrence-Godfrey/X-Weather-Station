#include <xCore.h>
#include <xSW01.h>
#include <xOD01.h>


void setRGBColor(int redValue, int greenValue, int blueValue);


#define RED   CC03_RED
#define GREEN CC03_GREEN
#define BLUE  CC03_BLUE

xOD01 OD01;
xSW01 SW01;

const int DelayTime = 1500;

//Create a variable to store the data read from SW01
float dew_point;
float temp;

void setup(){

  //Initialise variables to zero
  dew_point = 0;
  temp = 0;
  //Start I2C communication
  Wire.begin();

  OD01.begin();
  //Start SW01 Sensor
  SW01.begin();

  //Delay for sensor to normalise
  delay(DelayTime);
  
}

void loop(){
  
  //Read and calculate data from SW01
  SW01.poll();

  //Request to get humidity, temperature and dew point data then store in the variables
  dew_point = SW01.getDewPoint();
  temp = SW01.getTempC();

  //calculate cloud base height
  float spread = temp - dew_point;
  float height = ((spread/2.5)*1000)*0.3048;

  OD01.print("Dew Point: ");
  OD01.print(dew_point);
  OD01.println(" C");
  
  OD01.print("Cloud Height ");
  OD01.print(height);
  OD01.println(" m");

  delay(DelayTime-1000);
  OD01.clear();
}
