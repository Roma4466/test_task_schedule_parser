import argparse

import pandas as pd

from utils.schedule_analyzer import ScheduleParser


def main(file_name):
    try:
        file_path = f'data/{file_name}.xlsx'
        df = pd.read_excel(file_path, header=None)
        parser = ScheduleParser()
        parser.parse_schedule(df, file_name)

        print("Analysis finished, seek json result file in output folder")
        print("Note, that file may be in wrong encoding for your IDE")
        print("If you are using PyCharm, just click on \"Reload in 'windows-1251'\"")
    except FileNotFoundError:
        print("No such file in data folder. Please write correct name")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze schedule data.')
    parser.add_argument('file_name', type=str, help='The name of the Excel file without extension')

    args = parser.parse_args()
    main(args.file_name)
