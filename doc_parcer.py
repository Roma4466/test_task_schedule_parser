from docx import Document
from datetime import datetime

import pandas as pd

import json

from read_doc import read_faculty_and_specialties
from time_parcer import parce_time
from xlxs_parcer import analyze, datetime_serializer

SPECIALITIES = "Спеціальності"

# Load the document
doc_path = 'data/3.docx'
document = Document(doc_path)

(faculty, specialities, year_of_study, started_year) = read_faculty_and_specialties(document)

table = document.tables[0]
data = []

for row in table.rows:
    row_data = []
    for cell in row.cells:
        row_data.append(cell.text.strip())
    data.append(row_data)

df = pd.DataFrame(data)

df.columns = df.iloc[0]
df = df.drop(df.index[0])

day_column = -1
time_column = 0
disciple_column = 1
group_column = 3
week_column = 6
room_column = 7

final_parsed_data = {
    faculty: {
        SPECIALITIES: {},
        "Рік навчання": year_of_study,
        "Роки навчального року": [started_year, started_year + 1],
    }
}

for speciality in specialities:
    final_parsed_data[faculty][SPECIALITIES][speciality] = {}

current_day = ""
current_time = ""
for index, row in df.iterrows():
    if pd.notna(row.iloc[day_column]):
        current_day = row.iloc[day_column]
    current_time = row.iloc[time_column] if pd.notna(row.iloc[time_column]) else current_time
    discipline_info = row.iloc[disciple_column] if pd.notna(row.iloc[disciple_column]) else ""
    if not discipline_info:
        continue
    discipline = discipline_info.split("(")[0]
    teacher = discipline_info.split(")")[1]

    # after this line from
    # "Навчально-науковий семінар з економіки (екон.) проф. Бураковський І.В."
    # will be
    # "екон"
    speciality_abbreviation = discipline_info.split(")")[0].split("(")[1][:-1]

    group = row.iloc[group_column] if pd.notna(row.iloc[group_column]) else ""
    week = row.iloc[week_column] if pd.notna(row.iloc[week_column]) else ""
    room = row.iloc[room_column] if pd.notna(row.iloc[room_column]) else ""

    print(f"day of week: {current_day}",
          f"time: {current_time}",
          f"disciple: {discipline}",
          f"group: {group}",
          f"week: {week}",
          f"room: {room}")

    # here can be several specialities so we have to understand which is it
    speciality = ""
    for speciality_from_docx in specialities:
        speciality_lowered = speciality_from_docx.lower()
        if speciality_lowered[:len(speciality_abbreviation)] == speciality_abbreviation:
            speciality = speciality_from_docx

    if discipline not in final_parsed_data[faculty][SPECIALITIES][speciality]:
        final_parsed_data[faculty][SPECIALITIES][speciality][discipline] = {
        }
    if group not in final_parsed_data[faculty][SPECIALITIES][speciality][discipline]:
        final_parsed_data[faculty][SPECIALITIES][speciality][discipline][group] = {}

    start_time_str, end_time_str = current_time.split('-')
    start_time = parce_time(start_time_str)
    end_time = parce_time(end_time_str)

    final_parsed_data[faculty][SPECIALITIES][speciality][discipline][group] = {
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
