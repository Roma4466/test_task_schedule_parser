from datetime import datetime


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
