
class MethodNotImplemented(Exception):
    def __init__(self, method_name:str):
        super("Method \"" + method_name + "\"not implemented !")