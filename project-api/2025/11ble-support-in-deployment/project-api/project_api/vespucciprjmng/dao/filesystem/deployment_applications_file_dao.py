from typing import List, Any
from uuid import uuid4
from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import ProjectFileDAO
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.deployment_dao import DeploymentDAO
from project_api.vespucciprjmng.domain.deployment import Application
from project_api.vespucciprjmng.domain.deployment import Bluestv3Payload, Bluestv3PayloadDecodingSchemaInstance

import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DeploymentApplicationFileDAO(DeploymentDAO):
    """Deployment Application data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str) -> List[Application]:
        """Get all stored applications inside a project"""

        logger.debug(f"> DeploymentApplicationFileDAO.get_all project={project_name}")
        self.data_session.connect(get_project_file_name(project_name))

        application_domain_objs = []
        if "applications" in self.data_session.json_file:
            logger.debug(
                f"Found {len(self.data_session.json_file['applications'])} applications in project {project_name}"
            )
            for application_domain_obj in self.data_session.json_file["applications"]:
                logger.debug(
                    f"Deserializing application uuid={application_domain_obj.get('uuid', 'unknown')}"
                )
                application_domain_obj = self.__deserialize_application(json_application_obj=application_domain_obj)
                application_domain_objs.append(application_domain_obj)
        else:
            logger.debug("No 'applications' key present in project file")
        
        self.data_session.dispose()
        logger.debug(f"< DeploymentApplicationFileDAO.get_all count={len(application_domain_objs)}")

        return application_domain_objs

    def get(self, project_name: str, application_uuid_or_index: str) -> Application:
        """Get application given a application ID"""

        logger.debug(
            f"> DeploymentApplicationFileDAO.get project={project_name} uuid_or_index={application_uuid_or_index}"
        )
        self.data_session.connect(get_project_file_name(project_name))

        application_domain_obj = None

        if "applications" in self.data_session.json_file:
            logger.debug("Scanning applications for requested uuid")
            for json_application_obj in self.data_session.json_file["applications"]:
                if json_application_obj.get("uuid") == application_uuid_or_index:
                    logger.debug("Application match found; deserializing")
                    application_domain_obj = self.__deserialize_application(json_application_obj=json_application_obj)
                    break
        else:
            logger.debug("No 'applications' key present in project file")
        
        self.data_session.dispose()
        logger.debug(
            f"< DeploymentApplicationFileDAO.get found={application_domain_obj is not None}"
        )

        return application_domain_obj
    
    def delete(self, project_name: str, application_uuid_or_name: str) -> None:
        """Delete application from related project"""
        logger.debug(
            f"> DeploymentApplicationFileDAO.delete project={project_name} uuid_or_name={application_uuid_or_name}"
        )
        self.data_session.connect(get_project_file_name(project_name))

        filtered_json_application_objs = []
        selected_json_application_obj = None
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] != application_uuid_or_name:
                filtered_json_application_objs.append(json_application_obj)
            else:
                selected_json_application_obj = json_application_obj
        self.data_session.json_file["applications"] = filtered_json_application_objs
        
        if selected_json_application_obj:
            logger.debug("Application deleted from list")
        else:
            logger.warning("Requested application to delete not found")

        self.data_session.save()
        self.data_session.dispose()
        logger.debug("< DeploymentApplicationFileDAO.delete done")
        return
    
    def patch(self, project_name: str, application_uuid_or_name: str, app: Application) -> None:
        """Patch application from related project"""
        logger.debug(
            f"> DeploymentApplicationFileDAO.patch project={project_name} uuid_or_name={application_uuid_or_name}"
        )
        self.data_session.connect(get_project_file_name(project_name))
        
        selected_json_application_obj = None
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] == application_uuid_or_name:
                selected_json_application_obj = json_application_obj
        
        if not selected_json_application_obj:
            logger.warning("Application to patch not found")
        else:
            logger.debug("Patching application fields that are present in input")
            # Update any provided parameter
            if app.binary_id and "binary_id" in selected_json_application_obj:
                selected_json_application_obj["binary_id"] = app.binary_id
            if app.binary_uri and "binary_uri" in selected_json_application_obj:    
                selected_json_application_obj["binary_uri"] = app.binary_uri
            if app.device_manifest_uri and "device_manifest_uri" in selected_json_application_obj:
                selected_json_application_obj["device_manifest_uri"] = app.device_manifest_uri
            if app.device_template_id and "device_template_id" in selected_json_application_obj:    
                selected_json_application_obj["device_template_id"] = app.device_template_id
            if app.device_template_uri and "device_template_uri" in selected_json_application_obj:    
                selected_json_application_obj["device_template_uri"] = app.device_template_uri
            if app.image_uri and "image_uri" in selected_json_application_obj:
                selected_json_application_obj["image_uri"] = app.image_uri
            if app.module_id and "module_id" in selected_json_application_obj:    
                selected_json_application_obj["module_id"] = app.module_id
            if app.protocol and "protocol" in selected_json_application_obj:
                selected_json_application_obj["protocol"] = app.protocol
            if app.type and "type" in selected_json_application_obj:    
                selected_json_application_obj["type"] = app.type

        self.data_session.save()
        self.data_session.dispose()
        logger.debug("< DeploymentApplicationFileDAO.patch done")
        return

    def save(self, project_name: str, application: Application) -> None:
        """Save new application or update existing application"""
    
        logger.debug(
            f"> DeploymentApplicationFileDAO.save project={project_name} application_uuid={application.uuid}"
        )
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_application_obj = None
        for json_application_obj in self.data_session.json_file["applications"]:
            if json_application_obj["uuid"] == application.uuid:
                selected_json_application_obj = json_application_obj
                break

        patched_json_application_obj = self.__serialize_application(application)
        logger.debug(
            f"Prepared serialized application keys={list(patched_json_application_obj.keys())}"
        )

        if selected_json_application_obj:
            logger.debug("Updating existing application")
            selected_json_application_obj.update(patched_json_application_obj)
        else:  
            logger.debug("Appending new application")
            self.data_session.json_file["applications"].append(patched_json_application_obj)

        self.data_session.save()
        self.data_session.dispose()
        logger.debug("< DeploymentApplicationFileDAO.save done")
        pass

    def __deserialize_application(self, json_application_obj) -> Application:
        logger.debug(f'>DeploymentApplicationFileDAO.De__deserialize_application')
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
        if "bluestv3_payload" in json_application_obj:
            payload = json_application_obj.get("bluestv3_payload", {})
            logger.debug(f'collecting bluestv3_payload \nbluestv3_payload: {json.dumps(payload)}')
            if payload != {}:            
                p = Bluestv3Payload()
                p.device_id = payload.get("device_id", "")
                p.fw_id = payload.get("fw_id", "")
                p.payload_id = payload.get("payload_id", "")

                schema_list = payload.get("decoding_schema", [{}])
                if not isinstance(schema_list, list):
                    raise ValueError("decoding_schema must be a list")                
                p.decoding_schema = [ Bluestv3PayloadDecodingSchemaInstance(
                        telemetry=ds.get("telemetry", ""), type_=ds.get("type", "")
                    )
                    for ds in schema_list if isinstance(ds, dict)
                ] 
            application_domain_obj.bluestv3_payload = p
        else:
            application_domain_obj.bluestv3_payload             = None
        logger.debug(f'< DeploymentApplicationFileDAO.De__deserialize_application')
            
        return application_domain_obj

    def __serialize_application(self, application_obj: Application) -> Any:
        logger.debug(f'> DeploymentApplicationFileDAO.__serialize_application')
        
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

        payload = application_obj.bluestv3_payload if hasattr(application_obj, "bluestv3_payload") else None
        logger.debug(f'DeploymentApplicationFileDAO.__serialize_application: Serialize bluestv3_payload fields')
        if payload is not None:
            try:
                logger.debug(f'serializing bluestv3_payload')
                json_application_domain_obj["bluestv3_payload"] = payload.to_dict()
            except AttributeError:
                logger.warning('bluestv3_payload object missing to_dict; skipping serialization')
                
        logger.debug(f'< DeploymentApplicationFileDAO.__serialize_application')
                
        return json_application_domain_obj
