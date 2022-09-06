import time

from w1thermsensor import W1ThermSensor #water temperature sensor library
import Adafruit_ADS1x15  # Water level sensor library
import bme280  # atmospheric conditions sensor library
import smbus2  # general I2C library
from pyiArduinoI2Cdsl import * #Light sensor library
from pyiArduinoI2Cph import *  # pH sensor library
from pyiArduinoI2Ctds import *  # TDS sensor library


class DataCollection:
    '''
    
    '''
    def __init__(self) -> None:
        self.GAIN = 1
        self.atm_port = 1
        self.atm_address = 0x76
        self.sensor_info = {}
        self.sensor_keys = ['min_wl', 'max_wl', 'air_temp', 'hum', 'pres', 'water_temp', 'light1', 'light2', 'light3', 'light4', 'ph', 'ec', 'tds']
        self.adc_cutoff = 14000
    
    
    def get_sensor_data (self):
        adc = Adafruit_ADS1x15.ADS1115(0x48)                                            
        tds_sensor = pyiArduinoI2Ctds(0x29)
        ph_sensor = pyiArduinoI2Cph(0x19)
        dsl0 = pyiArduinoI2Cdsl(0x30)
        dsl1 = pyiArduinoI2Cdsl(0x31)
        dsl2 = pyiArduinoI2Cdsl(0x32)
        dsl3 = pyiArduinoI2Cdsl(0x33)
        water_sensor = W1ThermSensor()                                           
        time.sleep(2)

        self.sensor_info['light1'] = dsl0.getLux()
        self.sensor_info['light2'] = dsl1.getLux()
        self.sensor_info['light3'] = dsl2.getLux()
        self.sensor_info['light4'] = dsl3.getLux()
        
        self.sensor_info[self.sensor_keys[0]] = int(adc.read_adc(0, gain=self.GAIN) > self.adc_cutoff)
        self.sensor_info[self.sensor_keys[0]] = int(adc.read_adc(1, gain=self.GAIN) > self.adc_cutoff)

        self.sensor_info['water_temp'] = water_sensor.get_temperature()                    
        
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


    
