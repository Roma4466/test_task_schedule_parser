import unittest
from datetime import datetime, time

from utils.formatting.time_parcer import TimeFormatter


class TestTimeFormatter(unittest.TestCase):

    def test_parce_time(self):
        today = datetime.now().date()
        self.assertEqual(TimeFormatter.parce_time("8:30").time(), time(8, 30))
        self.assertEqual(TimeFormatter.parce_time("8.30").time(), time(8, 30))
        self.assertEqual(TimeFormatter.parce_time("08:30").date(), today)
        self.assertEqual(TimeFormatter.parce_time("8.30").date(), today)
        self.assertEqual(TimeFormatter.parce_time("8:30").time(), time(8, 30))

    def test_format_datetime_for_json(self):
        current_year = datetime.now().year
        self.assertEqual(TimeFormatter.format_datetime_for_json(datetime(current_year, 1, 14)), "14-1")
        self.assertEqual(TimeFormatter.format_datetime_for_json(datetime(current_year + 1, 1, 14)), "1-24")
        self.assertEqual(TimeFormatter.format_datetime_for_json("1-14"), "1-14")
        self.assertEqual(TimeFormatter.format_datetime_for_json(None), None)
