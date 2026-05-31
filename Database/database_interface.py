from abc import ABC, abstractmethod

class IAppRepository(ABC):

    """
    Settings
    """

    @abstractmethod
    def set_language(self,lang) -> None:
        pass

    
    @abstractmethod
    def get_language(self,lang) -> str:
        pass

    """
    Subjects
    """

    @abstractmethod
    def get_all_subjects(self) -> list[dict]:
        pass

    @abstractmethod
    def add_absence(self, subject_id: int, amount: int = 1):
        pass

    @abstractmethod
    def add_subject(self, data:dict) -> None:
        pass

    @abstractmethod
    def remove_subject(self, subject_id:int) -> None:
        pass

    """
    Notes
    """

    @abstractmethod
    def get_daily_note(self, subject_id:int , date:str) -> dict:
        pass

    @abstractmethod
    def set_daily_note(self, subject_id:int , date:str, content:str) -> None:
        pass
