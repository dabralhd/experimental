from __future__ import annotations

import json
import os

from project_api.services.models.tools import ToolDescriptor
from project_api.vespucciprjmng.repository.db_service.project_db_repo import (
    ProjectDBRepo,
)
from project_api.vespucciprjmng.repository.filesystem.project_file_repo import (
    ProjectFileRepo,
)

DB_SERVICE_HOST = os.getenv('DB_SERVICE_HOST', 'vespucci_ai_projects_db_service')
DB_SERVICE_PORT = os.getenv('DB_SERVICE_PORT', '6060')

VESPUCCI_ENVIRONMENT = os.getenv('VESPUCCI_ENVIRONMENT', "dev")
FLASK_ENV = os.getenv('FLASK_ENV')
KUBERNETES_SERVICE_PORT_HTTPS = os.getenv('KUBERNETES_SERVICE_PORT_HTTPS', None)
CONTAINER_NAME = os.getenv('CONTAINER_NAME', "main_rest_api")
CONTAINER_ID = os.getenv('CONTAINER_ID', "N/A")
PORT = int(os.getenv('REST_API_PORT', 9090))

FOLDER_APP_FULL_PATH = os.path.dirname(os.path.realpath(__file__))

OIDC_CLIENT_SECRETS_PATH = os.getenv('OIDC_CLIENT_SECRETS_PATH', os.path.join(FOLDER_APP_FULL_PATH, 'oidc_provider_test', 'client_secrets.json'))
TRACKING_API_PATH = os.getenv('TRACKING_API_PATH', os.path.join(FOLDER_APP_FULL_PATH, 'tracking_api', 'tracking_api.json'))
STORAGE_PATH = os.getenv('STORAGE_PATH', os.path.join(FOLDER_APP_FULL_PATH, '../test'))

USER_WORKSPACE_SUBPATH = os.getenv('USER_WORKSPACE_SUBPATH', '')
USER_PROJECTS_SUBPATH = os.path.join(USER_WORKSPACE_SUBPATH , 'projects')

JOBS_FOLDER_PATH = STORAGE_PATH

ARTIFACTS_FOLDER = os.getenv('ARTIFACTS_FOLDER', os.path.join("/", "data", "artifacts"))
ASSETS_FOLDER_PATH = os.getenv('ASSETS_FOLDER', os.path.join(ARTIFACTS_FOLDER, ".assets"))
GET_STARTED_PROJECTS_PATH = os.path.join(ARTIFACTS_FOLDER , "get-started-projects")
EXPERIMENT_TEMPLATES_PATH = os.path.join(ASSETS_FOLDER_PATH, "templates", "models", "experiments", "jupyter_notebook")

EXTRACT_THREAD_POOL_MAX_SIZE = int(os.getenv('EXTRACT_THREAD_POOL_MAX_SIZE', '512'))

JOBCONTROL_API_BASE_PATH = "/svc/jobcontrol/v1alpha1"
JOBCONTROL_API_BASE_URL = os.getenv(
    "JOBCONTROL_API_BASE_URL",
    "http://jobcontrol-api:5002"
) + JOBCONTROL_API_BASE_PATH

CONVERSION_JOB_TEMPLATE_ID = "01HH1K7BF29ENCV95XTDVSAN61"
CONVERSION_JOB_MAX_CONSECUTIVE_POLLING_ERRORS = os.getenv(
    "CONVERSION_JOB_MAX_CONSECUTIVE_POLLING_ERRORS",
    "3"
)

class GlobalObjects():
    __instance = None

    @property
    def flask_app(self):
        """Gets global Flask application.


        :return: The Flask application instance.
        """
        return self._flask_app

    @flask_app.setter
    def flask_app(self, flask_app):
        """Global Flask application


        :param flask_app: Flask application instance.
        """

        self._flask_app = flask_app

    @property
    def tools(self):
        """Tools metadata.


        :return: Tool metadata list.
        """
        tools = []
        tools_file_path = os.path.join(
            ASSETS_FOLDER_PATH, "rules", "tools.json")
        with open(tools_file_path, "r") as file:
            raw_tools = json.load(file)
            for raw_tool in raw_tools["tools"]:
                try:
                    tools.append(ToolDescriptor.deserialize(raw_tool=raw_tool))
                except Exception as e:
                    print(e)
        return tools

    def __init__(self) -> None:
        pass

    @staticmethod
    def getInstance() -> GlobalObjects:
        if not GlobalObjects.__instance:
            GlobalObjects.__instance = GlobalObjects()
        return GlobalObjects.__instance

    def getDBProjectRepo(self, user_id: str) -> ProjectDBRepo:
        project_repo = ProjectDBRepo(user_id=user_id, service_uri="http://"+DB_SERVICE_HOST+":"+DB_SERVICE_PORT)
        return project_repo
    
    def getFSProjectRepo(self, user_id: str) -> ProjectFileRepo:
        user_project_projects_path_folder = os.path.join(STORAGE_PATH, user_id, USER_PROJECTS_SUBPATH)
        # Check if the path exists
        if not os.path.exists(user_project_projects_path_folder):
            # Create the path
            os.makedirs(user_project_projects_path_folder)
        project_repo = ProjectFileRepo(user_project_projects_path_folder)
        return project_repo

    def getFSUserWorkspaceFolder(self, user_id: str) -> str:
        return os.path.join(STORAGE_PATH, user_id, USER_PROJECTS_SUBPATH)
    
    def getPublicProjectsPath(self):
        return GET_STARTED_PROJECTS_PATH