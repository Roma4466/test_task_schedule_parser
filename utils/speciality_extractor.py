import re


def extract_speciality_from_abbreviation(str_input, specialities):
    result = set()
    before_and_after_opening_parenthesis = str_input.split("(")
    filtered_list = [i for i in before_and_after_opening_parenthesis if ")" in i]
    for string in filtered_list:
        split = string.split(")")[0]
        # split by "," or "+"
        split = re.split(r'[,+]', split)
        for abbreviation in split:
            without_non_letters = abbreviation.replace(")", "").replace(".", "").replace(" ", "")
            for speciality in specialities:
                if without_non_letters in speciality.lower():
                    result.add(speciality)
    return result
