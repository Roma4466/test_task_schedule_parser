from datetime import datetime


class TimeFormatter:
    @staticmethod
    def parse_time(time_str: str) -> datetime:
        today = datetime.now().date()
        start_time_str = time_str.replace('.', ':').rjust(5, '0')
        return datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())

    @staticmethod
    def format_datetime_for_json(obj):
        if isinstance(obj, datetime):
            return f"{obj.day}-{obj.month}" if obj.year == datetime.now().year else f"{obj.month}-{obj.year - 2000}"
        return obj
