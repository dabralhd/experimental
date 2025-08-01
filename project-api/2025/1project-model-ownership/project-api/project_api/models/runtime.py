# coding: utf-8

from __future__ import absolute_import

from typing import List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model
from project_api.models.job import Job


class Runtime(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, type: str=None,  jobs: List=None):  # noqa: E501
        """Pipeline - a model defined in Swagger

        :param type: The name of this Pipeline.  # noqa: E501
        :type type: str
        :param jobs: The array of Job instances.  # noqa: E501
        :type jobs: array
        """
        self.swagger_types = {
            'type': str,
            'jobs': List[Job],
        }

        self.attribute_map = {
            'type': 'type',
            'jobs': 'jobs'
        }
        self._type = type
        self._jobs = jobs

    @classmethod
    def from_dict(cls, dikt) -> 'Runtime':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Tool of this Tool.  # noqa: E501
        :rtype: Tool
        """
        return util.deserialize_model(dikt, cls)

    @property
    def type(self) -> str:
        """Gets the type of this Runtime.


        :return: The type of this Runtime.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Runtime.


        :param name: The type of this Runtime.
        :type name: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def jobs(self) -> List:
        """Gets the description of this Runtime.


        :return: The description of this Runtime.
        :rtype: str
        """
        return self._jobs

    @jobs.setter
    def jobs(self, jobs: List):
        """Sets the description of this Runtime.


        :param description: The description of this Runtime.
        :type description: str
        """
        if jobs is None:
            raise ValueError("Invalid value for `jobs`, must not be `None`")  # noqa: E501

        self._jobs = jobs
    
