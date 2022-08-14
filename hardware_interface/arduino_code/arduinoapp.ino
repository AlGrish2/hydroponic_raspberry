#include <BH1750.h>                 //light sensor library
#include <BME280I2C.h>              //atmospheric sensor library
#include <Rtc_Pcf8563.h>            //RTC library
#include <iarduino_I2C_pH.h>        //pH sensor library
#include <iarduino_I2C_TDS.h>       //TDS sensor library
#include <Wire.h>                   //I2C library
BH1750 bh1750_a;                    //begin light sensor library for sensor 1
BH1750 bh1750_b;                    //begin light sensor library for sensor 2
BH1750 lightMeter;                  //begin light sensor library
BME280I2C bme;                      //begin atmospheric sensor library
Rtc_Pcf8563 rtc;                    //begin RTC library
iarduino_I2C_pH sensor(0x19);       //begin pH sensor library + declare pH sensor address
iarduino_I2C_TDS tds(0x29);         //begin TDS sensor library + declare EC sensor address

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
  pinMode(3, INPUT);                                                  //Declare pin mode for pin 
  pinMode(4, INPUT);                                                  //Declare pin mode for pin 
  pinMode(3, INPUT);                                                  //Declare pin mode for pin 
  pinMode(4, INPUT);                                                  //Declare pin mode for pin 
  pinMode(3, INPUT);                                                  //Declare pin mode for pin 
  pinMode(4, INPUT);                                                  //Declare pin mode for pin 
  pinMode(3, INPUT);                                                  //Declare pin mode for pin 
  pinMode(4, INPUT);                                                  //Declare pin mode for pin 
  pinMode(3, INPUT);                                                  //Declare pin mode for pin 
  pinMode(4, INPUT);                                                  //Declare pin mode for pin 
}
float light_level_a;                  //variable for light sensor 1
float light_level_b;                  //variable for light sensor 2
int hour = 0;                         //variable for hours in RTC
int minute = 0;                       //variable for minutes in RTC
int sec = 0;                          //variable for seconds in RTC
float temp(NAN), hum(NAN), pres(NAN); //variables for air conditions sensor
float pH = 0;                         //variable for pH
float EC = 0;                         //variable for Electrical conductivity
float TDS = 0;                        //variable for total dissolved solids
bool wlupper = false;                 //variable for upper water level sensor
bool wllower = false;                 //variable for lower water level sensor
float temperature = 22.5;             //variable for temperature
bool mpump = 0;                       //main pump state variable
const int pump_pin = 4;               //pump pin, in this case, corresponds to EK 2
float aprt = 0;                       //pump a run time variable
float bprt = 0;                       //pump b run time variable
float avolume = 0;                    //volume of solution A needed to be added
float bvolume = 0;                    //volume of solution B needed to be added
const int pumprate = 100;             //milliliters per hour for persithaltic pump at 12 v
const int apump_pin = 2;              //digital pin number of solution A pump
const int bpump_pin = 2;              //digital pin nubmer of solution B pump

void loop()                                           //Main code
{
  light_sensors_data();
  print_light_sensor();
  BME280data();
  print_air_sensor(&Serial);
//  input_time_serial();
  print_time();
  pH_data();
  print_pH();
  ec_data();
  print_ec();
  water_level_sense();
  print_wl();
  Serial.print("\n\r");
  delay(1000);
}

void light_sensors_data ()                          //update light sensor variables to most recent reading
{
  if (bh1750_a.measurementReady()) {
    light_level_a = bh1750_a.readLightLevel();
  }
  if (bh1750_b.measurementReady()) {
    light_level_b = bh1750_b.readLightLevel();
  }
}

void print_light_sensor()                           //serial print light sensor readings
{
  
  Serial.print("Light1 :");
  Serial.print(light_level_a);
  Serial.print("\t\tLight2 :");
  Serial.print(light_level_b);
  Serial.print("\n\r");
}

void BME280data()                                   //update atmospheric sensor variables to most recent reading
{
  float temp(NAN), hum(NAN), pres(NAN);
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);
  bme.read(pres, temp, hum, tempUnit, presUnit);
}

void print_air_sensor(Stream* client)                //serial print light sensor readings
{
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);

  bme.read(pres, temp, hum, tempUnit, presUnit);
  
  client->print("Temp: ");
  client->print(temp);
  client->print("°C");
  client->print("\t\tHumidity: ");
  client->print(hum);
  client->print("% RH");
  client->print("\t\tPressure: ");
  client->print(pres);
  client->print("Pa");
  client->print("\n\r");
}

void rtc_get_time()                                 //update second, minute and hour variables to most recent RTC readings
{
  rtc.getTime();
}
void print_time()                                   //serial print time
{
  Serial.print("Time: ");
  Serial.print(rtc.formatTime());
  Serial.print("\n\r");
}
void input_time_serial()                            //work in progress function for reading time from serial input
{
  if(Serial.available() > 0) // function for getting variables for time
  {
    Serial.print("input hour");
    hour = Serial.read();
    Serial.print("input minute");
    minute = Serial.read();
    Serial.print("input sec");
    sec = Serial.read();
  }
  rtc.setTime(hour, minute, sec); // sets time on RTC
}

void pH_data()                                      //update pH sensor variable to most recent reading
{
   pH = sensor.getPH();
}

void print_pH()                                     //serial print pH value
{
  Serial.print("pH: ");
  Serial.print(pH);
  Serial.print("\t\t");
}

void ec_data()                                      //update TDS sensor variables to most recent reading
{
  tds.set_t(temperature);
  EC = tds.get_S();
  TDS = tds.getTDS();
}
void print_ec()                                     //serial print TDS sensor readings
{
  Serial.print("EC: ");
  Serial.print(tds.get_S());
  Serial.print("mS/cm" );
  Serial.print("\t\tTDS: ");
  Serial.print(tds.getTDS());
  Serial.print("mg/L\n\r");
}

void water_level_sense()                            //update water level sensor variables to most recent reading
{
  if (digitalRead(3) == HIGH) {wlupper = true;}
  else {wlupper = false;}
  if (digitalRead(4) == HIGH) {wllower = true;}
  else {wllower = false;}
}

void print_wl()                                     //serial print water level readings
{
  Serial.print("Upper Sensor: ");
  Serial.print(wlupper);
  Serial.print("\t\tLower Sensor: ");
  Serial.print(wllower);
  Serial.print("\n\r");
}

void SPI_COMM()                                     //spi communication protocol
{
  
}

void pump_main_switch()                             //change main pump state(on -> off or off -> on)
{
  if(mpump == 1)
  {
    digitalWrite(pump_pin, LOW);
    Serial.print("pump off\n\r");
    mpump = 0;
  }
  else
  {
    digitalWrite(pump_pin, HIGH);
    Serial.print("pump on\n\r");
    mpump = 1;
  }
}

void apump_run()                                  //run pump for solution A to add a set volume of solution a
{
  aprt = avolume/pumprate;
  while(sec+60*minute+3600*hour < sec+60*minute+3600*hour+aprt)
  {
    digitalWrite(apump_pin, HIGH);
  }
  digitalWrite(apump_pin, LOW);
}

void bpump_run()                                  //run pump for solution B to add a set volume of solution a
{
  bprt = bvolume/pumprate;
  while(sec+60*minute+3600*hour < sec+60*minute+3600*hour+bprt)
  {
    digitalWrite(bpump_pin, HIGH);
  }
  digitalWrite(bpump_pin, LOW);
}
