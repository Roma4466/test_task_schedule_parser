from abc import ABC, abstractmethod
from typing import List

import pandas as pd
from pandas import DataFrame, Series

from utils.constants import FieldsNames
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
        self.schedule_data_frame = schedule_data_frame
        self.day_column = get_coordinates_of_column(schedule_data_frame, [FieldsNames.DAY_FIELD_NAMES])[1]
        self.time_column = get_coordinates_of_column(schedule_data_frame, [FieldsNames.TIME_FIELD_NAME])[1]
        self.disciple_column = get_coordinates_of_column(schedule_data_frame, [FieldsNames.DISCIPLE_INFO_FIELD_NAME])[1]
        self.group_column = get_coordinates_of_column(schedule_data_frame, [FieldsNames.GROUP_FIELD_NAME])[1]
        self.week_column = get_coordinates_of_column(schedule_data_frame, ["Тижні", "Тиждень"])[1]
        self.room_column = get_coordinates_of_column(schedule_data_frame, ["Аудиторія", "Ауд."])[1]

    def parse(self):
        self.final_parsed_data = {
            self._faculty_name: {
                FieldsNames.SPECIALITIES_FIELD_NAME: {},
                "Рік навчання": self._year_of_studying,
                "Роки навчального року": [self._years[0], self._years[1]],
            }
        }
        for major in self._majors:
            self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][major] = {}

        self.current_time = ""
        self.current_day = ""
        self.previous_disciple = ""
        self.group = ""
        self.room = ""
        self.weeks_list = ""
        self.major = ""

        self.coordinates = get_coordinates_of_column(self.schedule_data_frame, [FieldsNames.DAY_FIELD_NAMES])[0]

        # Use Pandas to filter rows where schedule starts and apply parse_row function
        filtered_df = self.schedule_data_frame.loc[self.coordinates + 1:]
        filtered_df.apply(self.parse_row, axis=1)

        return self.final_parsed_data

    def parse_row(self, row: Series):
        self.current_day = row.at[self.day_column] if pd.notna(row.at[self.day_column]) else self.current_day
        self.current_time = row.at[self.time_column] if pd.notna(row.at[self.time_column]) else self.current_time
        discipline_info = row.at[self.disciple_column] if pd.notna(row.at[self.disciple_column]) else ""

        self.group = str(row[self.group_column] if pd.notna(row[self.group_column]) else self.group)
        if FieldsNames.LECTURE_FIELD_NAME.lower() in self.group.lower():
            self.group = FieldsNames.LECTURE_FIELD_NAME
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

    def fill_map_information(self, start_time_str: str, end_time_str: str, teacher: str):
        return {
            FieldsNames.TIME_START: start_time_str,
            FieldsNames.TIME_END: end_time_str,
            FieldsNames.WEEKS: self.weeks_list,
            FieldsNames.ROOM: self.room,
            FieldsNames.DAY_FIELD_NAMES: self.current_day,
            FieldsNames.TEACHER: teacher
        }

    @abstractmethod
    def parse_disciple_cell_text_into_map(self, discipline_info):
        pass
