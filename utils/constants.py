from enum import StrEnum


class FieldsNames(StrEnum):
    # fields names from .xlsx file
    SPECIALITY_FIELD_NAME = 'Спеціальність'
    FACULTY_FIELD_NAME = 'Факультет'
    SPECIALITIES_FIELD_NAME = "Спеціальності"
    LECTURE_FIELD_NAME = "лекція"
    DAY_FIELD_NAMES = "День"
    TIME_FIELD_NAME = "Час"
    DISCIPLE_INFO_FIELD_NAME = "Дисципліна, викладач"
    GROUP_FIELD_NAME = "Група"

    # fields names in .json file
    TIME_START = "час початку"
    TIME_END = "час кінця"
    WEEKS = "тижні"
    ROOM = "Аудиторія"
    TEACHER = "викладач"
