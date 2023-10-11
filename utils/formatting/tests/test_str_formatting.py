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

    def test_remove_spaces_from_start_and_end(self):
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end('  ABC  '), 'ABC')
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end('ABC'), 'ABC')
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end('  '), '')
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end(' A'), 'A')  # Single leading space
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end('A '), 'A')  # Single trailing space
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end(' A '),
                         'A')  # Single leading and trailing space
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end(' '), '')  # Single space
        self.assertEqual(StringFormatter.remove_spaces_from_start_and_end(''), '')  # Empty string
