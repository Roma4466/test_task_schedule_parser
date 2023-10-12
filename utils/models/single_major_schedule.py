from typing import List

import pandas as pd

from utils.constants import FieldsNames
from utils.formatting.str_formatting import StringFormatter
from utils.models.schedule import Schedule


class SingleMajorSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: pd.DataFrame):
        super().__init__(faculty_name, year_of_studying, years, majors, schedule_data_frame)

    def parse_disciple_cell_text_into_map(self, discipline_info):
        # Split and clean up the discipline and teacher information
        discipline_info_series = pd.Series(discipline_info.split(", "))
        discipline_info_series = discipline_info_series.apply(StringFormatter.remove_spaces_from_start_and_end)

        discipline = discipline_info_series.iloc[0]
        teacher = discipline_info_series.iloc[1] if len(discipline_info_series) > 1 else "???"

        # Initialize the nested dictionaries if they don't exist
        faculty_data = self.final_parsed_data.setdefault(self._faculty_name, {})
        specialities_data = faculty_data.setdefault(FieldsNames.SPECIALITIES_FIELD_NAME, {})
        major_data = specialities_data.setdefault(self._majors[0], {})
        discipline_data = major_data.setdefault(discipline, {})
        group_data = discipline_data.setdefault(self.group, {})

        # Fill in the information
        start_time_str, end_time_str = self.current_time.split('-')
        group_data.update(self.fill_map_information(start_time_str, end_time_str, teacher))
