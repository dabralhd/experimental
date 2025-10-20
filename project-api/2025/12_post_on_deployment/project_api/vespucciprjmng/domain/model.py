from __future__ import annotations

from enum import Enum
from typing import List

from project_api.vespucciprjmng.domain.dataset import Dataset
from project_api.vespucciprjmng.domain.domain_obj import DomainOBJ
from project_api.vespucciprjmng.domain.training import Training


class ModelType(Enum):
    CLASSIFIER          = "classifier"
    ANOMALY_DETECTOR    = "anomaly_detector"
    PREDICTOR           = "predictor"

class TrainingType(Enum):
    ONLINE     = "online"
    OFFLINE    = "offline"

class Stage(Enum):
    DEFINITION              = "definition"
    LOG_COLLECTION          = "log_collection"
    MODELING                = "modeling"
    VALIDATION_ON_TARGET    = "validation_on_target"
    DEPLOYMENT              = "deployment"

class ModelMetadata():
    
    @property
    def type(self) -> ModelType:
        return self.__model_type
    
    @property
    def classes(self) -> List[str]:
        return self.__classes

    @type.setter 
    def type(self, value: ModelType):
        self.__model_type = value

    @classes.setter
    def classes(self, value: List[str]):
        self.__classes = value

    def __init__(self, classes: List[str], model_type: ModelType = None):
        self.__classes = classes
        self.__model_type = model_type
        pass

class ModelTarget():
    
    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value
    
    @property
    def component(self) -> str:
        return self.__component

    @component.setter
    def component(self, value: str):
        self.__component = value

    @property
    def device(self) -> str:
        return self.__device

    @device.setter
    def device(self, value: str):
        self.__device = value

    def __init__(self, type: str = None, component: str = None, device: str = None):
        self.__type = type
        self.__component = component
        self.__device = device
        pass

class Model(DomainOBJ):
    """Model data model"""

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
    def model_ref(self) -> Model:
        return self.__model_ref

    @model_ref.setter 
    def model_ref(self, value: Model):
        self.__model_ref = value

    @property
    def dataset(self) -> Dataset:
        return self.__dataset

    @dataset.setter 
    def dataset(self, value: Dataset):
        self.__dataset = value

    @property
    def model_metadata(self) -> ModelMetadata:
        return self.__model_metadata

    @model_metadata.setter 
    def model_metadata(self, value: ModelMetadata):
        self.__model_metadata = value

    @property
    def target(self) -> ModelTarget:
        return self.__model_target

    @target.setter
    def target(self, value: ModelTarget):
        self.__model_target = value
    
    @property
    def training(self) -> Training:
        return self.__model_training

    @training.setter
    def training(self, value: Training):
        self.__model_training = value
    
    @property
    def data_sufficiency(self) -> Training:
        return self.__data_sufficiency

    @data_sufficiency.setter
    def data_sufficiency(self, value: Training):
        self.__data_sufficiency = value

    @property
    def model_owner_uuid(self) -> str:
        return self.__model_owner_uuid 

    @model_owner_uuid.setter
    def model_owner_uuid(self, value: str):
        self.__model_owner_uuid = value           

    @property
    def creation_time(self) -> str:
        """Gets the creation_time of this Project.


        :return: The creation_time of this Project.
        :rtype: str
        """
        return self.__creation_time

    @creation_time.setter
    def creation_time(self, creation_time: str=None):
        """Sets the creation_time of this Project.


        :param creation_time: The creation_time of this Project.
        :type creation_time: str
        """
        if creation_time is None:
            raise ValueError("Invalid value for `creation_time`, must not be `None`")  # noqa: E501

        self.__creation_time = creation_time

    @property
    def last_update_time(self) -> str:
        """Gets the last_update_time of this Project.


        :return: The last_update_time of this Project.
        :rtype: str
        """
        return self.__last_update_time

    @last_update_time.setter
    def last_update_time(self, last_update_time: str):
        """Sets the last_update_time of this Project.


        :param last_update_time: The last_update_time of this Project.
        :type last_update_time: str
        """
        self.__last_update_time = last_update_time              

    def __init__(self, uuid: str = None, name: str = None, model_ref: Model = None, dataset: Dataset = None, model_metadata: ModelMetadata = None, model_target: ModelTarget = None, model_training: Training=None, data_sufficiency: Training=None, creation_time: str=None, last_update_time: str=None, model_owner_uuid: str=None):
        self.__uuid             = uuid
        self.__name             = name
        self.__model_ref        = model_ref
        self.__dataset          = dataset
        self.__model_metadata   = model_metadata
        self.__model_target     = model_target
        self.__model_training   = model_training
        self.__data_sufficiency = data_sufficiency
        self.__creation_time = creation_time
        self.__last_update_time = last_update_time    
        self.__model_owner_uuid = model_owner_uuid