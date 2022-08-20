from datetime import datetime
from pydantic import BaseModel, AnyUrl


class AgregatedRecognitionsSchema(BaseModel):
    mean_size: float
    healthy_plants: float
    deffect_0: float
    deffect_1: float
    deffect_2: float


class SensorsSchema(BaseModel):
    sensor_0_light_level: float
    sensor_1_light_level: float
    air_temp: float
    relative_humidity: float
    pressure: float
    water_temp: float
    water_ph: float
    water_ec: float
    water_ppm: float
    water_level_up: bool
    water_level_down: bool


class RequestSchema(BaseModel):
    tower_id: int
    timestamp: float = datetime.now().timestamp()
    raw_video_url: AnyUrl = None
    processed_video_url: AnyUrl = None
    
    mean_size: float = None
    healthy_plants: float = None
    deffect_0: float = None
    deffect_1: float = None
    deffect_2: float = None

    sensor_0_light_level: float = None
    sensor_1_light_level: float = None
    air_temp: float = None
    relative_humidity: float = None
    pressure: float = None
    water_temp: float = None
    water_ph: float = None
    water_ec: float = None
    water_ppm: float = None
    water_level_up: bool = None
    water_level_down: bool = None