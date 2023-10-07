SPECIALITY_FIELD_NAME = 'Спеціальність'
FACULTY_FIELD_NAME = 'Факультет'


def read_faculty_and_specialties(document):
    faculty = ""
    specialities = []
    year_of_study = 0
    started_year = 0
    is_read_specialities = False
    digits = ""

    current_string = ""
    for para in document.paragraphs:
        for run in para.runs:
            if run.bold:
                if run.text[:9] == FACULTY_FIELD_NAME:
                    faculty = run.text
                elif is_read_specialities:
                    split = run.text.split("»,")
                    for speciality in split:
                        if len(speciality) > 3:
                            if speciality[0] == " ":
                                speciality = speciality[1:]
                            if len(speciality) > 3 and speciality[0] == '«':
                                speciality = speciality[1:].replace("»", "")
                                specialities.append(speciality)
                    for symbol in run.text:
                        if symbol.isdigit():
                            year_of_study = int(symbol)
                            is_read_specialities = False
            else:
                for symbol in run.text:
                    if symbol.isdigit():
                        digits += symbol
                    else:
                        if len(digits) == 4:
                            started_year = int(digits)
                        digits = ""

                    if current_string == SPECIALITY_FIELD_NAME:
                        current_string = ""
                        is_read_specialities = True
                    else:
                        if (len(SPECIALITY_FIELD_NAME) > len(current_string)
                                and symbol == SPECIALITY_FIELD_NAME[len(current_string)]):
                            current_string += symbol
                        elif (len(FACULTY_FIELD_NAME) > len(current_string)
                              and symbol == FACULTY_FIELD_NAME[len(current_string)]):
                            current_string += symbol
                        else:
                            current_string = ""
    print(faculty, specialities, year_of_study, started_year - 1)
    return faculty, specialities, year_of_study, started_year - 1
