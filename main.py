import argparse
import time

import pandas as pd

from utils.schedule_analyzer import ScheduleParser


def main(file_name):
    start_analysis(file_name)


def without_arguments():
    name = str(input("Write file name without extension, for example: fen:\n"))
    start_analysis(name)


def start_analysis(name):
    start_time = time.time()  # Store the start time

    try:
        file_path = f'data/{name}.xlsx'
        df = pd.read_excel(file_path, header=None)
        ScheduleParser.parse_schedule(df, name)

        print("Analysis finished, seek json result file in output folder")
        print("Note, that file may be in wrong encoding for your IDE")
        print("If you are using PyCharm, just click on \"Reload in 'windows-1251'\"")
    except FileNotFoundError:
        print("No such file in data folder. Please write correct name")

    end_time = time.time()  # Store the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"The start_analysis method took {elapsed_time} seconds to complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze schedule data.')
    parser.add_argument('file_name', type=str, nargs='?', help='The name of the Excel file without extension')

    args = parser.parse_args()

    if args.file_name:
        main(args.file_name)
    else:
        print("Drag your file into data folder in root directory of this project")
        without_arguments()
