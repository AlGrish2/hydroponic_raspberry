import os
from typing import List, Tuple
from datetime import datetime

import cv2
import numpy as np
import requests

from handlers.models import SensorsSchema, RequestSchema, AgregatedRecognitionsSchema


class SensorModule:
    def __init__(
        self, 
        tower_id: int,
        endpoint: str,
        ):
        
        self.tower_id = tower_id
        self.endpoint = endpoint
        

    def get_sensor_info(self) -> SensorsSchema:

        try:
            from hardware_interface.raspberry_code.arduino_sensors import DataCollection
            collector = DataCollection()
            print('Сonnection to sensors')
            sensor_info = collector.get_sensor_data()
            min_wl: int = sensor_info['min_wl']
            max_wl: int = sensor_info['max_wl']
            air_temp: float = sensor_info['air_temp']
            hum: float = sensor_info['hum']
            pres: float = sensor_info['pres']
            water_temp: float = sensor_info['water_temp']
            light1: float = sensor_info['light1']
            light2: float = sensor_info['light2']
            light3: float = sensor_info['light3']
            light4: float = sensor_info['light4']
            ph: float = sensor_info['ph']
            ec: float = sensor_info['ec']
            tds: float = sensor_info['tds']
        except Exception as x:
            min_wl: int = 0
            max_wl: int = 1
            air_temp: float = 0.5
            hum: float = 0.5
            pres: float = 0.5
            water_temp: float = 0.5
            light1: float = 0.5
            light2: float = 0.5
            light3: float = 0.5
            light4: float = 0.5
            ph: float = 0.5
            ec: float = 0.5
            tds: float = 0.5
            print(x)

        sensors_schema = SensorsSchema(
            min_wl = min_wl,
            max_wl = max_wl,
            air_temp = air_temp,
            hum = hum,
            pres = pres,
            water_temp = water_temp,
            light1 = light1,
            light2 = light2,
            light3 = light3,
            light4 = light4,
            ph = ph,
            ec = ec,
            tds = tds
        )
        return sensors_schema

    def serialize(
        self,
        timestamp: datetime,
        raw_video_url: str,
        processed_video_url: str,
        agregated_info: AgregatedRecognitionsSchema,
        sensor_info: SensorsSchema
        ) -> RequestSchema:
        
        request_schema = RequestSchema(
            tower_id=self.tower_id,
            timestamp=timestamp,
            raw_video_url=raw_video_url,
            processed_video_url=processed_video_url,
            mean_size=agregated_info.mean_size,
            nutrient_surplus=agregated_info.nutrient_surplus,
            magnesium=agregated_info.magnesium,
            phosphate=agregated_info.phosphate,
            healthy=agregated_info.healthy,
            phosphorous=agregated_info.phosphorous,
            nitrates=agregated_info.nitrates,
            potassium=agregated_info.potassium,
            nitrogen=agregated_info.nitrogen,
            calcium=agregated_info.calcium,
            sulfur=agregated_info.sulfur,
            min_wl = sensor_info.min_wl,
            max_wl = sensor_info.max_wl,
            air_temp = sensor_info.air_temp,
            hum = sensor_info.hum,
            pres = sensor_info.pres,
            water_temp = sensor_info.water_temp,
            light1 = sensor_info.light1,
            light2 = sensor_info.light2,
            light3 = sensor_info.light3,
            light4 = sensor_info.light4,
            ph = sensor_info.ph,
            ec = sensor_info.ec,
            tds = sensor_info.tds
        )
        return request_schema

    def agregate_results(self) -> AgregatedRecognitionsSchema:
        """ 
        Business logic, process and agregate recognitions
        """
        # TODO Count values frome frame recognitions
        agregated_recs_schema = AgregatedRecognitionsSchema(
            mean_size=-1,
            nutrient_surplus=-1,
            magnesium=-1,
            phosphate=-1,
            healthy=-1,
            phosphorous=-1,
            nitrates=-1,
            potassium=-1,
            nitrogen=-1,
            calcium=-1,
            sulfur=-1
        )
        return agregated_recs_schema

    def upload_result(self, request_schema: RequestSchema):
        r = requests.post(self.endpoint, json=request_schema.dict())
        print(request_schema.dict())
        print(r)

    def handle(self):
        sensor_info = self.get_sensor_info()
        timestamp = datetime.now().timestamp()
        raw_video_url, processed_video_url = 'http://none', 'http://none'

        agregated_results = self.agregate_results()

        request_schema = self.serialize(
            timestamp, 
            raw_video_url, 
            processed_video_url,
            agregated_results,
            sensor_info
        )

        self.upload_result(request_schema)
