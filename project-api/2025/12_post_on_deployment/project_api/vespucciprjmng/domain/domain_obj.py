

class DomainOBJ():
    
    @property
    def project_ref(self) -> str:
        return self.__project_ref

    @project_ref.setter 
    def project_ref(self, value: str):
        self.__project_ref = value