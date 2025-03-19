
from typing import Any, List
from uuid import uuid4

from project_api.vespucciprjmng.dao.filesystem.json_data_connector import (
    JSONDataConnector,
)
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import (
    ProjectFileDAO,
)
from project_api.vespucciprjmng.dao.filesystem.util import get_project_file_name
from project_api.vespucciprjmng.dao.model_dao import ModelDAO
from project_api.vespucciprjmng.domain.dataset import Dataset
from project_api.vespucciprjmng.domain.model import (
    Model,
    ModelMetadata,
    ModelTarget,
    ModelType,
)


class ModelFileDAO(ModelDAO):
    """Model data access object for JSON file"""
    
    def __init__(self, data_session: JSONDataConnector):
        super().__init__(data_session)
        self.project_dao = ProjectFileDAO(data_session)

    def get_all(self, project_name: str = None) -> List[Model]:
        """Get all stored models (without details) inside project(s)"""
        if not project_name:
            raise Exception("'get_all' models with project_id=" +project_name+ " is not implemented")

        self.data_session.connect(get_project_file_name(project_name))

        model_domain_objs = []
        for json_model_obj in self.data_session.json_file["models"]:
            model_domain_obj = self.__deserialize_model(project_ref=project_name, json_model_obj=json_model_obj)
            if hasattr(model_domain_obj, "dataset"): # Append iff dataset is present
                model_domain_objs.append(model_domain_obj)
        
        self.data_session.dispose()
        return model_domain_objs

    def get(self, model_uuid_or_name: str = None, project_name: str = None) -> Model:
        """Get model with all details"""
        
        if not project_name:
            raise Exception("'get model' method without 'project_name' input attribute is not implemented")
        
        self.data_session.connect(get_project_file_name(project_name))

        model_domain_obj = None
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                model_domain_obj = self.__deserialize_model(project_ref=project_name, json_model_obj=json_model_obj)
        
        self.data_session.dispose()
        return model_domain_obj if hasattr(model_domain_obj, "dataset") else None
    
    def delete(self, project_name: str = None, model_uuid_or_name: str = None) -> None:
        """Delete model from related project"""
        self.data_session.connect(get_project_file_name(project_name))

        filtered_json_model_objs = []
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] != model_uuid_or_name and json_model_obj["name"] != model_uuid_or_name:
                filtered_json_model_objs.append(json_model_obj)
        self.data_session.json_file["models"] = filtered_json_model_objs

        self.data_session.save()
        self.data_session.dispose()

    def patch(self, project_name: str, model_uuid_or_name: str, model: Model) -> None:
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_model_obj = None
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model_uuid_or_name or json_model_obj["name"] == model_uuid_or_name:
                selected_json_model_obj = json_model_obj

        # Update only dataset_id parameters currently
        if model.dataset.dataset_id:    
            selected_json_model_obj["dataset"]["dataset_id"] = model.dataset.dataset_id
        if model.dataset.name:
            selected_json_model_obj["dataset"]["name"] = model.dataset.name

        if model.model_metadata.classes:
            selected_json_model_obj["metadata"]["classes"] = model.model_metadata.classes
        
        self.data_session.save()
        self.data_session.dispose()

    def clone(self, project_name: str, clone_model_uuid_or_name: str, model_uuid_or_name: str) -> None:
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_model_obj = None
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == clone_model_uuid_or_name or json_model_obj["name"] == clone_model_uuid_or_name:
                selected_json_model_obj = json_model_obj

        cloned_json_model_obj = self.__copy_model(selected_json_model_obj, model_uuid_or_name)

        self.data_session.json_file["models"].append(cloned_json_model_obj)

        self.data_session.save()
        self.data_session.dispose()

    def save(self, project_name: str , model: Model) -> None:
        """Save new model or update existing model"""
    
        self.data_session.connect(get_project_file_name(project_name))

        selected_json_model_obj = None
        for json_model_obj in self.data_session.json_file["models"]:
            if json_model_obj["uuid"] == model.uuid:
                selected_json_model_obj = json_model_obj
                break

        patched_json_model_obj = self.__serialize_model(model)

        if selected_json_model_obj:
            selected_json_model_obj.update(patched_json_model_obj)
            # if not "experiments" in selected_json_model_obj:
            #     selected_json_model_obj["experiments"] = []   
        else:
            # if not "experiments" in patched_json_model_obj:
            #     patched_json_model_obj["experiments"] = []   
            self.data_session.json_file["models"].append(patched_json_model_obj)

        self.data_session.save()
        self.data_session.dispose()

    def __deserialize_model(self, project_ref, json_model_obj) -> Model:
        model_domain_obj = Model()
        model_domain_obj.uuid = json_model_obj["uuid"]
        model_domain_obj.name = json_model_obj["name"]        
        
        model_domain_obj.dataset = Dataset(json_model_obj["dataset"]["name"], 
                                            json_model_obj["dataset"]["dataset_id"])
        
        model_domain_obj.project_ref = project_ref
        model_domain_obj.model_metadata = ModelMetadata(classes=[])
        model_domain_obj.model_metadata.type = ModelType(json_model_obj["metadata"]["type"])
        
        model_domain_obj.target = ModelTarget(json_model_obj["target"]["type"], 
                                                    json_model_obj["target"]["component"],
                                                    json_model_obj["target"]["device"])
    
        for class_name in json_model_obj["metadata"]["classes"]:
            model_domain_obj.model_metadata.classes.append(class_name)

        if "creation_time" in json_model_obj:
            model_domain_obj.creation_time = str(json_model_obj["creation_time"])
        if "last_update_time" in json_model_obj:
            model_domain_obj.last_update_time = json_model_obj["last_update_time"]
        
        return model_domain_obj

    def __serialize_model(self, model_domain_obj: Model) -> Any:
        json_model_obj = dict({})

        if not model_domain_obj.uuid:
            model_domain_obj.uuid = str(uuid4())

        json_model_obj["uuid"] = model_domain_obj.uuid
        json_model_obj["name"] = model_domain_obj.name
        
        json_model_obj["dataset"] = {
            "name": model_domain_obj.dataset.name,
            "dataset_id":  model_domain_obj.dataset.dataset_id
        }
        
        json_model_obj["metadata"] = {
            'type': model_domain_obj.model_metadata.type.value,
            "classes": model_domain_obj.model_metadata.classes
        }
        json_model_obj["target"] = {
            "type": model_domain_obj.target.type,
            "component": model_domain_obj.target.component,
            "device": model_domain_obj.target.device
        }
        json_model_obj["creation_time"] = model_domain_obj.creation_time
        json_model_obj["last_update_time"] = model_domain_obj.last_update_time
        
        return json_model_obj
    
    def __copy_model(self, json_model_obj, model_name) -> Any:
        copy_json_model_obj = dict({})

        copy_json_model_obj["uuid"] = str(uuid4())
        copy_json_model_obj["name"] = model_name
        
        copy_json_model_obj["dataset"] = {
            "name": json_model_obj["dataset"]["name"],
            "dataset_id":  json_model_obj["dataset"]["dataset_id"]
        }
        
        copy_json_model_obj["metadata"] = {
            'type': json_model_obj["metadata"]["type"],
            "classes": json_model_obj["metadata"]["classes"]
        }
        copy_json_model_obj["target"] = {
            "type": json_model_obj["target"]["type"],
            "component": json_model_obj["target"]["component"],
            "device": json_model_obj["target"]["device"]
        }
        
        return copy_json_model_obj