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

```json
{
    "Факультет економічних наук": {
        "Спеціальності": {
            "Економіка": {
                "Навчально-науковий семінар з економіки": {
                    "1": {
                        "час початку": "8:30",
                        "час кінця": "9:50",
                        "тижні": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14
                        ],
                        "аудиторія": "Д",
                        "день тижня": "Понеділок",
                        "викладач": "проф. Бураковський І.В."
                    }
                }
            },
            "Фінанси банківська справа та страхування": {
                "Моделювання та управління фінансовими активами": {
                    "лекція": {
                        "час початку": "13:30",
                        "час кінця": "14:50",
                        "тижні": [
                            1
                        ],
                        "аудиторія": "Д",
                        "день тижня": "Понеділок",
                        "викладач": "проф. Долінський Л.Б."
                    },
                    "1": {
                        "час початку": "11:40",
                        "час кінця": "13:00",
                        "тижні": [
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8
                        ],
                        "аудиторія": "Д",
                        "день тижня": "Понеділок",
                        "викладач": "проф. Долінський Л.Б."
                    },
                    "2": {
                        "час початку": "16:30",
                        "час кінця": "17:50",
                        "тижні": [
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8
                        ],
                        "аудиторія": "00:00",
                        "день тижня": "Вівторок",
                        "викладач": "проф. Долінський Л.Б."
                    }
                },
                "Страхування": {
                    "2": {
                        "час початку": "13:30",
                        "час кінця": "14:50",
                        "тижні": [
                            2,
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "аудиторія": "00:00",
                        "день тижня": "Вівторок",
                        "викладач": "доц. Бридун Є.В."
                    },
                    "лекція": {
                        "час початку": "10:00",
                        "час кінця": "11:20",
                        "тижні": [
                            1
                        ],
                        "аудиторія": "Д",
                        "день тижня": "Четвер",
                        "викладач": "доц. Бридун Є.В."
                    },
                    "1": {
                        "час початку": "10:00",
                        "час кінця": "11:20",
                        "тижні": [
                            2,
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "аудиторія": "Д",
                        "день тижня": "Четвер",
                        "викладач": "доц. Бридун Є.В."
                    }
                }
            }
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

You can find several examples of .xlsx files in data folder, to check them just run main.py and type file from its
folder name into console 
