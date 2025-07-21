import typing

# singleton creation helper decorator
def singleton(cls):
    """
    Decorator that makes a class a singleton.
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Endpoint:
    def __init__(self, name: str, url: str = None, method: str = None, headers: typing.Dict[str, str] = None, body: typing.Dict[str, str] = None):
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"{self.name} - {self.url} - {self.method} - {self.headers} - {self.body}"