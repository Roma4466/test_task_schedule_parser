from utils.str_formatting import remove_non_letters

SPECIALITY_FIELD_NAME = 'Спеціальність'
FACULTY_FIELD_NAME = 'Факультет'


def read_faculty_and_specialties(df):
    faculty = ""
    specialities = []
    year_of_study = 0
    started_year = 0
    is_read_specialities = False
    is_read_faculty = False
    digits = ""

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        for col_index in range(min(7, df.shape[1])):
            text = str(row.iloc[col_index])
            current_string = ""
            for symbol in text:
                if symbol.isdigit():
                    digits += symbol
                else:
                    if len(digits) == 4:
                        started_year = int(digits)
                    digits = ""

                if current_string == SPECIALITY_FIELD_NAME:
                    current_string = ""
                    is_read_specialities = True
                elif current_string == FACULTY_FIELD_NAME:
                    is_read_faculty = True
                current_string += symbol

            if is_read_faculty:
                faculty = current_string
                is_read_faculty = False
            if is_read_specialities:
                for i in current_string:
                    if i.isdigit():
                        year_of_study = int(i)
                specialities_tmp = current_string.split("», ")
                for speciality in specialities_tmp:
                    speciality = remove_non_letters(speciality)
                    specialities.append(speciality)
                is_read_specialities = False

    return faculty, specialities, year_of_study, started_year
