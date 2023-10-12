import re
from typing import List

from pandas import DataFrame

from utils.constants import FieldsNames
from utils.formatting.str_formatting import StringFormatter
from utils.models.schedule import Schedule


class SeveralMajorsSchedule(Schedule):

    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str],
                 schedule_data_frame: DataFrame):
        super().__init__(faculty_name, year_of_studying, years, majors, schedule_data_frame)

    def parse_disciple_cell_text_into_map(self, discipline_info):
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
            if discipline not in self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][speciality]:
                self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][speciality][discipline] = {}
            if self.group not in self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][speciality][
                discipline]:
                self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][speciality][discipline][
                    self.group] = {}

        start_time_str, end_time_str = self.current_time.split('-')
        start_time_str = start_time_str.replace(".", ":")
        end_time_str = end_time_str.replace(".", ":")
        for speciality in self.major:
            self.final_parsed_data[self._faculty_name][FieldsNames.SPECIALITIES_FIELD_NAME][speciality][discipline][
                self.group] = self.fill_map_information(start_time_str, end_time_str, teacher)

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
