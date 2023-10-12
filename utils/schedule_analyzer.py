import json
import os

import pandas as pd

from utils.constants import FieldsNames
from utils.datetime_serializer import datetime_serializer
from utils.formatting.str_formatting import StringFormatter
from utils.models.several_majors_schedule import SeveralMajorsSchedule
from utils.models.single_major_schedule import SingleMajorSchedule


class ScheduleParser:
    @staticmethod
    def parse_schedule(schedule_data_frame: pd.DataFrame, name: str):
        schedule = ScheduleParser.fill_specialities(schedule_data_frame)
        final_parsed_data = schedule.parse()
        json_str = json.dumps(final_parsed_data, indent=4, default=datetime_serializer, ensure_ascii=False)

        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'output/{name}.json', 'w') as f:
            f.write(json_str)

    @staticmethod
    def fill_specialities(schedule_data_frame: pd.DataFrame):
        faculty = ""
        majors = []
        year_of_study = 0
        started_year = 0

        # Use Pandas to find rows containing speciality and faculty information
        speciality_row = schedule_data_frame[
            schedule_data_frame.apply(lambda row: row.astype(str).str.contains(FieldsNames.SPECIALITY_FIELD_NAME).any(),
                                      axis=1)]
        faculty_row = schedule_data_frame[
            schedule_data_frame.apply(lambda row: row.astype(str).str.contains(FieldsNames.FACULTY_FIELD_NAME).any(),
                                      axis=1)]

        if not speciality_row.empty:
            speciality_info = speciality_row.iloc[0].dropna().astype(str)
            year_of_study = int(''.join(filter(str.isdigit, speciality_info.iloc[0])))
            majors = [StringFormatter.remove_non_letters(item) for item in speciality_info]

        if not faculty_row.empty:
            faculty_info = faculty_row.iloc[0].dropna().astype(str)
            faculty = faculty_info.iloc[0]
            digits = ''.join(filter(str.isdigit, faculty_info.iloc[-1]))
            started_year = int(digits) if digits else 0  # Default to 0 if no digits are found

        if len(majors) > 1:
            return SeveralMajorsSchedule(faculty, year_of_study, [started_year, started_year + 1], majors,
                                         schedule_data_frame)
        else:
            return SingleMajorSchedule(faculty, year_of_study, [started_year, started_year + 1], majors,
                                       schedule_data_frame)
