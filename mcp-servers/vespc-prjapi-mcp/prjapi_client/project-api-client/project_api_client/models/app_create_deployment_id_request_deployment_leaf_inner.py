# coding: utf-8

"""
    STAIoTCraft - Project API

    REST API to access STAIoTCraft Back-End web-service User Projects

    The version of the OpenAPI document: 3.0.7
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from project_api_client.models.app_create_deployment_id_request_deployment_leaf_inner_datalogging import AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging
from project_api_client.models.app_create_deployment_id_request_deployment_leaf_inner_inference import AppCreateDeploymentIdRequestDeploymentLeafInnerInference
from typing import Optional, Set
from typing_extensions import Self

class AppCreateDeploymentIdRequestDeploymentLeafInner(BaseModel):
    """
    AppCreateDeploymentIdRequestDeploymentLeafInner
    """ # noqa: E501
    gateway_id: Optional[StrictStr] = None
    device_id: Optional[StrictStr] = None
    application: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    display_name: Optional[StrictStr] = None
    datalogging: Optional[AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging] = None
    inference: Optional[AppCreateDeploymentIdRequestDeploymentLeafInnerInference] = None
    __properties: ClassVar[List[str]] = ["gateway_id", "device_id", "application", "description", "display_name", "datalogging", "inference"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AppCreateDeploymentIdRequestDeploymentLeafInner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of datalogging
        if self.datalogging:
            _dict['datalogging'] = self.datalogging.to_dict()
        # override the default output from pydantic by calling `to_dict()` of inference
        if self.inference:
            _dict['inference'] = self.inference.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppCreateDeploymentIdRequestDeploymentLeafInner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "gateway_id": obj.get("gateway_id"),
            "device_id": obj.get("device_id"),
            "application": obj.get("application"),
            "description": obj.get("description"),
            "display_name": obj.get("display_name"),
            "datalogging": AppCreateDeploymentIdRequestDeploymentLeafInnerDatalogging.from_dict(obj["datalogging"]) if obj.get("datalogging") is not None else None,
            "inference": AppCreateDeploymentIdRequestDeploymentLeafInnerInference.from_dict(obj["inference"]) if obj.get("inference") is not None else None
        })
        return _obj


