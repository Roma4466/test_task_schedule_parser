from typing import List


class WeekParser:
    @staticmethod
    def parse_week(week_str: str) -> List[int]:
        weeks = []
        for part in week_str.replace('.', ',').split(','):
            start, end = map(int, part.split("-")) if '-' in part else (int(part), int(part))
            weeks.extend(range(start, end + 1))
        return weeks
