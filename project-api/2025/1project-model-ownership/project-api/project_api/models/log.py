# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model


class Log(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, uuid: str=None, name: str=None, description: str=None, annotated: bool=None, start_time: str=None, end_time: str=None, device_description: object=None):  # noqa: E501
        """Log - a model defined in Swagger

        :param uuid: The uuid of this Log.  # noqa: E501
        :type uuid: str
        :param name: The name of this Log.  # noqa: E501
        :type name: str
        :param description: The description of this Log.  # noqa: E501
        :type description: str
        :param annotated: The annotated of this Log.  # noqa: E501
        :type annotated: bool
        :param start_time: The start_time of this Log.  # noqa: E501
        :type start_time: str
        :param end_time: The end_time of this Log.  # noqa: E501
        :type end_time: str
        :param device_description: The device_description of this Log.  # noqa: E501
        :type device_description: object
        """
        self.swagger_types = {
            'uuid': str,
            'name': str,
            'description': str,
            'annotated': bool,
            'start_time': str,
            'end_time': str,
            'device_description': object
        }

        self.attribute_map = {
            'uuid': 'uuid',
            'name': 'name',
            'description': 'description',
            'annotated': 'annotated',
            'start_time': 'start_time',
            'end_time': 'end_time',
            'device_description': 'device_description'
        }
        self._uuid = uuid
        self._name = name
        self._description = description
        self._annotated = annotated
        self._start_time = start_time
        self._end_time = end_time
        self._device_description = device_description

    @classmethod
    def from_dict(cls, dikt) -> 'Log':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Log of this Log.  # noqa: E501
        :rtype: Log
        """
        return util.deserialize_model(dikt, cls)

    @property
    def uuid(self) -> str:
        """Gets the uuid of this Log.


        :return: The uuid of this Log.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid: str):
        """Sets the uuid of this Log.


        :param uuid: The uuid of this Log.
        :type uuid: str
        """
        if uuid is None:
            raise ValueError("Invalid value for `uuid`, must not be `None`")  # noqa: E501

        self._uuid = uuid

    @property
    def name(self) -> str:
        """Gets the name of this Log.


        :return: The name of this Log.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Log.


        :param name: The name of this Log.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this Log.


        :return: The description of this Log.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Log.


        :param description: The description of this Log.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def annotated(self) -> bool:
        """Gets the annotated of this Log.


        :return: The annotated of this Log.
        :rtype: bool
        """
        return self._annotated

    @annotated.setter
    def annotated(self, annotated: bool):
        """Sets the annotated of this Log.


        :param annotated: The annotated of this Log.
        :type annotated: bool
        """
        if annotated is None:
            raise ValueError("Invalid value for `annotated`, must not be `None`")  # noqa: E501

        self._annotated = annotated

    @property
    def start_time(self) -> str:
        """Gets the start_time of this Log.


        :return: The start_time of this Log.
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: str):
        """Sets the start_time of this Log.


        :param start_time: The start_time of this Log.
        :type start_time: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def end_time(self) -> str:
        """Gets the end_time of this Log.


        :return: The end_time of this Log.
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: str):
        """Sets the end_time of this Log.


        :param end_time: The end_time of this Log.
        :type end_time: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def device_description(self) -> object:
        """Gets the device_description of this Log.


        :return: The device_description of this Log.
        :rtype: object
        """
        return self._device_description

    @device_description.setter
    def device_description(self, device_description: object):
        """Sets the device_description of this Log.


        :param device_description: The device_description of this Log.
        :type device_description: object
        """
        if device_description is None:
            raise ValueError("Invalid value for `device_description`, must not be `None`")  # noqa: E501

        self._device_description = device_description
