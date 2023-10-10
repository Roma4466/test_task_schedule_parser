from datetime import datetime


def parce_time(time_str):
    today = datetime.now().date()
    # Replace the dot with a colon
    start_time_str = time_str.replace('.', ':')
    # Add a leading zero if the hour is a single digit
    if len(start_time_str.split(':')[0]) == 1:
        start_time_str = '0' + start_time_str

    return datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())


# when I convert table from .docx to .xlxs file
# it converts numbers of week "1-14" into type datetime
# 01.01.2014, so I have to do it reverse
def format_datetime_for_json(obj):
    if isinstance(obj, datetime):
        current_year = datetime.now().year
        # if second number of weeks was less than 12
        # it converts first to day of month and second to number of month
        if obj.year == current_year:
            return f"{obj.day}-{obj.month}"
        else:
            return f"{obj.month}-{obj.year - 2000}"
    else:
        return obj


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%H:%M')
    raise TypeError("Type not serializable")
