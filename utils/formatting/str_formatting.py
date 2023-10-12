class StringFormatter:
    @staticmethod
    def remove_non_letters(input_str: str) -> str:
        input_str = input_str.replace("р.н.", "")
        cleaned_str = ''.join(c for c in input_str if c.isalpha() or c == ' ' or c == '`')
        return cleaned_str.strip()

    @staticmethod
    def remove_everything_after_last_digit(input_str: str) -> str:
        last_digit_index = max((i for i, c in enumerate(input_str) if c.isdigit()), default=None)
        return input_str[:last_digit_index + 1] if last_digit_index is not None else ''
