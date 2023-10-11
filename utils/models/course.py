from datetime import datetime
from typing import List

from utils.models.day_of_week import DayOfWeek


class Course:
    def __init__(self,
                 group: str,
                 start_time: datetime,
                 end_time: datetime,
                 weeks: List[int],
                 room: str,
                 day_of_week: DayOfWeek,
                 teacher: str):
        self._group = group
        self._start_time = start_time
        self._end_time = end_time
        self._weeks = weeks
        self._room = room
        self._day_of_week = day_of_week
        self._teacher = teacher
