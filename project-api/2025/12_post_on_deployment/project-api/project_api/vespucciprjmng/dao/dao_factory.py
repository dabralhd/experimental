
from abc import abstractmethod

from project_api.vespucciprjmng.dao.deployment_dao import DeploymentDAO
from project_api.vespucciprjmng.dao.model_dao import ModelDAO
from project_api.vespucciprjmng.dao.project_dao import ProjectDAO


class DAOFactory():
    
    @abstractmethod
    def get_project_dao_instance() -> ProjectDAO:
        pass

    @abstractmethod
    def get_deployment_dao_instance() -> DeploymentDAO:
        pass

    @abstractmethod
    def get_model_dao_instance() -> ModelDAO:
        pass

    @abstractmethod
    def get_input_dao_instance():
        pass

    @abstractmethod
    def get_output_dao_instance():
        pass

    @abstractmethod
    def get_experiment_dao_instance():
        pass

    @abstractmethod
    def get_log_dao_instance():
        pass

    @abstractmethod
    def get_test_dao_instance():
        pass

    @abstractmethod
    def get_input_tool_dao_instance():
        pass

    @abstractmethod
    def get_output_tool_dao_instance():
        pass

    @abstractmethod
    def get_job_dao_instance():
        pass