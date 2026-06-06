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
    def set_status(self, subject_id:int , new_status:str) -> None:
        pass

    @abstractmethod
    def add_absence(self, subject_id: int, amount: int = 1) -> int:
        pass

    @abstractmethod
    def add_subject(self, data:dict) -> None:
        pass

    @abstractmethod
    def remove_subject(self, subject_id:int) -> None:
        pass

    @abstractmethod
    def ensure_progress_defaults(self) -> None:
        pass

    @abstractmethod
    def update_subject_progress(
        self, subject_id: int, current_activity: int, current_colloquium: int
    ) -> None:
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

    """
    Events
    """

    @abstractmethod
    def get_all_events(self) -> list[dict]:
        pass

    @abstractmethod
    def add_event(self, subject_id: int, event_type: str, title: str, date_time: str) -> None:
        pass

    @abstractmethod
    def remove_event(self, event_id: int) -> None:
        pass

    @abstractmethod
    def get_upcoming_events(self) -> list[dict]:
        pass
