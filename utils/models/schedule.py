from abc import ABC, abstractmethod
from typing import List

from pandas import DataFrame

from utils.constants import SPECIALITIES_FIELD_NAME
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

    def parse(self):
        # Initialize the final data structure to hold the parsed information
        self.final_parsed_data = {
            self._faculty_name: {
                SPECIALITIES_FIELD_NAME: {},
                "Рік навчання": self._year_of_studying,
                "Роки навчального року": [self._years[0], self._years[1]],
            }
        }
        for major in self._majors:
            self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][major] = {}
        # because of if there is time in 2 cels
        # python reads it like it is only in one cell,
        # so I have save last time
        self.current_time = ""
        self.current_day = ""
        self.previous_disciple = ""
        self.group = ""
        self.room = ""
        self.week = ""
        self.major = ""


        # getting row number where schedule starts
        self.coordinates = get_coordinates_of_column(self.schedule_data_frame, "День")[0]

        for index, row in self.schedule_data_frame.iterrows():
            self.parse_row(index, row)
        return self.final_parsed_data

    @abstractmethod
    def parse_row(self, index, row):
        pass
