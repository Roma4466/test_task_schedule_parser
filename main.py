import pandas as pd

from utils.schedule_analyzer import ScheduleParser

print("Drag your file into data folder in root directory of this project")

name = str(input("Write file name without extension, for example: fen:\n"))
try:
    file_path = f'data/{name}.xlsx'
    df = pd.read_excel(file_path, header=None)
    parser = ScheduleParser()
    parser.parse(df, name)

    print("Analysis finished, seek json result file in output folder")
    print("Note, that file may be in wrong encoding for your IDE")
    print("If you are using PyCharm, just click on \"Reload in 'windows-1251'\"")
except FileNotFoundError:
    print("No such file in data folder. Please write correct name")
