import unittest
from src.bracket_validator.validator import validate_brackets


class TestBracketValidator(unittest.TestCase):
    def test_valid_brackets(self):
        self.assertEqual(validate_brackets("<div><p>{ test }</p></div>"), "Строка валідна")
        self.assertEqual(validate_brackets("()"), "Строка валідна")
        self.assertEqual(validate_brackets("Без дужок взагалі"), "Строка валідна")

    def test_unbalanced_closing(self):
        with self.assertRaises(ValueError) as context:
            validate_brackets("<div><p>{ test }}</p</div>")

        error_msg = str(context.exception)
        self.assertIn("Дужки незбалансовані на позиціях", error_msg)
        self.assertIn("^", error_msg)

    def test_unclosed_opening(self):
        with self.assertRaises(ValueError):
            validate_brackets("({<test>")


if __name__ == '__main__':
    unittest.main()