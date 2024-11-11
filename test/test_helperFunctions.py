import json
import os
import unittest

from src.helperFunctions import (
    get_commands,
    numeric_str_to_int,
    convert_to_spelling,
    string_to_camel_case,
    string_to_snake_case,
)


class TestHelperFunction(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_commands_dir"
        self.test_empty_dir = "test_empty_commands_dir"
        self.test_not_a_dir = "non_existent_dir"

        # Setup a temporary test directory for get_commands
        os.makedirs(self.test_dir, exist_ok=True)

        # Setup a temporary test directory for get_commands
        os.makedirs(self.test_empty_dir, exist_ok=True)

        # Create a valid JSON file
        with open(os.path.join(self.test_dir, "test_commands.json"), "w") as f:
            json.dump({"command1": "action1"}, f)

        # Create an invalid JSON file
        with open(os.path.join(self.test_dir, "invalid_commands.json"), "w") as f:
            f.write("{invalid json}")

    def tearDown(self):
        # Clean up by removing files and directory
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)
        os.rmdir(self.test_empty_dir)

    def test_get_commands_valid_directory(self):
        commands = get_commands(self.test_dir)
        self.assertIn("command1", commands)
        self.assertEqual(commands["command1"], "action1")

    def test_get_commands_invalid_directory(self):
        self.assertEqual(get_commands(self.test_not_a_dir), {})

    def test_get_commands_empty_directory(self):
        self.assertEqual(get_commands(self.test_empty_dir), {})

    def test_numeric_str_to_int_valid_input(self):
        self.assertEqual(numeric_str_to_int("three"), 3)
        self.assertEqual(numeric_str_to_int("seven"), 7)
        self.assertEqual(numeric_str_to_int("one two three"), 123)
        self.assertEqual(numeric_str_to_int("seven eight"), 78)
        self.assertEqual(numeric_str_to_int("nine eight seven six five four"), 987654)

    def test_numeric_str_to_int_invalid_input(self):
        with self.assertRaises(ValueError):
            numeric_str_to_int("invalid input")

    def test_convert_to_spelling_single_input(self):
        class Command:
            def __init__(self, name, key):
                self.name = name
                self.key = key

        spelling_commands = [Command("alpha", "a"), Command("beta", "b")]
        self.assertEqual(convert_to_spelling("beta", spelling_commands), "b")
        self.assertEqual(convert_to_spelling("alpha beta", spelling_commands), "ab")
        self.assertEqual(
            convert_to_spelling("alpha gamma", spelling_commands), "a"
        )  # Gamma ignored

    def test_string_to_camel_case(self):
        self.assertEqual(string_to_camel_case("hello"), "Hello")
        self.assertEqual(string_to_camel_case("hello world"), "HelloWorld")

    def test_string_to_snake_case_single_input(self):
        self.assertEqual(string_to_snake_case("hello"), "hello")
        self.assertEqual(string_to_snake_case("hello world"), "hello_world")


if __name__ == "__main__":
    unittest.main()
