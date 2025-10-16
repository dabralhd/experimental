class DBServiceSpecs():

    @staticmethod
    def getProjectsPath() -> str:
        return "/projects"

    @staticmethod
    def getProjectPath(project_uuid: str) -> str:
        return "/projects/" + project_uuid

    @staticmethod
    def getModelsPath(project_uuid: str) -> str:
        return "/projects/" + project_uuid + "/models"

    @staticmethod
    def getModelPath(project_uuid: str, model_uuid: str) -> str:
        return "/projects/" + project_uuid + "/models/" + model_uuid

    @staticmethod
    def getInputsPath(project_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs"

    @staticmethod
    def getInputPath(project_uuid: str, input_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs/" + input_uuid

    @staticmethod
    def getOutputsPath(project_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs"

    @staticmethod
    def getOutputPath(project_uuid: str, output_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs/" + output_uuid

    @staticmethod
    def getLogsPath(project_uuid: str, input_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs/" + input_uuid + "/logs"

    @staticmethod
    def getLogPath(project_uuid: str, input_uuid: str, log_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs/" + input_uuid + "/logs/" + log_uuid

    @staticmethod
    def getInputToolsPath(project_uuid: str, input_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs/" + input_uuid + "/tools"

    @staticmethod
    def getInputToolPath(project_uuid: str, input_uuid: str, tool_uuid: str) -> str:
        return "/projects/" + project_uuid + "/inputs/" + input_uuid + "/tools/" + tool_uuid

    @staticmethod
    def getOutputToolsPath(project_uuid: str, output_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs/" + output_uuid + "/tools"

    @staticmethod
    def getOutputToolPath(project_uuid: str, output_uuid: str, tool_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs/" + output_uuid + "/tools/" + tool_uuid

    @staticmethod
    def getExperimentsPath(project_uuid: str, model_uuid: str) -> str:
        return "/projects/" + project_uuid + "/models/" + model_uuid + "/experiments"

    @staticmethod
    def getExperimentPath(project_uuid: str, model_uuid: str, experiment_uuid: str) -> str:
        return "/projects/" + project_uuid + "/models/" + model_uuid + "/experiments/" + experiment_uuid

    @staticmethod
    def getTestsPath(project_uuid: str, output_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs/" + output_uuid + "/tests"

    @staticmethod
    def getTestPath(project_uuid: str, output_uuid: str, test_uuid: str) -> str:
        return "/projects/" + project_uuid + "/outputs/" + output_uuid + "/tests/" + test_uuid
