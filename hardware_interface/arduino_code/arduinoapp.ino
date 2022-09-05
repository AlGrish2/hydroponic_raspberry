#include <Adafruit_ADS1X15.h>
#include <BH1750.h>                 //light sensor library
#include <BME280I2C.h>              //atmospheric sensor library
#include <Rtc_Pcf8563.h>            //RTC library
#include <iarduino_I2C_pH.h>        //pH sensor library
#include <iarduino_I2C_TDS.h>       //TDS sensor library
#include <Wire.h>                   //I2C library
#include <SD.h>
#include <OneWire.h> 
#include <DallasTemperature.h>


BH1750 bh1750_a;                    //begin light sensor library for sensor 1
BH1750 bh1750_b;                    //begin light sensor library for sensor 2
BH1750 lightMeter;                  //begin light sensor library
BME280I2C bme;                      //begin atmospheric sensor library
Rtc_Pcf8563 rtc;                    //begin RTC library
iarduino_I2C_pH sensor(0x19);       //begin pH sensor library + declare pH sensor address
iarduino_I2C_TDS tds(0x29);         //begin TDS sensor library + declare EC sensor address
Adafruit_ADS1115 ads;
File myFile;
OneWire oneWire(A2);
DallasTemperature sensors(&oneWire);

#define pump_pin 4;                   //pump pin, in this case, corresponds to EK 2
#define pumprate 100;               //milliliters per hour for persithaltic pump at 12 v
#define apump_pin 2;                  //digital pin number of solution A pump
#define bpump_pin 5;                  //digital pin nubmer of solution B pump
float light_level_a;                  //variable for light sensor 1
float light_level_b;                  //variable for light sensor 2
int hour = 0;                         //variable for hours in RTC
int minute = 0;                       //variable for minutes in RTC
int sec = 0;                          //variable for seconds in RTC
float temp(NAN), hum(NAN), pres(NAN); //variables for air conditions sensor
float pH = 0;                         //variable for pH
float EC = 0;                         //variable for Electrical conductivity
float TDS = 0;                        //variable for total dissolved solids
bool wlupper;                      //variable for upper water level sensor
bool wllower;                      //variable for lower water level sensor
float temperature = 22.5;             //variable for temperature
int failcount = 0;
//bool mpump = 0;                       //main pump state variable
//float aprt = 0;                       //pump a run time variable
//float bprt = 0;                       //pump b run time variable
//float avolume = 0;                    //volume of solution A needed to be added
//float bvolume = 0;                    //volume of solution B needed to be added


void setup() 
{
  Serial.begin(9600);                                                 //begin serial monitor
  while(!Serial){}                                                    //wait for serial port to begin operation
  Wire.begin();                                                       //begin I2C bus operation
  sensor.begin();                                                     //activate pH sensor
  tds.begin();                                                        //activate TDS sensor
  bh1750_a.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x23, &Wire);      //set up operation mode for light sensor 1
  bh1750_b.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x5C, &Wire);      //set up operation mode for light sensor 2
  while(!bme.begin()){delay(1000);}                                   //wait for atmospheric sensor to begin operation
  switch(bme.chipModel())                                             //detect that the atmospheric sensor is the correct model
  {
     case BME280::ChipModel_BME280:
       Serial.println("Found BME280 sensor! Success.");
       break;
     default:
       Serial.println("Found UNKNOWN sensor! Error!");
  }
  rtc.initClock();                                                    //begin RTC operation
  rtc.setDate(17, 7, 7, 20, 22);                                      //Set date to be done through RPi SPI connection(day, weekday, month, century, year
  ads.begin();
  sensors.begin();
}




void light_sensors_data()                          //update light sensor variables to most recent reading
{
  if (bh1750_a.measurementReady()) {
    light_level_a = bh1750_a.readLightLevel();
  }
  if (bh1750_b.measurementReady()) {
    light_level_b = bh1750_b.readLightLevel();
  }
}

void wtemperature_data()
{
  sensors.requestTemperatures();
  temperature = sensors.getTempCByIndex(0);
}

void BME280data()                                   //update atmospheric sensor variables to most recent reading
{
  float temp(NAN), hum(NAN), pres(NAN);
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);
  bme.read(pres, temp, hum, tempUnit, presUnit);
}


void pH_data()                                      //update pH sensor variable to most recent reading
{
   pH = sensor.getPH();
}

void ec_data()                                      //update TDS sensor variables to most recent reading
{
  tds.set_t(temperature);
  EC = tds.get_S();
  TDS = tds.getTDS();
}

void water_level_sense()                            //update water level sensor variables to most recent reading
{
  if (ads.readADC_SingleEnded(0) < 14000) {wlupper = false;}
  else {wlupper = true;}
  if (ads.readADC_SingleEnded(1) < 1400) {wllower = false;}
  else {wllower = true;}
}

void record_sd()                                     //spi communication protocol
{
  if (!SD.begin(10)) {while (1);}
  myFile = SD.open("records.txt", FILE_WRITE);
  if (myFile) 
  {
    myFile.println(rtc.formatDate());
    myFile.println(", ");
    myFile.println(rtc.formatTime());
    myFile.println(", ");
    myFile.println(temp);
    myFile.println(", ");
    myFile.println(hum);
    myFile.println(", ");
    myFile.println(pres);
    myFile.println(", ");
    myFile.println(temperature);
    myFile.println(", ");
    myFile.println(light_level_a);
    myFile.println(", ");
    myFile.println(light_level_b);
    myFile.println(", ");
    myFile.println(EC);
    myFile.println(", ");
    myFile.println(TDS);
    myFile.println(", ");
    myFile.println(wllower);
    myFile.println(", ");
    myFile.println(wlupper);
    myFile.close();
  }
  else
  {
    failcount++;
  }
}

void loop()                                           //Main code
{
  rtc.getMinute();
  if(minute <= 3)
  {
    light_sensors_data();
    BME280data();
    ec_data();
    water_level_sense();
    wtemperature_data();
    record_sd();
    delay(180000);
  }
  else {delay(180000);}
}