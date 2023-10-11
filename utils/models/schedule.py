from abc import ABC, abstractmethod


class Schedule(ABC):
    @property
    @abstractmethod
    def majors(self):
        """list of names of majors"""
        pass

