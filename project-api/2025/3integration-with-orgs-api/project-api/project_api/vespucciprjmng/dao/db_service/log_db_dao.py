
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.db_service.http_connector import (
    HTTPDataConnector,
)
from project_api.vespucciprjmng.dao.db_service.service_specs import (
    DBServiceSpecs,
)
from project_api.vespucciprjmng.dao.log_dao import LogDAO
from project_api.vespucciprjmng.domain.log import DeviceDescription, Log
from project_api.vespucciprjmng.utils import read_json_attribute


class LogDBDAO(LogDAO):
    """Log data access object for DB service"""
    
    def __init__(self, service_uri: str):
        self.__http_connector = HTTPDataConnector(service_uri)


    def get_all(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str = None) -> List[Log]:
        """Get all stored logs (without details) inside a project/model or input"""
        
        if not model_uuid_or_name_or_input_uuid:
            raise Exception("'get_all' logs for all models/inputs is not implemented")
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        log_domain_objs = []

        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)

        for json_log_obj in selected_json_input_obj["logs"]:
            log_domain_obj = self.__deserialize_log(project_ref=project_uuid, json_log_obj=json_log_obj)
            log_domain_objs.append(log_domain_obj)
        
        return log_domain_objs

    def get(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, log_name_or_uuid: str) -> Log:
        """Get log (with all details) given project/model or input"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        log_domain_obj = None

        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        for json_log_obj in selected_json_input_obj["logs"]:
            if json_log_obj["name"] == log_name_or_uuid or json_log_obj["uuid"] == log_name_or_uuid:
                log_domain_obj = self.__deserialize_log(project_ref=project_uuid, json_log_obj=json_log_obj)
                break

        return log_domain_obj
    
    def delete(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, log_name_or_uuid: str) -> None:
        """Delete log from related project/model/input"""
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)
        for log_json_obj in selected_json_input_obj["logs"]:
            if log_name_or_uuid == log_json_obj["name"] or log_name_or_uuid == log_json_obj["uuid"]:
                self.__http_connector.delete(DBServiceSpecs.getLogPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"], log_uuid=log_json_obj["uuid"]))
                break

    def update(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, log: Log) -> None:
        """Update existing log for given model/input"""
    
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        selected_log_json_obj = None
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)

        for json_log_obj in selected_json_input_obj["logs"]:
            if json_log_obj["name"] == log.name or json_log_obj["uuid"] == log.uuid:
                selected_log_json_obj = json_log_obj
                break

        patched_json_log_obj = self.__serialize_log(log)

        # if selected_log_json_obj:
        self.__http_connector.put(DBServiceSpecs.getLogPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"], log_uuid=selected_log_json_obj["uuid"]), patched_json_log_obj)
        # else:
        #     self.__http_connector.post(DBServiceSpecs.getLogsPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"]), patched_json_log_obj)


    def save(self, project_uuid: str, model_uuid_or_name_or_input_uuid: str, log: Log) -> None:
        """Save new log or update existing log for given model/input"""
        
        project_json_obj = self.__http_connector.get(DBServiceSpecs.getProjectPath(project_uuid=project_uuid))

        # selected_log_json_obj = None
        selected_json_input_obj = self.__get_input_json_obj(project_json_obj, model_uuid_or_name_or_input_uuid)

        # for json_log_obj in selected_json_input_obj["logs"]:
        #     if json_log_obj["name"] == log.name or json_log_obj["uuid"] == log.uuid:
        #         selected_log_json_obj = json_log_obj
        #         break

        patched_json_log_obj = self.__serialize_log(log)

        # if selected_log_json_obj:
        #     self.__http_connector.put(DBServiceSpecs.getLogPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"], log_uuid=selected_log_json_obj["uuid"]), patched_json_log_obj)
        # else:
        self.__http_connector.post(DBServiceSpecs.getLogsPath(project_uuid=project_uuid, input_uuid=selected_json_input_obj["uuid"]), patched_json_log_obj)


    def __get_input_json_obj(self, project_json_obj: Any, model_uuid_or_name_or_input_uuid: str) -> Any:
        for json_model_obj in project_json_obj["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_model_obj["name"] == model_uuid_or_name_or_input_uuid:
                selected_model= json_model_obj

        for json_input_obj in project_json_obj["inputs"]:
            if json_input_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_input_obj["model_ref"] == selected_model["uuid"]:
                return json_input_obj


    def __deserialize_log(self, project_ref, json_log_obj) -> Log:

        log_domain_obj = Log()
        log_domain_obj.project_ref  = project_ref
        log_domain_obj.uuid         = json_log_obj["uuid"]
        log_domain_obj.name         = json_log_obj["name"]

        log_domain_obj.annotated    = read_json_attribute(json_log_obj, "annotated")
        log_domain_obj.description  = read_json_attribute(json_log_obj, "description")
        log_domain_obj.start_time  = read_json_attribute(json_log_obj, "start_time")
        log_domain_obj.end_time  = read_json_attribute(json_log_obj, "end_time")
        if "device_description" in json_log_obj:
            log_domain_obj.device_description = DeviceDescription(
                part_number=read_json_attribute(json_log_obj["device_description"], "part_number"),
                serial_number=read_json_attribute(json_log_obj["device_description"],"serial_number"),
                alias=read_json_attribute(json_log_obj["device_description"], "alias"),
                fw_name=read_json_attribute(json_log_obj["device_description"], "fw_name"),
                fw_version=read_json_attribute(json_log_obj["device_description"], "fw_version")
            )
        
        return log_domain_obj

    def __serialize_log(self, log_domain_obj: Log) -> Any:
        json_log_obj = dict({})

        if not log_domain_obj.uuid:
            log_domain_obj.uuid = str(uuid4())

        json_log_obj["uuid"]        = log_domain_obj.uuid
        json_log_obj["name"]        = log_domain_obj.name
        json_log_obj["annotated"]   = log_domain_obj.annotated
        json_log_obj["description"] = log_domain_obj.description
        json_log_obj["start_time"]  = log_domain_obj.start_time
        json_log_obj["end_time"]    = log_domain_obj.end_time
        json_log_obj["device_description"] = {
            "part_number": log_domain_obj.device_description.part_number,
            "serial_number": log_domain_obj.device_description.serial_number,
            "alias": log_domain_obj.device_description.alias,
            "fw_name": log_domain_obj.device_description.fw_name,
            "fw_version": log_domain_obj.device_description.fw_version
        }
        
        return json_log_obj