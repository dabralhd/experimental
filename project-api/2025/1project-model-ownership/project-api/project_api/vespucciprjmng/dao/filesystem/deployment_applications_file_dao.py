
from typing import List, Any
from uuid import uuid4
from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import ProjectFileDAO
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.deployment_dao import DeploymentDAO
from project_api.vespucciprjmng.domain.deployment import Application

class DeploymentApplicationFileDAO(DeploymentDAO):
    """Deployment Application data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str) -> List[Application]:
        """Get all stored applications inside a project"""

        self.data_session.connect(get_project_file_name(project_name))

        application_domain_objs = []
        if "applications" in self.data_session.json_file:
            for application_domain_obj in self.data_session.json_file["applications"]:
                application_domain_obj = self.__deserialize_application(json_application_obj=application_domain_obj)
                application_domain_objs.append(application_domain_obj)
        
        self.data_session.dispose()

        return application_domain_objs

    def get(self, project_name: str, application_uuid_or_index: str) -> Application:
        """Get application given a application ID"""

        self.data_session.connect(get_project_file_name(project_name))

        application_domain_obj = None

        if "applications" in self.data_session.json_file:
            for json_application_obj in self.data_session.json_file["applications"]:
                if json_application_obj["uuid"] == application_uuid_or_index:
                    application_domain_obj = self.__deserialize_application(json_application_obj=json_application_obj)
        
        self.data_session.dispose()

        return application_domain_obj
    
    def delete(self, project_name: str, application_uuid_or_name: str) -> None:
        """Delete application from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_json_application_objs = []
        selected_json_application_obj = None
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] != application_uuid_or_name:
                filtered_json_application_objs.append(json_application_obj)
            else:
                selected_json_application_obj = json_application_obj
        self.data_session.json_file["applications"] = filtered_json_application_objs
        
        self.data_session.save()
        self.data_session.dispose()
        return

    def save(self, project_name: str, application: Application) -> None:
        """Save new application or update existing application"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_application_obj = None
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] == application.uuid:
                selected_json_application_obj = json_application_obj
                break

        patched_json_application_obj = self.__serialize_application(application)

        if selected_json_application_obj:
            selected_json_application_obj.update(patched_json_application_obj)
        else:  
            self.data_session.json_file["applications"].append(patched_json_application_obj)

        self.data_session.save()
        self.data_session.dispose()
        pass

    def __deserialize_application(self, json_application_obj) -> Application:
        application_domain_obj = Application()
       
        application_domain_obj.uuid                 = json_application_obj["uuid"]
        application_domain_obj.type                 = json_application_obj["type"]
        if "device_template_uri" in json_application_obj:
            application_domain_obj.device_template_uri  = json_application_obj["device_template_uri"]
        else:
            application_domain_obj.device_template_uri  = None
        if "device_template_id" in json_application_obj:
            application_domain_obj.device_template_id   = json_application_obj["device_template_id"]
        else:
            application_domain_obj.device_template_id   = None    
        if "device_manifest_uri" in json_application_obj:
            application_domain_obj.device_manifest_uri  = json_application_obj["device_manifest_uri"]
        else:
            application_domain_obj.device_manifest_uri  = None
        if "image_uri" in json_application_obj:
            application_domain_obj.image_uri            = json_application_obj["image_uri"]
        else:
            application_domain_obj.image_uri            = None
        if "module_id" in json_application_obj:
            application_domain_obj.module_id            = json_application_obj["module_id"]
        else:
            application_domain_obj.module_id            = None
        if "binary_uri" in json_application_obj:
            application_domain_obj.binary_uri           = json_application_obj["binary_uri"]
        else:
            application_domain_obj.binary_uri           = None
        if "binary_id" in json_application_obj:
            application_domain_obj.binary_id            = json_application_obj["binary_id"]
        else:
            application_domain_obj.binary_id            = None
        if "protocol" in json_application_obj:
            application_domain_obj.protocol             = json_application_obj["protocol"]        
        else:
            application_domain_obj.protocol             = None
            
        return application_domain_obj

    def __serialize_application(self, application_obj: Application) -> Any:
        json_application_domain_obj = dict({})

        json_application_domain_obj["uuid"] = application_obj.uuid
        json_application_domain_obj["type"] = application_obj.type
        if application_obj.device_template_uri:
            json_application_domain_obj["device_template_uri"] = application_obj.device_template_uri
        if application_obj.device_template_id:
            json_application_domain_obj["device_template_id"] = application_obj.device_template_id
        if application_obj.device_manifest_uri:
            json_application_domain_obj["device_manifest_uri"] = application_obj.device_manifest_uri
        if application_obj.image_uri:
            json_application_domain_obj["image_uri"] = application_obj.image_uri
        if application_obj.module_id:
            json_application_domain_obj["module_id"] = application_obj.module_id
        if application_obj.binary_uri:
            json_application_domain_obj["binary_uri"] = application_obj.binary_uri
        if application_obj.binary_id is not None:
            json_application_domain_obj["binary_id"] = application_obj.binary_id
        if application_obj.protocol is not None:
            json_application_domain_obj["protocol"] = application_obj.protocol       
        
        return json_application_domain_obj