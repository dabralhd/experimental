
from enum import Enum


class ResourceKind(Enum):
    PROJECT = "project"
    MODEL   = "model"
    INPUT   = "input"
    LOG     = "log"
    OUTPUT  = "output"
    TEST    = "test"
    EXPERIMENT = "experiment"
    TOOL    = "tool"

class ResourceAlreadyExisting(Exception):
    def __init__(self, uuid: str, name: str, kind: ResourceKind):
        super(kind.value + " resource with IDs \"" + name + "\" \\ \"" + uuid + "\" already exist !")