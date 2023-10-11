from typing import List

from utils.models.schedule import Schedule


class SingleMajorSchedule(Schedule):
    def __init__(self, faculty_name: str, year_of_studying: int, years: List[int], majors: List[str]):
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
