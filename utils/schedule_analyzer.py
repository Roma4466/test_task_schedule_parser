import json
import os

from pandas import DataFrame

from utils.constants import SPECIALITY_FIELD_NAME, FACULTY_FIELD_NAME
from utils.datetime_serializer import datetime_serializer
from utils.formatting.str_formatting import StringFormatter
from utils.models.several_majors_schedule import SeveralMajorsSchedule
from utils.models.single_major_schedule import SingleMajorSchedule


class ScheduleParser:
    @staticmethod
    def parse_schedule(schedule_data_frame: DataFrame, name: str):
        """function that will parse schedule from .xlsx format into .json file"""
        schedule = ScheduleParser.fill_specialities(schedule_data_frame)
        final_parsed_data = schedule.parse()
        json_str = json.dumps(final_parsed_data, indent=4, default=datetime_serializer, ensure_ascii=False)
        # Define the directory path
        output_dir = 'output'

        # Check if the directory exists, and if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'output/{name}.json', 'w') as f:
            f.write(json_str)

    @staticmethod
    def fill_specialities(schedule_data_frame: DataFrame):
        """
        creates either instance of SingleMajorSchedule or SeveralMajorsSchedule class
        """
        faculty = ""
        majors = []
        year_of_study = 0
        started_year = 0
        is_read_specialities = False
        is_read_faculty = False
        digits = ""

        # Loop through each row in the DataFrame
        for index, row in schedule_data_frame.iterrows():
            for col_index in range(min(7, schedule_data_frame.shape[1])):
                text = str(row.iloc[col_index])
                current_string = ""
                for symbol in text:
                    if symbol.isdigit():
                        digits += symbol
                    else:
                        if len(digits) == 4:
                            started_year = int(digits)
                        digits = ""

                    if current_string == SPECIALITY_FIELD_NAME:
                        current_string = ""
                        is_read_specialities = True
                    elif current_string == FACULTY_FIELD_NAME:
                        is_read_faculty = True
                    current_string += symbol

                if is_read_faculty:
                    faculty = current_string
                    is_read_faculty = False
                if is_read_specialities:
                    for i in current_string:
                        if i.isdigit():
                            year_of_study = int(i)
                    specialities_tmp = current_string.split("», ")
                    for speciality in specialities_tmp:
                        speciality = StringFormatter.remove_non_letters(speciality)
                        majors.append(speciality)
                    is_read_specialities = False

        if len(majors) > 1:
            return SeveralMajorsSchedule(faculty, year_of_study, [started_year, started_year + 1], majors,
                                         schedule_data_frame)
        return SingleMajorSchedule(faculty, year_of_study, [started_year, started_year + 1], majors,
                                   schedule_data_frame)
