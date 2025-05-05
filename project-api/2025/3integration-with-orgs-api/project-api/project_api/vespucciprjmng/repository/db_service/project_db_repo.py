
from typing import Any, List

from project_api.vespucciprjmng.dao.db_service.db_dao_factory import (
    DBDAOFactory,
)
from project_api.vespucciprjmng.dao.db_service.domain.db_tool import DBTool
from project_api.vespucciprjmng.domain.experiment import Experiment
from project_api.vespucciprjmng.domain.input import Input, InputType
from project_api.vespucciprjmng.domain.log import DeviceDescription, Log
from project_api.vespucciprjmng.domain.model import (
    Model,
    ModelMetadata,
    ModelType,
    Stage,
    TrainingType,
)
from project_api.vespucciprjmng.domain.output import Output, OutputType
from project_api.vespucciprjmng.domain.project import Project
from project_api.vespucciprjmng.domain.test import Test
from project_api.vespucciprjmng.repository.exceptions.method_not_implemented import (
    MethodNotImplemented,
)
from project_api.vespucciprjmng.repository.exceptions.resource_already_exist import (
    ResourceAlreadyExisting,
    ResourceKind,
)
from project_api.vespucciprjmng.repository.project_repo import ProjectRepo


class ProjectDBRepo(ProjectRepo):

    def __init__(self, user_id: str, service_uri: str):
        self.dao_factory = DBDAOFactory(user_id=user_id, service_uri=service_uri)

    def get_projects(self) -> List[Project]:
        return self.dao_factory.get_project_dao_instance().get_all()
    
    def get_project(self, project_uuid: str) -> Project:
        project: Project    = self.dao_factory.get_project_dao_instance().get(uuid=project_uuid)
        models: List[Model] = self.dao_factory.get_model_dao_instance().get_all(project_uuid=project_uuid)
        inputs: List[Input] = []
        outputs: List[Output] = []
        
        for model in models:
            input   = self.dao_factory.get_input_dao_instance().get(project_uuid=project.uuid, model_uuid_or_name=model.uuid)
            output  = self.dao_factory.get_output_dao_instance().get(project_uuid=project.uuid, model_uuid_or_name=model.uuid)

            logs = self.dao_factory.get_log_dao_instance().get_all(project_uuid=project.uuid, model_uuid_or_name_or_input_uuid=model.uuid)
            experiments = self.dao_factory.get_experiment_dao_instance().get_all(project_uuid=project.uuid, model_uuid_or_name=model.uuid)
            tests = []
            for experiment in experiments:
                experiment_tests = self.dao_factory.get_test_dao_instance().get_all(project_uuid=project.uuid, model_uuid_or_name_or_output_uuid=model.uuid, experiment_uuid_or_name=experiment.uuid)
                for experiment_test in experiment_tests:
                    tests.append(experiment_test)

            input_tools = self.dao_factory.get_input_tool_dao_instance().get_all(project_uuid=project.uuid, model_uuid_or_name_or_input_uuid=model.uuid)
            output_tools = self.dao_factory.get_output_tool_dao_instance().get_all(project_uuid=project.uuid, model_uuid_or_name_or_output_uuid=model.uuid)

            model.experiments = experiments
            model.input = input
            model.output = output
            
            input.logs  = logs
            input.tools = input_tools
            output.tests= tests
            output.tools= output_tools

            inputs.append(input)
            outputs.append(output)

        project.inputs  = inputs
        project.models  = models
        project.outputs = outputs
        return project

    def create_project(self, name: str = None, description: str = "", version: str = "0.0.1", uuid = None) -> Project:
        existing_projects = self.dao_factory.get_project_dao_instance().get_all()
        for existing_project in existing_projects:
            if existing_project.name == name:
                raise ResourceAlreadyExisting(existing_project.uuid, existing_project.name, ResourceKind.PROJECT)

        new_project = Project(uuid=uuid, name=name, description=description, version=version)
        self.dao_factory.get_project_dao_instance().save(new_project)
        existing_projects = self.dao_factory.get_project_dao_instance().get_all()
        for existing_project in existing_projects:
            return self.dao_factory.get_project_dao_instance().get(uuid=existing_project.uuid)

    def create_model(self, project_uuid:str, model_name: str, model_type: ModelType, model_metadata: ModelMetadata, training_type: TrainingType, stage: Stage, input_type: InputType,output_type: OutputType, input_tool: DBTool, output_tool: DBTool, model_uuid: str = None, input_uuid: str = None,  output_uuid: str = None) -> Model:
        existing_models = self.dao_factory.get_model_dao_instance().get_all(project_uuid=project_uuid)
        for existing_model in existing_models:
            if existing_model.name == model_name:
                raise ResourceAlreadyExisting(existing_model.uuid, existing_model.name, ResourceKind.MODEL)

        new_model = Model(
            uuid=model_uuid,
            name=model_name,
            model_type=model_type,
            model_metadata=model_metadata,
            training_type=training_type,
            stage=stage
        )
        new_input = Input(uuid=input_uuid, input_type=input_type)
        new_output = Output(uuid=output_uuid, output_type=output_type)
        self.dao_factory.get_model_dao_instance().save(project_uuid=project_uuid, model=new_model, input=new_input, output=new_output, input_tools=[input_tool], output_tools=[output_tool])
        return self.dao_factory.get_model_dao_instance().get(project_uuid=project_uuid, model_uuid_or_name=model_name)

    def create_log_from_board(self, project_uuid: str, model_name: str, name: str, description: str, annotated: bool, start_time: str, end_time: str, device_description: DeviceDescription, uuid: str = None) -> Log:
        # existing_logs = self.dao_factory.get_log_dao_instance().get_all(project_uuid=project_uuid, model_uuid_or_name_or_input_uuid=model_name)
        # for existing_log in existing_logs:
        #     if existing_log.name == model_name or existing_log.uuid == uuid:
        #         raise ResourceAlreadyExisting(existing_log.uuid, existing_log.name, ResourceKind.LOG)

        new_log = Log(
            uuid=uuid,
            name=name,
            description=description,
            annotated=annotated,
            start_time=start_time,
            end_time=end_time,
            device_description=device_description
        )
        try:
            self.dao_factory.get_log_dao_instance().get(project_uuid=project_uuid, model_uuid_or_name_or_input_uuid=model_name, log_name_or_uuid=uuid)
            self.dao_factory.get_log_dao_instance().update(project_uuid=project_uuid, model_uuid_or_name_or_input_uuid=model_name, log=new_log)
        except:
            self.dao_factory.get_log_dao_instance().save(project_uuid=project_uuid, model_uuid_or_name_or_input_uuid=model_name, log=new_log)
        return self.dao_factory.get_log_dao_instance().get(project_uuid=project_uuid, model_uuid_or_name_or_input_uuid=model_name, log_name_or_uuid=name)

    def create_experiment(self, project_uuid: str, model_uuid_or_name: str, name: str, description: str, model_dev_file: str, uuid: str = None) -> Experiment:
        new_experiment = Experiment(uuid=uuid, name=name, description=description, model_dev_file=model_dev_file)
        self.dao_factory.get_experiment_dao_instance().save(project_uuid=project_uuid, model_uuid_or_name=model_uuid_or_name, experiment=new_experiment)
        return self.dao_factory.get_experiment_dao_instance().get(project_uuid=project_uuid, model_uuid_or_name=model_uuid_or_name, experiment_uuid_or_name=name)

    def create_test(self, project_uuid: str, model_uuid_or_name: str, experiment_uuid_or_name: str, name: str, model_file: str, parameters: Any, uuid: str = None) -> Test:
        new_test = Test(uuid=uuid, name=name, model_file=model_file, parameters=parameters)
        self.dao_factory.get_test_dao_instance().save(project_uuid=project_uuid, model_uuid_or_name_or_output_uuid=model_uuid_or_name, experiment_uuid_or_name=experiment_uuid_or_name, test=new_test)
        return self.dao_factory.get_test_dao_instance().get(project_uuid=project_uuid, model_uuid_or_name_or_output_uuid=model_uuid_or_name, experiment_uuid_or_name=experiment_uuid_or_name, test_uuid_or_name=name)
    
    def create_deployment(self, *args):
        raise MethodNotImplemented("create_deployment")