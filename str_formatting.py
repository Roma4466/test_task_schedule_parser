# this method does from this:
# ' "Інженерія програмного забезпечення ", 3 р.н.'
# this:
# 'Інженерія програмного забезпечення'
def remove_non_letters(input_str):
    input_str = input_str.replace("р.н.", "")
    input_str = ''.join(c for c in input_str if c.isalpha() or c == ' ')
    return remove_spaces_from_start_and_end(input_str)


def remove_spaces_from_start_and_end(input_str):
    while len(input_str) > 1 and input_str[0] == " ":
        input_str = input_str[1:]
    while len(input_str) > 1 and input_str[-1] == " ":
        input_str = input_str[:-1]
    return input_str
