import re
from typing import List

import pandas as pd
from pandas import DataFrame

from utils.constants import SPECIALITIES_FIELD_NAME, LECTION_FIELD_NAME
from utils.formatting.str_formatting import StringFormatter
from utils.formatting.time_parcer import TimeFormatter
from utils.models.schedule import Schedule


class SeveralMajorsSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: DataFrame):
        super().__init__(faculty_name, year_of_studying, years, majors, schedule_data_frame)

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
        if LECTION_FIELD_NAME.lower() in self.group.lower():
            self.group = LECTION_FIELD_NAME
        else:
            self.group = StringFormatter.remove_everything_after_last_digit(self.group)
        self.week = row[self.week_column] if pd.notna(row[self.week_column]) else self.week
        self.week = TimeFormatter.format_datetime_for_json(self.week)
        self.room = row[self.room_column] if pd.notna(row[self.room_column]) else self.room
        # if this cell is empty then
        # there is no need to read further
        if not discipline_info:
            return

        if len(discipline_info.split(")")) < 2:
            # sometimes it parses disciple info in 2 cells
            # in first disciple in second teacher name
            teacher = StringFormatter.remove_spaces_from_start_and_end(discipline_info)
            discipline = StringFormatter.remove_spaces_from_start_and_end(self.previous_disciple)
        else:
            discipline = StringFormatter.remove_spaces_from_start_and_end(discipline_info.split("(")[0])
            self.previous_disciple = discipline
            teacher = StringFormatter.remove_spaces_from_start_and_end(discipline_info.split(")")[1])
            if not teacher.replace(" ", ""):
                return
            self.major = SeveralMajorsSchedule.extract_speciality_from_abbreviation(discipline_info, self._majors)

        for speciality in self.major:
            if discipline not in self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][speciality]:
                self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][speciality][discipline] = {}
            if self.group not in self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][speciality][discipline]:
                self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][speciality][discipline][self.group] = {}

        start_time_str, end_time_str = self.current_time.split('-')
        start_time_str = start_time_str.replace(".", ":")
        end_time_str = end_time_str.replace(".", ":")
        for speciality in self.major:
            self.final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][speciality][discipline][self.group] = {
                "час початку": start_time_str,
                "час кінця": end_time_str,
                "тижні": self.week,
                "аудиторія": self.room,
                "день тижня": self.current_day,
                "викладач": teacher
            }

    @staticmethod
    def extract_speciality_from_abbreviation(str_input: str, majors: List[str]):
        result = set()
        before_and_after_opening_parenthesis = str_input.split("(")
        filtered_list = [i for i in before_and_after_opening_parenthesis if ")" in i]
        for string in filtered_list:
            split = string.split(")")[0]
            # split by "," or "+"
            split = re.split(r'[,+]', split)
            for abbreviation in split:
                without_non_letters = abbreviation.replace(")", "").replace(".", "").replace(" ", "")
                for speciality in majors:
                    if without_non_letters in speciality.lower():
                        result.add(speciality)
        return result
