import json

import pandas as pd
import os

from utils.formatting import time_parcer
from utils.coordinates_getter import get_coordinates_of_column
from utils.read_specialities import read_faculty_and_specialties
from utils.speciality_extractor import extract_speciality_from_abbreviation
from utils.formatting.str_formatting import remove_spaces_from_start_and_end

SPECIALITIES_FIELD_NAME = "Спеціальності"
LECTION_FIELD_NAME = "лекція"


class ScheduleParser:
    @staticmethod
    def parse_schedule(schedule_data_frame, name):
        """function that will parse schedule from .xlsx format into .json file"""
        is_several_specialities = False

        # getting column number
        day_column = get_coordinates_of_column(schedule_data_frame, ["День"])[1]
        time_column = get_coordinates_of_column(schedule_data_frame, ["Час"])[1]
        disciple_column = get_coordinates_of_column(schedule_data_frame, ["Дисципліна, викладач"])[1]
        group_column = get_coordinates_of_column(schedule_data_frame, ["Група"])[1]
        week_column = get_coordinates_of_column(schedule_data_frame, ["Тижні", "Тиждень"])[1]
        room_column = get_coordinates_of_column(schedule_data_frame, ["Аудиторія", "Ауд."])[1]

        faculty, specialities, year_of_study, started_year = read_faculty_and_specialties(schedule_data_frame)
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
        coordinates = get_coordinates_of_column(schedule_data_frame, "День")[0]

        for index, row in schedule_data_frame.iterrows():
            # before coordinates row there is basic
            # info about faculty etc.
            # there is no schedule there so I skip it
            if index < coordinates + 1:
                continue

            if pd.notna(row[day_column]):
                current_day = row[day_column]
            current_time = row[time_column] if pd.notna(row[time_column]) else current_time
            discipline_info = row[disciple_column] if pd.notna(row[disciple_column]) else ""

            group = str(row[group_column] if pd.notna(row[group_column]) else group)
            if LECTION_FIELD_NAME.lower() in group.lower():
                group = LECTION_FIELD_NAME
            else:
                for i in group:
                    if i.isdigit():
                        group = int(i)
                        break
            week = row[week_column] if pd.notna(row[week_column]) else week
            week = time_parcer.format_datetime_for_json(week)
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
                discipline = remove_spaces_from_start_and_end(discipline_info.split(", ")[0])
                teacher = remove_spaces_from_start_and_end(discipline_info.split(", ")[1]) if len(
                    discipline_info.split(", ")) > 1 else "???"
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

        json_str = json.dumps(final_parsed_data, indent=4, default=time_parcer.datetime_serializer, ensure_ascii=False)
        # Define the directory path
        output_dir = 'output'

        # Check if the directory exists, and if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'output/{name}.json', 'w') as f:
            f.write(json_str)
