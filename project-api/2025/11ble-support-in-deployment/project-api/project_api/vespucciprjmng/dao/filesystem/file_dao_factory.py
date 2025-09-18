
from project_api.vespucciprjmng.dao.dao_factory import DAOFactory
from project_api.vespucciprjmng.dao.filesystem.json_data_connector import JSONDataConnector
from project_api.vespucciprjmng.dao.filesystem.model_file_dao import ModelFileDAO
from project_api.vespucciprjmng.dao.filesystem.project_file_dao import ProjectFileDAO
from project_api.vespucciprjmng.dao.filesystem.deployment_file_dao import DeploymentFileDAO
from project_api.vespucciprjmng.dao.filesystem.model_file_dao import ModelFileDAO
from project_api.vespucciprjmng.dao.filesystem.training_file_dao import TrainingFileDAO
from project_api.vespucciprjmng.dao.filesystem.data_sufficiency_file_dao import DataSufficiencyFileDAO
from project_api.vespucciprjmng.dao.filesystem.job_file_dao import JobFileDAO
from project_api.vespucciprjmng.dao.filesystem.deployment_applications_file_dao import DeploymentApplicationFileDAO

class FileDAOFactory(DAOFactory):

    def __init__(self, projects_folder_uri: str = None, job_uri: str = None):
        self.__project_data_session_instance    = JSONDataConnector(projects_folder_uri)
        self.__project_dao_instance             = None
        self.__deployment_dao_instance          = None
        self.__deployment_app_dao_instance      = None
        self.__model_dao_instance               = None
        self.__training_dao_instance            = None
        self.__job_job_dao_instance             = None
        self.__data_sufficiency_dao_instance    = None

    def get_project_dao_instance(self) -> ProjectFileDAO:
        if not self.__project_dao_instance:
            self.__project_dao_instance = ProjectFileDAO(self.__project_data_session_instance)
        return self.__project_dao_instance

    def get_deployment_dao_instance(self) -> DeploymentFileDAO:
        if not self.__deployment_dao_instance:
            self.__deployment_dao_instance = DeploymentFileDAO(self.__project_data_session_instance)
        return self.__deployment_dao_instance
    
    def get_deployment_app_dao_instance(self) -> DeploymentApplicationFileDAO:
        if not self.__deployment_app_dao_instance:
            self.__deployment_app_dao_instance = DeploymentApplicationFileDAO(self.__project_data_session_instance)
        return self.__deployment_app_dao_instance

    def get_model_dao_instance(self) -> ModelFileDAO:
        if not self.__model_dao_instance:
            self.__model_dao_instance = ModelFileDAO(self.__project_data_session_instance)
        return self.__model_dao_instance
    
    def get_training_dao_instance(self) -> TrainingFileDAO:
        if not self.__training_dao_instance:
            self.__training_dao_instance = TrainingFileDAO(self.__project_data_session_instance)
        return self.__training_dao_instance
    
    def get_data_sufficiency_dao_instance(self) -> DataSufficiencyFileDAO:
        if not self.__data_sufficiency_dao_instance:
            self.__data_sufficiency_dao_instance = DataSufficiencyFileDAO(self.__project_data_session_instance)
        return self.__data_sufficiency_dao_instance
    
    def get_job_dao_instance(self) -> JobFileDAO:
        if not self.__job_job_dao_instance:
            self.__job_job_dao_instance = JobFileDAO(self.__project_data_session_instance)
        return self.__job_job_dao_instance
    