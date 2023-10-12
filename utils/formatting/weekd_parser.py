from typing import List


class WeekParser:
    @staticmethod
    def parse_week(week_str: str) -> List[int]:
        """
        Parsing from format "1,2,4-11" into [1,2,4,5,6,7,8,9,10,11]
        """
        weeks = []
        for part_by_dot in week_str.split("."):
            for part in part_by_dot.split(","):
                if "-" in part:
                    start, end = map(int, part.split("-"))
                    weeks.extend(range(start, end + 1))
                else:
                    weeks.append(int(part))
        return weeks
