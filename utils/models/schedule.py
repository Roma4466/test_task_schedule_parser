from abc import ABC, abstractmethod
from typing import List

from pandas import DataFrame

from utils.coordinates_getter import get_coordinates_of_column


class Schedule(ABC):
    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: DataFrame):
        self._faculty_name = faculty_name
        self._year_of_studying = year_of_studying
        self._years = years
        self._majors = majors
        # getting column number
        self.schedule_data_frame = schedule_data_frame
        self.day_column = get_coordinates_of_column(schedule_data_frame, ["День"])[1]
        self.time_column = get_coordinates_of_column(schedule_data_frame, ["Час"])[1]
        self.disciple_column = get_coordinates_of_column(schedule_data_frame, ["Дисципліна, викладач"])[1]
        self.group_column = get_coordinates_of_column(schedule_data_frame, ["Група"])[1]
        self.week_column = get_coordinates_of_column(schedule_data_frame, ["Тижні", "Тиждень"])[1]
        self.room_column = get_coordinates_of_column(schedule_data_frame, ["Аудиторія", "Ауд."])[1]

    @abstractmethod
    def parse(self):
        pass
