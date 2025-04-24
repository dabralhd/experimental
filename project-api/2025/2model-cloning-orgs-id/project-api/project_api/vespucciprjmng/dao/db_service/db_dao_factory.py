
from project_api.vespucciprjmng.dao.dao_factory import DAOFactory
from project_api.vespucciprjmng.dao.db_service.experiment_db_dao import (
    ExperimentDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.input_db_dao import InputDBDAO
from project_api.vespucciprjmng.dao.db_service.input_tool_db_dao import (
    InputToolDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.log_db_dao import LogDBDAO
from project_api.vespucciprjmng.dao.db_service.model_db_dao import ModelDBDAO
from project_api.vespucciprjmng.dao.db_service.output_db_dao import OutputDBDAO
from project_api.vespucciprjmng.dao.db_service.output_tool_db_dao import (
    OutputToolDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.project_db_dao import (
    ProjectDBDAO,
)
from project_api.vespucciprjmng.dao.db_service.test_db_dao import TestDBDAO


class DBDAOFactory(DAOFactory):

    def __init__(self, user_id: str, service_uri: str):
        self.__user_id                  = user_id
        self.__service_uri              = service_uri
        self.__project_dao_instance     = None
        self.__model_dao_instance       = None
        self.__input_dao_instance       = None
        self.__output_dao_instance      = None
        self.__experiment_dao_instance  = None
        self.__log_dao_instance         = None
        self.__test_dao_instance        = None
        self.__input_tool_dao_instance  = None
        self.__output_tool_dao_instance = None

    def get_project_dao_instance(self) -> ProjectDBDAO:
        if not self.__project_dao_instance:
            self.__project_dao_instance = ProjectDBDAO(self.__user_id, self.__service_uri)
        return self.__project_dao_instance

    def get_model_dao_instance(self) -> ModelDBDAO:
        if not self.__model_dao_instance:
            self.__model_dao_instance = ModelDBDAO(self.__service_uri)
        return self.__model_dao_instance

    def get_input_dao_instance(self) -> InputDBDAO:
        if not self.__input_dao_instance:
            self.__input_dao_instance = InputDBDAO(self.__service_uri)
        return self.__input_dao_instance

    def get_output_dao_instance(self) -> OutputDBDAO:
        if not self.__output_dao_instance:
            self.__output_dao_instance = OutputDBDAO(self.__service_uri)
        return self.__output_dao_instance

    def get_experiment_dao_instance(self) -> ExperimentDBDAO:
        if not self.__experiment_dao_instance:
            self.__experiment_dao_instance = ExperimentDBDAO(self.__service_uri)
        return self.__experiment_dao_instance

    def get_log_dao_instance(self) -> LogDBDAO:
        if not self.__log_dao_instance:
            self.__log_dao_instance = LogDBDAO(self.__service_uri)
        return self.__log_dao_instance

    def get_test_dao_instance(self) -> TestDBDAO:
        if not self.__test_dao_instance:
            self.__test_dao_instance = TestDBDAO(self.__service_uri)
        return self.__test_dao_instance

    def get_input_tool_dao_instance(self) -> InputToolDBDAO:
        if not self.__input_tool_dao_instance:
            self.__input_tool_dao_instance = InputToolDBDAO(self.__service_uri)
        return self.__input_tool_dao_instance

    def get_output_tool_dao_instance(self) -> OutputToolDBDAO:
        if not self.__output_tool_dao_instance:
            self.__output_tool_dao_instance = OutputToolDBDAO(self.__service_uri)
        return self.__output_tool_dao_instance