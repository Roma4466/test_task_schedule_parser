from abc import ABC, abstractmethod


class Schedule(ABC):
    @property
    @abstractmethod
    def is_several_majors(self):
        """is true if in .xlsx file there are more than 1 majors"""
        pass
