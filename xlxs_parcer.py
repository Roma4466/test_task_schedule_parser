from datetime import datetime

import pandas as pd

from coordinates_getter import get_coordinates_by_name
import json


def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%H:%M')
    raise TypeError("Type not serializable")


def analyze(df, faculty, specialty, year_of_study, started_year):
    day_column = get_coordinates_by_name(df, "День")
    time_column = get_coordinates_by_name(df, "Час")
    disciple_column = get_coordinates_by_name(df, "Дисципліна, викладач")
    group_column = get_coordinates_by_name(df, "Група")
    week_column = get_coordinates_by_name(df, "Тижні")
    room_column = get_coordinates_by_name(df, "Аудиторія") if get_coordinates_by_name(df, "Аудиторія") else \
        get_coordinates_by_name(df, "Ауд.")

    final_parsed_data = {
        faculty: {
            specialty: {},
            "Рік навчання": year_of_study,
            "Роки навчального року": [started_year, started_year + 1],
        }
    }
    current_day = ""
    current_time = ""

    column_of_day = get_coordinates_by_name(df, "День")

    for index, row in df.iterrows():
        if index < column_of_day + 1:
            continue

        if pd.notna(row[day_column]):
            current_day = row[day_column]
        current_time = row[time_column] if pd.notna(row[time_column]) else current_time

        discipline_info = row[disciple_column] if pd.notna(row[disciple_column]) else ""

        if not discipline_info:
            continue

        discipline = discipline_info.split(", ")[0]
        teacher = discipline_info.split(", ")[1]

        group = row[group_column] if pd.notna(row[group_column]) else ""
        week = row[week_column] if pd.notna(row[week_column]) else ""
        room = row[room_column] if pd.notna(row[room_column]) else ""

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
