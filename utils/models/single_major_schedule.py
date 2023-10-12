from typing import List

from pandas import DataFrame

from utils.constants import FieldsNames
from utils.formatting.str_formatting import StringFormatter
from utils.models.schedule import Schedule


class SingleMajorSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: DataFrame):
        super().__init__(faculty_name, year_of_studying, years, majors, schedule_data_frame)

    def parse_disciple_cell_text_into_map(self, discipline_info):
        discipline = discipline_info.split(", ")[0].strip()
        teacher = discipline_info.split(", ")[1].strip() if len(
            discipline_info.split(", ")) > 1 else "???"
        # now we know faculty, specialty, discipline
        # then let`s initialize field in result file
        if discipline not in self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][
            self._majors[0]]:
            self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][self._majors[0]][
                discipline] = {}

        if self.group not in \
                self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][self._majors[0]][
                    discipline]:
            self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][self._majors[0]][
                discipline][
                self.group] = {}

        start_time_str, end_time_str = self.current_time.split('-')

        self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][self._majors[0]][discipline][
            self.group] = self.fill_map_information(start_time_str, end_time_str, teacher)
