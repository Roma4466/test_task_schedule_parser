# FIDO 2023 Developer Test Task: Schedule Parser for NaUKMA

## Description

This project aims to unify the schedules of different faculties at NaUKMA by creating a parser. The parser will read the
schedules from `.xlsx` files and convert them into a standardized JSON format.

## Problem Statement

There is no unified standard for schedules at NaUKMA. This parser aims to solve that problem by providing a readable
data structure for schedules.

## Installation

1. Clone this repository
   git clone https://github.com/Roma4466/test_task_schedule_parser.git
2. Run `pip install -r requirements.txt`

## Usage

1. Drag your file into `data` folder in root directory of this project (for example, fen.xlsx)
2. Run `python main.py your_file_name_without_extension`

## Output

A unified JSON structure containing the schedules for every major in `output` folder<br>
Note, that file may be in wrong encoding for your IDE<br>
If you are using PyCharm, just click on "Reload in 'windows-1251'"

## Data Structure Example

You can find in `output\fen.json`

## Technologies Used

+ Python
+ Pandas
+ JSON

## Examples

You can find several examples of .xlsx files in data folder, to check them just run main.py and type file from its
folder name into console 
