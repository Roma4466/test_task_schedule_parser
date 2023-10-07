from datetime import datetime

import pandas as pd

from coordinates_getter import get_day_coordinates
import json

SPECIALITIES = "Спеціальності"


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%H:%M')
    raise TypeError("Type not serializable")


def analyze(df):
    # getting column number
    day_column = get_day_coordinates(df, "День")[1]
    time_column = get_day_coordinates(df, "Час")[1]
    disciple_column = get_day_coordinates(df, "Дисципліна, викладач")[1]
    group_column = get_day_coordinates(df, "Група")[1]
    week_column = get_day_coordinates(df, "Тижні")[1]
    room_column = get_day_coordinates(df, "Аудиторія")[1] if get_day_coordinates(df, "Аудиторія")[1] else \
        get_day_coordinates(df, "Ауд.")[1]

    # getting names of faculty, speciality etc.
    faculty = df.iloc[5, 0]
    specialty = df.iloc[6, 0].split("\"")[1]
    year_of_study = int(df.iloc[6, 0].split(", ")[1][0])
    started_year = int(df.iloc[7, 0].split("-")[0][-4:])

    # Initialize the final data structure to hold the parsed information
    final_parsed_data = {
        faculty: {
            specialty: {},
            "Рік навчання": year_of_study,
            "Роки навчального року": [started_year, started_year + 1],
        }
    }
    current_day = ""
    # because of if there is time in 2 cels
    # python reads it like it is only in one cell
    # so I have save last time
    current_time = ""

    # getting row number where schedule starts
    coordinates = get_day_coordinates(df, "День")[0]

    for index, row in df.iterrows():
        # before coordinates row there is basic
        # info about faculty etc.
        # there is no schedule there so I skip it
        if index < coordinates + 1:
            continue

        if pd.notna(row[day_column]):
            current_day = row[day_column]
        current_time = row[time_column] if pd.notna(row[time_column]) else current_time

        discipline_info = row[disciple_column] if pd.notna(row[disciple_column]) else ""

        # if this cell is empty then
        # there is no need to read further
        if not discipline_info:
            continue

        discipline = discipline_info.split(", ")[0]
        teacher = discipline_info.split(", ")[1]

        group = row[group_column] if pd.notna(row[group_column]) else ""
        week = row[week_column] if pd.notna(row[week_column]) else ""
        room = row[room_column] if pd.notna(row[room_column]) else ""

        # now we know faculty, specialty, discipline
        # then let`s initialize field in result file
        if discipline not in final_parsed_data[faculty][specialty]:
            final_parsed_data[faculty][specialty][discipline] = {
            }

        if group not in final_parsed_data[faculty][specialty][discipline]:
            final_parsed_data[faculty][specialty][discipline][group] = {}

        start_time_str, end_time_str = current_time.split('-')

        today = datetime.now().date()
        start_time = datetime.combine(today, datetime.strptime(start_time_str, '%H:%M').time())
        end_time = datetime.combine(today, datetime.strptime(end_time_str, '%H:%M').time())

        final_parsed_data[faculty][specialty][discipline][group] = {
            "час початку": start_time,
            "час кінця": end_time,
            "тижні": week,
            "аудиторія": room,
            "день тижня": current_day,
            "викладач": teacher
        }

    print(final_parsed_data)

    json_str = json.dumps(final_parsed_data, indent=4, default=datetime_serializer, ensure_ascii=False)

    with open('output/final_parsed_data.json', 'w') as f:
        f.write(json_str)
