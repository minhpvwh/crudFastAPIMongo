from typing import Optional, List, Any
from enum import Enum, IntEnum
from pydantic import BaseModel, EmailStr, Field


class StatusDeviceEnum(str, Enum):
    on = 'on'
    off = 'off'


class DeviceSchema(BaseModel):
    name: str = Field(...)
    location: str = Field(...)
    temp_from: float = Field(...)
    temp_to: float = Field(...)
    client_id: str = Field(...)
    secret_key: str = Field(...)
    status: StatusDeviceEnum = StatusDeviceEnum.on
    version: str = Field(...)

    class Config:
        title = 'Device'


class UpdateDeviceModel(BaseModel):
    name: Optional[str]
    location: Optional[str]
    temp_from: Optional[float]
    temp_to: Optional[float]
    client_id: Optional[str]
    secret_key: Optional[str]
    status: Optional[StatusDeviceEnum]
    version: Optional[str]
