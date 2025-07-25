# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model


class NewExperiment(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, description: str=None, model_dev_file: str=None):  # noqa: E501
        """NewExperiment - a model defined in Swagger

        :param name: The name of this NewExperiment.  # noqa: E501
        :type name: str
        :param description: The description of this NewExperiment.  # noqa: E501
        :type description: str
        :param model_dev_file: The model_dev_file of this NewExperiment.  # noqa: E501
        :type model_dev_file: str
        """
        self.swagger_types = {
            'name': str,
            'description': str,
            'model_dev_file': str
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'model_dev_file': 'model_dev_file'
        }
        self._name = name
        self._description = description
        self._model_dev_file = model_dev_file

    @classmethod
    def from_dict(cls, dikt) -> 'NewExperiment':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewExperiment of this NewExperiment.  # noqa: E501
        :rtype: NewExperiment
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this NewExperiment.


        :return: The name of this NewExperiment.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this NewExperiment.


        :param name: The name of this NewExperiment.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self) -> str:
        """Gets the description of this NewExperiment.


        :return: The description of this NewExperiment.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this NewExperiment.


        :param description: The description of this NewExperiment.
        :type description: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def model_dev_file(self) -> str:
        """Gets the model_dev_file of this NewExperiment.


        :return: The model_dev_file of this NewExperiment.
        :rtype: str
        """
        return self._model_dev_file

    @model_dev_file.setter
    def model_dev_file(self, model_dev_file: str):
        """Sets the model_dev_file of this NewExperiment.


        :param model_dev_file: The model_dev_file of this NewExperiment.
        :type model_dev_file: str
        """

        self._model_dev_file = model_dev_file
