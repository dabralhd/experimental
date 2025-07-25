# coding: utf-8

from __future__ import absolute_import

from datetime import date, datetime  # noqa: F401
from typing import Dict, List  # noqa: F401

from project_api import util
from project_api.models.base_model_ import Model


class ModelType(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    CLASSIFIER = "classifier"
    ANOMALY_DETECTOR = "anomaly_detector"
    def __init__(self):  # noqa: E501
        """ModelType - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'ModelType':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelType of this ModelType.  # noqa: E501
        :rtype: ModelType
        """
        return util.deserialize_model(dikt, cls)


    @staticmethod
    def from_str(label):
        if label == ModelType.CLASSIFIER:
            return ModelType.CLASSIFIER
        elif label == ModelType.ANOMALY_DETECTOR:
            return ModelType.ANOMALY_DETECTOR
        else:
            raise NotImplementedError