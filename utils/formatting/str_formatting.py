class StringFormatter:
    @staticmethod
    def remove_non_letters(input_str: str) -> str:
        """
        Removes all numbers, spaces from start/end, special symbols from string and return plain text with spaces
        :param input_str: f.e ' "Інженерія програмного забезпечення ", 3 р.н.'
        :return: f.e 'Інженерія програмного забезпечення'
        """
        input_str = input_str.replace("р.н.", "")
        input_str = ''.join(c for c in input_str if c.isalpha() or c == ' '
                            or c == "`"
                            )
        return StringFormatter.remove_spaces_from_start_and_end(input_str)

    @staticmethod
    def remove_spaces_from_start_and_end(input_str: str) -> str:
        while len(input_str) > 0 and input_str[0] == " ":
            input_str = input_str[1:]
        while len(input_str) > 0 and input_str[-1] == " ":
            input_str = input_str[:-1]
        return input_str

    @staticmethod
    def remove_everything_after_last_digit(input_str: str) -> str:
        """
        Removes all characters after the last digit in the string.
        :param input_str: f.e '24f46hello'
        :return: f.e '24f46'
        """
        last_digit_index = None
        for i, char in enumerate(reversed(input_str)):
            if char.isdigit():
                last_digit_index = len(input_str) - i - 1
                break
        if last_digit_index is not None:
            return input_str[:last_digit_index + 1]
        else:
            return ''
