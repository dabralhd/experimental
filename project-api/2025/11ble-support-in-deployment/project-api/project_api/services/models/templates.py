from enum import Enum


class TemplateType(Enum):
    EXPERIMENT_MODEL_DEV_FILE = "experiment_model_dev_file"


class TemplateDescriptor():

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def type(self) -> TemplateType:
        return self._type

    @type.setter
    def type(self, type: TemplateType):
        self._type = type

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    @property
    def config_path(self) -> str:
        return self._config_path

    @config_path.setter
    def config_path(self, config_path: str):
        self._config_path = config_path

    @property
    def schema_config_path(self) -> str:
        return self._config_path

    @config_path.setter
    def schema_config_path(self, schema_config_path: str):
        self._schema_config_path = schema_config_path

    def __init__(self, name: str, type: TemplateType, path: str, config_path: str, schema_config_path: str):
        self._name = name
        self._type = type
        self._path = path
        self._config_path = config_path
        self._schema_config_path = schema_config_path