
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.input_db_dao import InputDBDAO
from project_api.vespucciprjmng.dao.db_service.input_tool_db_dao import (
    InputToolDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.output_db_dao import OutputDBDAO
from project_api.vespucciprjmng.dao.db_service.output_tool_db_dao import (
    OutputToolDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.model_dao import ModelDAO
from project_api.vespucciprjmng.domain.input import Input
from project_api.vespucciprjmng.domain.model import (
    Model,
    ModelMetadata,
    ModelType,
    Stage,
    TrainingType,
)
from project_api.vespucciprjmng.domain.output import Output
from project_api.vespucciprjmng.domain.tool import Tool


class ModelDBDAO(ModelDAO):
    """Model data access object for DB service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)


    def get_all(self, project_uuid: str = None) -> List[Model]:
        """Get all stored models (without details) inside project(s)"""

        if not project_uuid:
            raise Exception("'get_all' models with project_id=" +project_uuid+ " is not implemented")

        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        model_domain_objs = []
        for json_model_obj in project_json_obj["models"]:
            model_domain_obj = self.__deserialize_model(project_ref=project_uuid, model_json_obj=json_model_obj)
            model_domain_objs.append(model_domain_obj)
        
        return model_domain_objs


    def get(self, model_uuid_or_name: str = None, project_uuid: str = None) -> Model:
        """Get stored model with attributes and references details"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        model_domain_obj = None
        for json_model_obj in project_json_obj["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                model_domain_obj = self.__deserialize_model(project_ref=project_uuid, model_json_obj=json_model_obj)
        return model_domain_obj
    
    def delete(self, project_uuid: str = None, model_uuid: str = None) -> None:
        """Delete model from related project"""
        self.__http_connector.delete(DBServiceSpecs.getModelPath(project_uuid=project_uuid, model_uuid=model_uuid))

    def update(self, project_uuid: str , model: Model) -> None:
        """Update existing an existing model"""
        body = self.__serialize_model(model_domain_obj=model)
        self.__http_connector.put(DBServiceSpecs.getModelPath(project_uuid=project_uuid, model_uuid=model.uuid), body)

    def save(self, project_uuid: str , model: Model, input: Input = None, output: Output = None, input_tools: List[Tool] = None, output_tools: List[Tool] = None) -> None:
        """Save new model"""
        if not model.uuid:
            model.uuid = str(uuid4())
        if not input.uuid:
            input.uuid = str(uuid4())
        if not output.uuid:
            output.uuid = str(uuid4())
        model_json_obj  = self.__serialize_model(model_domain_obj=model)
        input.model_ref = model
        input_json_obj  = InputDBDAO(None).serialize_input(input_domain_obj=input)
        output.model_ref = model
        output_json_obj = OutputDBDAO(None).serialize_output(output_domain_obj=output)
        input_tool_json_objs    = []
        output_tool_json_objs   = []

        for input_tool in input_tools:
            input_tool_json_objs.append(InputToolDBDAO(None).serialize_tool(tool_domain_obj=input_tool))

        for output_tool in output_tools:
            output_tool_json_objs.append(OutputToolDBDAO(None).serialize_tool(tool_domain_obj=output_tool))

        body = { "model": model_json_obj, "input": input_json_obj, "output": output_json_obj, "input_tools": input_tool_json_objs, "output_tools": output_tool_json_objs }
        self.__http_connector.post(DBServiceSpecs.getModelsPath(project_uuid=project_uuid), body)

    def __deserialize_model(self, project_ref, model_json_obj: Any) -> Model:
        classes = []
        if "model_metadata" in model_json_obj:
            if "classes" in model_json_obj["model_metadata"]:
                classes = model_json_obj["model_metadata"]["classes"]
        model_domain_obj = Model(
            uuid=model_json_obj["uuid"],
            name=model_json_obj["name"],
            model_type=ModelType(model_json_obj["model_type"]),
            training_type=TrainingType(model_json_obj["training_type"]),
            stage=Stage(model_json_obj["stage"]),
            model_metadata=ModelMetadata(classes=classes),
            experiments=[]
        )
        model_domain_obj.project_ref = project_ref
        return model_domain_obj 

    def __serialize_model(self, model_domain_obj: Model) -> Any:
        json_model_obj = dict({})

        if not model_domain_obj.uuid:
            model_domain_obj.uuid = str(uuid4())

        json_model_obj["uuid"] = model_domain_obj.uuid
        json_model_obj["name"] = model_domain_obj.name
        json_model_obj["model_type"] = model_domain_obj.model_type.value
        json_model_obj["training_type"] = model_domain_obj.training_type.value
        json_model_obj["stage"] = model_domain_obj.stage.value
        json_model_obj["model_metadata"] = {
            "classes": model_domain_obj.model_metadata.classes
        }

        return json_model_obj