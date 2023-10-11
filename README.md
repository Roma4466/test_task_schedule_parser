# FIDO 2023 Developer Test Task: Schedule Parser for NaUKMA

## Description

This project aims to unify the schedules of different faculties at NaUKMA by creating a parser. The parser will read the schedules from `.xlsx` files and convert them into a standardized JSON format.

## Problem Statement

There is no unified standard for schedules at NaUKMA. This parser aims to solve that problem by providing a readable data structure for schedules.

## Installation

1. Clone this repository
git clone https://github.com/Roma4466/test_task_schedule_parser.git
2. Install the required packages

## Usage

1. Run `pip install -r requirements.txt`
2. Drag your file into `data` folder in root directory of this project (for example, fen.xlsx)
3. Run `python main.py`
4. Write file name without extension, for example: fen

## Output

A unified JSON structure containing the schedules for every major in `output` folder<br>
Note, that file may be in wrong encoding for your IDE<br>
If you are using PyCharm, just click on "Reload in 'windows-1251'"

## Data Structure Example

```json
{
    "Факультет економічних наук": {
        "Спеціальності": {
            "Економіка": {
                "Навчально-науковий семінар з економіки": {
                    "1": {
                        "час початку": "8:30",
                        "час кінця": "9:50",
                        "тижні": "1-14",
                        "аудиторія": "Д",
                        "день тижня": "Понеділок",
                        "викладач": "проф. Бураковський І.В."
                    }
                },
            },
            "Фінанси банківська справа та страхування": {
                "Конкурентна розвідка": {
                    "лекція": {
                        "час початку": "15:00",
                        "час кінця": "16:20",
                        "тижні": 2,
                        "аудиторія": "Д",
                        "день тижня": "Четвер",
                        "викладач": "ст. викл. Синько Д."
                    },
                    "1": {
                        "час початку": "15:00",
                        "час кінця": "16:20",
                        "тижні": "3-9",
                        "аудиторія": "Д",
                        "день тижня": "Четвер",
                        "викладач": "ст. викл. Синько Д."
                    },
                    "2": {
                        "час початку": "16:30",
                        "час кінця": "17:50",
                        "тижні": "3-9",
                        "аудиторія": "Д",
                        "день тижня": "Четвер",
                        "викладач": "ст. викл. Синько Д."
                    },
                    "3": {
                        "час початку": "8:30",
                        "час кінця": "9:50",
                        "тижні": "2,4,5,6,7,8",
                        "аудиторія": "Д",
                        "день тижня": "’ятниця",
                        "викладач": "доц. Братик М.В."
                    },
                    "3пр": {
                        "час початку": "8:30",
                        "час кінця": "9:50",
                        "тижні": "9-14",
                        "аудиторія": "Д",
                        "день тижня": "’ятниця",
                        "викладач": "доц. Братик М.В."
                    }
                }
            },
        },
        "Рік навчання": 3,
        "Роки навчального року": [
            2023,
            2024
        ]
    }
}
```

## Technologies Used
+ Python
+ Pandas
+ JSON

## Examples

You can find several examples of .xlsx files in data folder, to check them just run main.py and type file from its folder name into console 
