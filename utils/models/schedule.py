from abc import ABC, abstractmethod
from typing import List

import pandas as pd
from pandas import DataFrame

from utils.constants import SPECIALITIES_FIELD_NAME, LECTURE_FIELD_NAME
from utils.coordinates_getter import get_coordinates_of_column
from utils.formatting.str_formatting import StringFormatter
from utils.formatting.time_parcer import TimeFormatter
from utils.formatting.weekd_parser import WeekParser


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
        self.weeks_list = ""
        self.major = ""

        # getting row number where schedule starts
        self.coordinates = get_coordinates_of_column(self.schedule_data_frame, "День")[0]

        for index, row in self.schedule_data_frame.iterrows():
            self.parse_row(index, row)
        return self.final_parsed_data

    def parse_row(self, index, row):
        # before coordinates row there is basic
        # info about faculty etc.
        # there is no schedule there, so I skip it
        if index < self.coordinates + 1:
            return

        if pd.notna(row[self.day_column]):
            self.current_day = row[self.day_column]
        self.current_time = row[self.time_column] if pd.notna(row[self.time_column]) else self.current_time
        discipline_info = row[self.disciple_column] if pd.notna(row[self.disciple_column]) else ""

        self.group = str(row[self.group_column] if pd.notna(row[self.group_column]) else self.group)
        if LECTURE_FIELD_NAME.lower() in self.group.lower():
            self.group = LECTURE_FIELD_NAME
        else:
            self.group = StringFormatter.remove_everything_after_last_digit(self.group)

        if pd.notna(row[self.week_column]):
            week_str = row[self.week_column]
            week_str = str(TimeFormatter.format_datetime_for_json(week_str))
            self.weeks_list = WeekParser.parse_week(week_str)

        self.room = row[self.room_column] if pd.notna(row[self.room_column]) else self.room
        # if this cell is empty then
        # there is no need to read further
        if not discipline_info:
            return
        self.parse_disciple_cell_text_into_map(discipline_info)

    @abstractmethod
    def parse_disciple_cell_text_into_map(self, discipline_info):
        pass
