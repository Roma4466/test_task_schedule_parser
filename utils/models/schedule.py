from abc import ABC, abstractmethod

from pandas import DataFrame

from utils.constants import SPECIALITY_FIELD_NAME, FACULTY_FIELD_NAME
from utils.formatting.str_formatting import StringFormatter
from utils.models.several_majors_schedule import SeveralMajorsSchedule


class Schedule(ABC):
    @property
    @abstractmethod
    def faculty_name(self):
        """
        start year and end year of education period
        """
        pass

    @property
    @abstractmethod
    def majors(self):
        """list of names of majors"""
        pass

    @property
    @abstractmethod
    def year_of_studying(self):
        pass

    @property
    @abstractmethod
    def years(self):
        """
        start year and end year of education period
        """
        pass

    @staticmethod
    def fill_specialities(df: DataFrame):
        faculty = ""
        majors = []
        year_of_study = 0
        started_year = 0
        is_read_specialities = False
        is_read_faculty = False
        digits = ""

        # Loop through each row in the DataFrame
        for index, row in df.iterrows():
            for col_index in range(min(7, df.shape[1])):
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
            return SeveralMajorsSchedule(faculty, year_of_study, [started_year, started_year + 1], majors)

        return faculty, majors, year_of_study, started_year
