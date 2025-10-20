from datetime import date
from enum import Enum

from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ


class PartNumber(Enum):
    STEVAL_STWINKT1     = "STEVAL-STWINKT1"
    OpenMV_H7_Plus      = "OpenMV-H7-Plus"
    STEVAL_MKSBOX1V1    = "STEVAL-MKSBOX1V1"

class DeviceDescription():

    @property
    def part_number(self) -> PartNumber:
        return self.__part_number

    @part_number.setter 
    def part_number(self, value: PartNumber):
        self.__part_number = value

    @property
    def serial_number(self) -> str:
        return self.__serial_number

    @serial_number.setter 
    def serial_number(self, value: str):
        self.__serial_number = value

    @property
    def alias(self) -> str:
        return self.__alias

    @alias.setter 
    def alias(self, value: str):
        self.__alias = value

    @property
    def fw_name(self) -> str:
        return self.__fw_name

    @fw_name.setter 
    def fw_name(self, value: str):
        self.__fw_name = value

    @property
    def fw_version(self) -> str:
        return self.__fw_version

    @fw_version.setter 
    def fw_version(self, value: str):
        self.__fw_version = value

    @property
    def firmware_id(self) -> str:
        return self.__firmware_id

    @firmware_id.setter 
    def firmware_id(self, value: str):
        self.__firmware_id = value

    @property
    def board_id(self) -> str:
        return self.__board_id

    @board_id.setter 
    def board_id(self, value: str):
        self.__board_id = value

    def __init__(self, part_number: str = None, serial_number: str = None, alias: str = None, fw_name: str = None, fw_version: str = None, firmware_id: int = None, board_id: int = None):
        self.__part_number      = part_number
        self.__serial_number    = serial_number
        self.__alias            = alias
        self.__fw_name          = fw_name
        self.__fw_version       = fw_version
        self.__firmware_id      = firmware_id
        self.__board_id         = board_id

class Log(DomainOBJ):
    """Log data model"""

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter 
    def uuid(self, value: str):
        self.__uuid = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter 
    def name(self, value: str):
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter 
    def description(self, value: str):
        self.__description = value

    @property
    def annotated(self) -> bool:
        return self.__annotated

    @annotated.setter 
    def annotated(self, value: bool):
        self.__annotated = value

    @property
    def start_time(self) -> date:
        return self.__start_time

    @start_time.setter 
    def start_time(self, value: date):
        self.__start_time = value

    @property
    def end_time(self) -> date:
        return self.__end_time

    @end_time.setter 
    def end_time(self, value: date):
        self.__end_time = value

    @property
    def device_description(self) -> DeviceDescription:
        return self.__device_description

    @device_description.setter 
    def device_description(self, value: DeviceDescription):
        self.__device_description = value

    def __init__(self, uuid: str = None, name: str = None, description: str = None, annotated: bool = None, start_time: date = None, end_time: date = None, device_description: DeviceDescription = None):
        self.__uuid         = uuid
        self.__name         = name
        self.__description  = description
        self.__annotated    = annotated
        self.__start_time   = start_time
        self.__end_time     = end_time
        self.__device_description = device_description