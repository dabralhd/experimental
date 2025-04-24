
from enum import Enum


class ResourceKind(Enum):
    PROJECT = "project"
    MODEL   = "model"
    EXPERIMENT = "experiment"
    TRAINING = "training"
    DEPLOYMENT = "deployment"

class ResourceAlreadyExisting(Exception):
    def __init__(self, uuid: str, name: str, kind: ResourceKind):
        message = f"{kind.value} resource with IDs \"{name}\" \\ \"{uuid}\" already exists!"
        super().__init__(message)