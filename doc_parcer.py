from docx import Document
from datetime import datetime

import pandas as pd

import json

from read_doc import read_faculty_and_specialties
from xlxs_parcer import analyze

# Load the document
doc_path = 'data/3.docx'
document = Document(doc_path)

(faculty, specialities, year_of_study, started_year) = read_faculty_and_specialties(document)
while True:
    print(end="")
table = document.tables[0]
data = []

# Iterate through each row in table
for row in table.rows:
    row_data = []
    for cell in row.cells:
        row_data.append(cell.text.strip())
    data.append(row_data)

# Convert list of lists into DataFrame
df = pd.DataFrame(data)

# Optionally, set the column headers if they are in the first row
df.columns = df.iloc[0]
df = df.drop(df.index[0])

day_column = 0
time_column = 1
disciple_column = 2
group_column = 3
week_column = 4
room_column = 5

final_parsed_data = {
    faculty: {
        specialty: {},
        "Рік навчання": year_of_study,
        "Роки навчального року": [started_year, started_year + 1],
    }
}
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

analyze(df)
# print(df)
