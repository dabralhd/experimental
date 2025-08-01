# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model


class ResourceUsage(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, efs_usage: str=None, cpu_usage: str=None):  # noqa: E501
        """ResourceUsage - a model defined in Swagger

        :param efs_usage: The efs_usage of this ResourceUsage.  # noqa: E501
        :type efs_usage: str
        :param cpu_usage: The cpu_usage of this ResourceUsage.  # noqa: E501
        :type cpu_usage: str
        """
        self.swagger_types = {
            'efs_usage': str,
            'cpu_usage': str
        }

        self.attribute_map = {
            'efs_usage': 'efs_usage',
            'cpu_usage': 'cpu_usage'
        }
        self._efs_usage = efs_usage
        self._cpu_usage = cpu_usage

    @classmethod
    def from_dict(cls, dikt) -> 'ResourceUsage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ResourceUsage of this ResourceUsage.  # noqa: E501
        :rtype: ResourceUsage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def efs_usage(self) -> str:
        """Gets the efs_usage of this ResourceUsage.


        :return: The efs_usage of this ResourceUsage.
        :rtype: str
        """
        return self._efs_usage

    @efs_usage.setter
    def efs_usage(self, efs_usage: str):
        """Sets the efs_usage of this ResourceUsage.


        :param efs_usage: The efs_usage of this ResourceUsage.
        :type efs_usage: str
        """
        if efs_usage is None:
            raise ValueError("Invalid value for `efs_usage`, must not be `None`")  # noqa: E501

        self._efs_usage = efs_usage

    @property
    def cpu_usage(self) -> str:
        """Gets the cpu_usage of this ResourceUsage.


        :return: The cpu_usage of this ResourceUsage.
        :rtype: str
        """
        return self._cpu_usage

    @cpu_usage.setter
    def cpu_usage(self, cpu_usage: str):
        """Sets the cpu_usage of this ResourceUsage.


        :param cpu_usage: The cpu_usage of this ResourceUsage.
        :type cpu_usage: str
        """
        if cpu_usage is None:
            raise ValueError("Invalid value for `cpu_usage`, must not be `None`")  # noqa: E501

        self._cpu_usage = cpu_usage
