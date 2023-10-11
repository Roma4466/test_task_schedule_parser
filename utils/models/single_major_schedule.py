from typing import List

import pandas as pd
from pandas import DataFrame

from utils.constants import SPECIALITIES_FIELD_NAME, LECTION_FIELD_NAME
from utils.coordinates_getter import get_coordinates_of_column
from utils.formatting.str_formatting import StringFormatter
from utils.formatting.time_parcer import TimeFormatter
from utils.models.schedule import Schedule


class SingleMajorSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: DataFrame):
        super().__init__(schedule_data_frame)
        self._faculty_name = faculty_name
        self._year_of_studying = year_of_studying
        self._years = years
        self._majors = majors

    @property
    def faculty_name(self):
        return self._faculty_name

    @property
    def year_of_studying(self):
        return self._year_of_studying

    @property
    def years(self):
        return self._year_of_studying

    @property
    def majors(self):
        return self.majors

    def parse(self):
        # Initialize the final data structure to hold the parsed information
        final_parsed_data = {
            self._faculty_name: {
                SPECIALITIES_FIELD_NAME: {},
                "Рік навчання": self._year_of_studying,
                "Роки навчального року": [self._years[0], self._years[1]],
            }
        }
        for current_specialities in self.majors:
            final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][current_specialities] = {}
        # because of if there is time in 2 cels
        # python reads it like it is only in one cell
        # so I have save last time
        current_time = ""
        current_day = ""
        group = ""
        room = ""
        week = ""

        # getting row number where schedule starts
        coordinates = get_coordinates_of_column(self.schedule_data_frame, "День")[0]

        for index, row in self.schedule_data_frame.iterrows():
            # before coordinates row there is basic
            # info about faculty etc.
            # there is no schedule there so I skip it
            if index < coordinates + 1:
                continue

            if pd.notna(row[self.day_column]):
                current_day = row[self.day_column]
            current_time = row[self.time_column] if pd.notna(row[self.time_column]) else current_time
            discipline_info = row[self.disciple_column] if pd.notna(row[self.disciple_column]) else ""

            group = str(row[self.group_column] if pd.notna(row[self.group_column]) else group)
            if LECTION_FIELD_NAME.lower() in group.lower():
                group = LECTION_FIELD_NAME
            else:
                for i in group:
                    if i.isdigit():
                        group = int(i)
                        break
            week = row[self.week_column] if pd.notna(row[self.week_column]) else week
            week = TimeFormatter.format_datetime_for_json(week)
            room = row[self.room_column] if pd.notna(row[self.room_column]) else room
            # if this cell is empty then
            # there is no need to read further
            if not discipline_info:
                continue

            discipline = StringFormatter.remove_spaces_from_start_and_end(discipline_info.split(", ")[0])
            teacher = StringFormatter.remove_spaces_from_start_and_end(discipline_info.split(", ")[1]) if len(
                discipline_info.split(", ")) > 1 else "???"
            # now we know faculty, specialty, discipline
            # then let`s initialize field in result file
            if discipline not in final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][self._majors[0]]:
                final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][self._majors[0]][discipline] = {}

            if group not in final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][self._majors[0]][discipline]:
                final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][self._majors[0]][discipline][group] = {}

            start_time_str, end_time_str = current_time.split('-')

            final_parsed_data[self._faculty_name][SPECIALITIES_FIELD_NAME][self._majors[0]][discipline][group] = {
                "час початку": start_time_str,
                "час кінця": end_time_str,
                "тижні": week,
                "аудиторія": room,
                "день тижня": current_day,
                "викладач": teacher
            }
        return final_parsed_data
