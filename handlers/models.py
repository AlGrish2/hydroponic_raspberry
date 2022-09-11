from datetime import datetime
from pydantic import BaseModel, AnyUrl


class AgregatedRecognitionsSchema(BaseModel):
    mean_size: float
    nutrient_surplus: float
    magnesium: float
    phosphate: float
    healthy: float
    phosphorous: float
    nitrates: float
    potassium: float
    nitrogen: float
    calcium: float
    sulfur: float


class SensorsSchema(BaseModel):
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


class RequestSchema(BaseModel):
    tower_id: int
    timestamp: float = datetime.now().timestamp()
    raw_video_url: AnyUrl = None
    processed_video_url: AnyUrl = None
    
    mean_size: float = None
    nutrient_surplus: float
    magnesium: float
    phosphate: float
    healthy: float
    phosphorous: float
    nitrates: float
    potassium: float
    nitrogen: float
    calcium: float
    sulfur: float

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