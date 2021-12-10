
from typing import Optional, Any, List, Union

from pydantic import BaseModel


class SentinelDataInfo(BaseModel):
    aoi: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    platformname: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "provided_data": "POINT (74 32)",
                "start_date": "20210801",
                "end_date": "20210830",
                "platformname": "Sentinel-2"
            }
        }