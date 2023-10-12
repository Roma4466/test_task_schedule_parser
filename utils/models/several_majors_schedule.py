import re
from typing import List

import pandas as pd

from utils.constants import FieldsNames
from utils.formatting.str_formatting import StringFormatter
from utils.models.schedule import Schedule


class SeveralMajorsSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: pd.DataFrame):
        super().__init__(faculty_name, year_of_studying, years, majors, schedule_data_frame)

    def parse_disciple_cell_text_into_map(self, discipline_info):
        discipline_info_series = pd.Series(discipline_info.split(")"))
        discipline = StringFormatter.remove_spaces_from_start_and_end(discipline_info_series.iloc[0].split("(")[0])
        teacher = StringFormatter.remove_spaces_from_start_and_end(discipline_info_series.iloc[-1])

        self.previous_disciple = discipline if len(discipline_info_series) > 1 else self.previous_disciple
        self.major = SeveralMajorsSchedule.extract_speciality_from_abbreviation(discipline_info, self._majors)

        for speciality in self.major:
            specialities_data = self.final_parsed_data[self._faculty_name].setdefault(
                FieldsNames.SPECIALITIES_FIELD_NAME, {})
            major_data = specialities_data.setdefault(speciality, {})
            discipline_data = major_data.setdefault(discipline, {})
            group_data = discipline_data.setdefault(self.group, {})

            start_time_str, end_time_str = self.current_time.split('-')
            start_time_str = start_time_str.replace(".", ":")
            end_time_str = end_time_str.replace(".", ":")
            group_data.update(self.fill_map_information(start_time_str, end_time_str, teacher))

    @staticmethod
    def extract_speciality_from_abbreviation(str_input: str, majors: List[str]):
        result = set()
        abbreviations = pd.Series(re.split(r'[,+]', str_input.split("(")[-1].split(")")[0]))
        abbreviations = abbreviations.str.replace(")", "").str.replace(".", "").str.replace(" ", "").str.lower()

        for speciality in majors:
            if abbreviations.isin([speciality.lower()]).any():
                result.add(speciality)

        return result
