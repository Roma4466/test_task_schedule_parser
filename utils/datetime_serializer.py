from datetime import datetime


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%H:%M')
    raise TypeError("Type not serializable")
