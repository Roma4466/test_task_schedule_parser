from read_specialities import read_faculty_and_specialties
from time_parcer import parce_time
from xlxs_parcer import analyze, datetime_serializer

from docx import Document
import json

# in this file i was trying to handle schedule from .docx file
# but unfortunately, table is movind aside as I move down
# so i decided to convert docx to xlsx and handle that file

SPECIALITIES = "Спеціальності"

# Load the document
doc_path = 'data/3.docx'  # Replace this with your document path
document = Document(doc_path)

faculty, specialities, year_of_study, started_year = read_faculty_and_specialties(document)

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

day_column = -1
time_column = 0
disciple_column = 1
group_column = 3
week_column = 6
room_column = 7

# Skipping header row by starting from index 1
for row in document.tables[0].rows[1:]:
    cells = [cell.text.strip() for cell in row.cells]

    if cells[day_column]:
        current_day = cells[day_column]
    current_time = cells[time_column] if cells[time_column] else current_time
    discipline_info = cells[disciple_column] if cells[disciple_column] else ""

    if not discipline_info:
        continue

    discipline = discipline_info.split("(")[0]
    teacher = discipline_info.split(")")[1]
    speciality_abbreviation = discipline_info.split(")")[0].split("(")[1][:-1]
    group = cells[group_column] if cells[group_column] else ""
    week = cells[week_column] if cells[week_column] else ""
    room = cells[room_column] if cells[room_column] else ""

    speciality = ""
    for speciality_from_docx in specialities:
        if speciality_from_docx.lower().startswith(speciality_abbreviation):
            speciality = speciality_from_docx
            break

    print(f"day of week: {current_day}",
          f"time: {current_time}",
          f"disciple: {discipline}",
          f"group: {group}",
          f"week: {week}",
          f"room: {room}")

    if discipline not in final_parsed_data[faculty][SPECIALITIES][speciality]:
        final_parsed_data[faculty][SPECIALITIES][speciality][discipline] = {}
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

# Output final data
print(final_parsed_data)
json_str = json.dumps(final_parsed_data, indent=4, default=datetime_serializer, ensure_ascii=False)
with open('output/final_parsed_data.json', 'w') as f:
    f.write(json_str)
