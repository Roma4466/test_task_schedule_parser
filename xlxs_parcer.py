import json

import pandas as pd

from coordinates_getter import get_coordinates_of_column
from read_specialities import read_faculty_and_specialties
from speciality_extractor import extract_speciality_from_abbreviation
from str_formatting import remove_spaces_from_start_and_end
from time_parcer import datetime_serializer

SPECIALITIES_FIELD_NAME = "Спеціальності"


def analyze(df):
    is_several_specialities = False

    # getting column number
    day_column = get_coordinates_of_column(df, ["День"])[1]
    time_column = get_coordinates_of_column(df, ["Час"])[1]
    disciple_column = get_coordinates_of_column(df, ["Дисципліна, викладач"])[1]
    group_column = get_coordinates_of_column(df, ["Група"])[1]
    week_column = get_coordinates_of_column(df, ["Тижні", "Тиждень"])[1]
    room_column = get_coordinates_of_column(df, ["Аудиторія", "Ауд."])[1]

    faculty, specialities, year_of_study, started_year = read_faculty_and_specialties(df)
    is_several_specialities = len(specialities) > 1

    # Initialize the final data structure to hold the parsed information
    final_parsed_data = {
        faculty: {
            SPECIALITIES_FIELD_NAME: {},
            "Рік навчання": year_of_study,
            "Роки навчального року": [started_year, started_year + 1],
        }
    }
    for current_specialities in specialities:
        final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][current_specialities] = {}
    # because of if there is time in 2 cels
    # python reads it like it is only in one cell
    # so I have save last time
    current_time = ""
    current_day = ""
    previous_disciple = ""
    group = ""
    room = ""
    week = ""
    current_specialities = ""

    # getting row number where schedule starts
    coordinates = get_coordinates_of_column(df, "День")[0]

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

        group = row[group_column] if pd.notna(row[group_column]) else group
        week = row[week_column] if pd.notna(row[week_column]) else week
        week = format_datetime_for_json(week)
        room = row[room_column] if pd.notna(row[room_column]) else room
        # if this cell is empty then
        # there is no need to read further
        if not discipline_info:
            continue

        if is_several_specialities:
            if len(discipline_info.split(")")) < 2:
                # sometimes it parses disciple info in 2 cells
                # in first disciple in second teacher name
                teacher = remove_spaces_from_start_and_end(discipline_info)
                discipline = remove_spaces_from_start_and_end(previous_disciple)
            else:
                discipline = remove_spaces_from_start_and_end(discipline_info.split("(")[0])
                previous_disciple = discipline
                teacher = remove_spaces_from_start_and_end(discipline_info.split(")")[1])
                if not teacher.replace(" ", ""):
                    continue
                current_specialities = extract_speciality_from_abbreviation(discipline_info, specialities)

            for speciality in current_specialities:
                if discipline not in final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][speciality]:
                    final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][speciality][discipline] = {}
                if group not in final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][speciality][discipline]:
                    final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][speciality][discipline][group] = {}

            start_time_str, end_time_str = current_time.split('-')
            start_time_str = start_time_str.replace(".", ":")
            end_time_str = end_time_str.replace(".", ":")

            for speciality in current_specialities:
                final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][speciality][discipline][group] = {
                    "час початку": start_time_str,
                    "час кінця": end_time_str,
                    "тижні": week,
                    "аудиторія": room,
                    "день тижня": current_day,
                    "викладач": teacher
                }
        else:
            discipline = discipline_info.split(", ")[0]
            teacher = discipline_info.split(", ")[1]
            # now we know faculty, specialty, discipline
            # then let`s initialize field in result file
            if discipline not in final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][specialities[0]]:
                final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][specialities[0]][discipline] = {}

            if group not in final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][specialities[0]][discipline]:
                final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][specialities[0]][discipline][group] = {}

            start_time_str, end_time_str = current_time.split('-')

            final_parsed_data[faculty][SPECIALITIES_FIELD_NAME][specialities[0]][discipline][group] = {
                "час початку": start_time_str,
                "час кінця": end_time_str,
                "тижні": week,
                "аудиторія": room,
                "день тижня": current_day,
                "викладач": teacher
            }

    json_str = json.dumps(final_parsed_data, indent=4, default=datetime_serializer, ensure_ascii=False)

    with open('output/final_parsed_data.json', 'w') as f:
        f.write(json_str)
