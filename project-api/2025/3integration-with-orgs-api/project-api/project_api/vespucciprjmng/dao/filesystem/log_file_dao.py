
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.log_dao import LogDAO
from project_api.vespucciprjmng.domain.log import DeviceDescription, Log
from project_api.vespucciprjmng.utils import read_json_attribute


class LogFileDAO(LogDAO):
    """Log data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str, model_uuid_or_name_or_input_uuid: str = None) -> List[Log]:
        """Get all stored logs (without details) inside a project/model or input"""
        
        if not model_uuid_or_name_or_input_uuid:
            raise Exception("'get_all' logs for all models/inputs is not implemented")
        
        self.data_session.connect(get_project_file_name(project_name))

        log_domain_objs = []

        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)

        for json_log_obj in selected_json_input_obj["logs"]:
            log_domain_obj = self.__deserialize_log(project_ref=project_name, json_log_obj=json_log_obj)
            log_domain_objs.append(log_domain_obj)
        
        self.data_session.dispose()

        return log_domain_objs

    def get(self, project_name: str, model_uuid_or_name_or_input_uuid: str, log_name_or_uuid: str) -> Log:
        """Get log (with all details) given project/model or input"""
        
        self.data_session.connect(get_project_file_name(project_name))

        log_domain_obj = None

        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)
        for json_log_obj in selected_json_input_obj["logs"]:
            if json_log_obj["name"] == log_name_or_uuid or json_log_obj["uuid"] == log_name_or_uuid:
                log_domain_obj = self.__deserialize_log(project_ref=project_name, json_log_obj=json_log_obj)
                break
        
        self.data_session.dispose()

        return log_domain_obj
    
    def delete(self, project_name: str, model_uuid_or_name_or_input_uuid: str, log_name_or_uuid: str) -> None:
        """Delete log from related project/model/input"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_log_domain_objs = []
        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)
        for json_log_obj in selected_json_input_obj["logs"]:
            if not (json_log_obj["name"] == log_name_or_uuid or json_log_obj["uuid"] == log_name_or_uuid) :
                filtered_log_domain_objs.append(json_log_obj)
                break
        selected_json_input_obj["logs"] = filtered_log_domain_objs
        
        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str, model_uuid_or_name_or_input_uuid: str, log: Log) -> None:
        """Save new log or update existing log for given model/input"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_log_json_obj = None
        selected_json_input_obj = self.__get_input_json_obj(model_uuid_or_name_or_input_uuid)

        for json_log_obj in selected_json_input_obj["logs"]:
            if json_log_obj["name"] == log.name or json_log_obj["uuid"] == log.uuid:
                selected_log_json_obj = json_log_obj
                break

        patched_json_log_obj = self.__serialize_log(log)

        if selected_log_json_obj:
            selected_log_json_obj.update(patched_json_log_obj) 
        else:
            selected_json_input_obj["logs"].append(patched_json_log_obj)

        self.data_session.save()
        self.data_session.dispose()


    def __get_input_json_obj(self, model_uuid_or_name_or_input_uuid: str) -> Any:
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name_or_input_uuid or json_model_obj["name"] == model_uuid_or_name_or_input_uuid:
                selected_model= json_model_obj

        for json_input_obj in self.data_session.json_file["inputs"]:
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