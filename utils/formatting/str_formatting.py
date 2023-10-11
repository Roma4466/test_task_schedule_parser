class StringFormatter:
    @staticmethod
    def remove_non_letters(input_str: str) -> str:
        """
        Removes all numbers, spaces from start/end, special symbols from string and return plain text with spaces
        :param input_str: f.e ' "Інженерія програмного забезпечення ", 3 р.н.'
        :return: f.e 'Інженерія програмного забезпечення'
        """
        input_str = input_str.replace("р.н.", "")
        input_str = ''.join(c for c in input_str if c.isalpha() or c == ' ' or c == "`")
        return StringFormatter.remove_spaces_from_start_and_end(input_str)

    @staticmethod
    def remove_spaces_from_start_and_end(input_str: str) -> str:
        while len(input_str) > 1 and input_str[0] == " ":
            input_str = input_str[1:]
        while len(input_str) > 1 and input_str[-1] == " ":
            input_str = input_str[:-1]
        return input_str
