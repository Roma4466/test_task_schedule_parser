from typing import List

from utils.models.course import Course


class Major:
    def __init__(self, courses: List[Course]):
        self._courses = courses
