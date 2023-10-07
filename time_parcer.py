from datetime import datetime


def parce_time(time_str):
    today = datetime.now().date()
    # Replace the dot with a colon
    start_time_str = time_str.replace('.', ':')
    # Add a leading zero if the hour is a single digit
    if len(start_time_str.split(':')[0]) == 1:
        start_time_str = '0' + start_time_str

    return datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())
