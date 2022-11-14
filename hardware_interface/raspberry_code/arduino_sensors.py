import time
import serial
import Adafruit_ADS1x15  # Water level sensor library
import bme280  # atmospheric conditions sensor library
import smbus2  # general I2C library
from pyiArduinoI2Cdsl import * #Light sensor library
from pyiArduinoI2Cph import *  # pH sensor library
from pyiArduinoI2Ctds import *  # TDS sensor library

class DataCollection:
    def __init__(self) -> None:
        self.atm_port = 1
        self.atm_address = 0x76
        self.sensor_info = {}
        self.sensor_keys = ['wl_upper', 'wl_lower', 'air_temp', 'hum', 'pres', 'water_temp', 'light1', 'ph', 'ec', 'tds']

    def get_sensor_data (self):
        tds_sensor = pyiArduinoI2Ctds(0x29)
        ph_sensor = pyiArduinoI2Cph(0x19)
        dsl0 = pyiArduinoI2Cdsl(0x30)
        watertemp = str(1)
        waterlevel = str(2)

        time.sleep(2)

        self.sensor_info['light1'] = dsl0.getLux()
        self.sensor_info['light2'] = -1
        self.sensor_info['light3'] = -1
        self.sensor_info['light4'] = -1
        self.sensor_info[self.sensor_keys[0]] = -1
        
        ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        ser.reset_input_buffer()
        watertempencode = watertemp.encode()
        while 1:
            ser.write(watertempencode)
            time.sleep(1)
            if ser.in_waiting > 0:
                self.sensor_info['water_temp'] = float(ser.readline().decode('utf-8').rstrip())
                break           
        time.sleep(0.5)
        waterlevelencode = waterlevel.encode()
        while 1:
            ser.write(waterlevelencode)
            time.sleep(1)
            if ser.in_waiting > 0:
                self.sensor_info[self.sensor_keys[1]] = ser.readline().decode('utf-8').rstrip()
                break
        
        while True:
            try:
                atm_bus = smbus2.SMBus(self.atm_port)
                time.sleep(1)
                atmospheric_data = bme280.sample(atm_bus, self.atm_address)
                self.sensor_info['air_temp'] = atmospheric_data.temperature
                self.sensor_info['hum'] = atmospheric_data.humidity
                self.sensor_info['pres'] = atmospheric_data.pressure*100
                break
            except:
                continue
        

        self.sensor_info['ph'] = ph_sensor.getPH()
        tds_sensor.set_t(self.sensor_info['water_temp'])
        self.sensor_info['ec'] = tds_sensor.getEC() 
        self.sensor_info['tds'] = tds_sensor.getTDS() 

        

        return self.sensor_info