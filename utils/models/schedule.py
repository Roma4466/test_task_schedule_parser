from abc import ABC, abstractmethod

from pandas import DataFrame

from utils.constants import SPECIALITIES_FIELD_NAME
from utils.coordinates_getter import get_coordinates_of_column
from utils.formatting.str_formatting import StringFormatter


class Schedule(ABC):
    def __init__(self, schedule_data_frame: DataFrame):
        # getting column number
        self.schedule_data_frame = schedule_data_frame
        self.day_column = get_coordinates_of_column(schedule_data_frame, ["День"])[1]
        self.time_column = get_coordinates_of_column(schedule_data_frame, ["Час"])[1]
        self.disciple_column = get_coordinates_of_column(schedule_data_frame, ["Дисципліна, викладач"])[1]
        self.group_column = get_coordinates_of_column(schedule_data_frame, ["Група"])[1]
        self.week_column = get_coordinates_of_column(schedule_data_frame, ["Тижні", "Тиждень"])[1]
        self.room_column = get_coordinates_of_column(schedule_data_frame, ["Аудиторія", "Ауд."])[1]

    @property
    @abstractmethod
    def faculty_name(self):
        """
        start year and end year of education period
        """
        pass

    @property
    @abstractmethod
    def majors(self):
        """list of names of majors"""
        pass

    @property
    @abstractmethod
    def year_of_studying(self):
        pass

    @property
    @abstractmethod
    def years(self):
        """
        start year and end year of education period
        """
        pass

    @abstractmethod
    def parse(self):
        pass