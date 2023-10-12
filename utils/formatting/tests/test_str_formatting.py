import timeit
import unittest

from utils.formatting.str_formatting import StringFormatter


class TestStringFormatter(unittest.TestCase):

    def test_remove_non_letters(self):
        self.assertEqual(StringFormatter.remove_non_letters(' "Інженерія програмного забезпечення ", 3 р.н.'),
                         'Інженерія програмного забезпечення')
        self.assertEqual(StringFormatter.remove_non_letters(' "Комп`ютерні науки", 1 р.н.'),
                         'Комп`ютерні науки')
        self.assertEqual(StringFormatter.remove_non_letters('123 ABC'), 'ABC')
        self.assertEqual(StringFormatter.remove_non_letters(''), '')
        self.assertEqual(StringFormatter.remove_non_letters('!@#$%^&*()'), '')  # Special characters
        self.assertEqual(StringFormatter.remove_non_letters('  '), '')  # Only spaces
        self.assertEqual(StringFormatter.remove_non_letters('ABC 123 р.н. DEF'), 'ABC   DEF')  # Mixed string
        self.assertEqual(StringFormatter.remove_non_letters('р.н.р.н.'), '')  # Only 'р.н.'

    def test_remove_everything_after_last_digit(self):
        self.assertEqual(StringFormatter.remove_everything_after_last_digit('24f46hello'), '24f46')
        self.assertEqual(StringFormatter.remove_everything_after_last_digit('abc'), '')  # No digits
        self.assertEqual(StringFormatter.remove_everything_after_last_digit('123abc456'),
                         '123abc456')  # Last character is a digit
        self.assertEqual(StringFormatter.remove_everything_after_last_digit(''), '')  # Empty string
        self.assertEqual(StringFormatter.remove_everything_after_last_digit('123'), '123')  # Only digits
        self.assertEqual(StringFormatter.remove_everything_after_last_digit('abc123'), 'abc123')  # Ends with digits


def time_function_call(func, *args, **kwargs):
    def wrapper():
        return func(*args, **kwargs)

    return timeit.timeit(wrapper, number=10000)


# if __name__ == '__main__':
    # unittest.main()

print("Timing remove_non_letters:")
print(time_function_call(StringFormatter.remove_non_letters, ' "Інженерія програмного забезпечення ", 3 р.н.'))
print("Timing remove_everything_after_last_digit:")
print(time_function_call(StringFormatter.remove_everything_after_last_digit, '24f46hello'))
