# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model


class ModelTarget(Model):
    
    def __init__(self, type: str=None,  component: str=None, device: str=None):  # noqa: E501
        """ModelTarget - 

        :param type: 
        :type type: str
        :param component: 
        :type component: str
        :param device: 
        :type device: str
        """
        self.swagger_types = {
            'type': str,
            'component': str,
            'device': str
        }

        self.attribute_map = {
            'type': 'type',
            'component': 'component',
            'device': 'device'
        }
        self._type = type
        self._component = component
        self._device = device

    @classmethod
    def from_dict(cls, dikt) -> 'ModelTarget':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Tool of this Tool.  # noqa: E501
        :rtype: Tool
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type(self) -> str:
        
        return self._type

    @type.setter
    def type(self, type: str):
    
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def component(self) -> str:
    
        return self._component

    @component.setter
    def component(self, component: str):
        if component is None:
            raise ValueError("Invalid value for `component`, must not be `None`")  # noqa: E501

        self._component = component

    @property
    def device(self) -> str:
    
        return self._device

    @device.setter
    def device(self, device: str):
        if device is None:
            raise ValueError("Invalid value for `device`, must not be `None`")  # noqa: E501

        self._device = device