import unittest
from unittest.mock import patch
from io import StringIO
from main import read_map


class TestMain(unittest.TestCase):

    def setUp(self):
        # Common mocks for all tests
        self.exit_patch = patch('sys.exit')
        self.mock_exit = self.exit_patch.start()

    def tearDown(self):
        # Stop all patches to clean up after each test
        patch.stopall()

    def run_read_map_with_input(self, stdin_value, argv_value=['main.py', '0']):
        """ Utility method to run `read_map` with mocked stdin and sys.argv, capturing all output """
        with patch('sys.stdin', StringIO(stdin_value)), patch('sys.argv', argv_value), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            read_map()
            captured_output = mock_stdout.getvalue()  # Capture all printed output
            return captured_output

    ### Error handling tests ###
    def assert_error_message(self, expected_message):
        """ Utility method to assert error message and exit """
        captured_output = self.mock_writeln.call_args[0][0]
        self.assertEqual(captured_output, expected_message)
        self.mock_exit.assert_called_once()

    def test_invalid_input(self):
        """ Test invalid input with negative values """
        printed_output = self.run_read_map_with_input('-10 -10 s sort')
        self.assertIn('ERROR: Invalid configuration line', printed_output)

    def test_valid_input(self):
        """ Test valid input """
        printed_output = self.run_read_map_with_input('10 10 s sort')
        self.assertNotIn('ERROR', printed_output)
        self.mock_exit.assert_not_called()

    def test_edge_case_input(self):
        """ Test edge case with input on the boundary """
        printed_output = self.run_read_map_with_input('0 0 s sort')
        self.assertIn('ERROR', printed_output)
        self.mock_exit.assert_called_once()

    ### Full map tests ###
    def generate_expected_full_map(self, map_size, entities):
        """ Utility method to generate the expected full map output with entities """
        output = []
        # Generate top coordinate row
        top_num_row = '    ' + ' '.join(f'{i:03}' for i in range(map_size))
        output.append(top_num_row)

        # Generate grid lines and coordinate labels
        for row in range(map_size - 1, -1, -1):  # Generate rows from bottom to top
            separator = '   +' + '---+' * map_size
            output.append(separator)

            side_num = f'{row:03}'
            row_content = f'{side_num}|'
            for col in range(map_size):
                if (row, col) in entities:
                    entity_icon = entities[(row, col)]
                    row_content += f' {entity_icon} |'
                else:
                    row_content += '   |'
            output.append(row_content)

        # Final border line
        output.append('   +' + '---+' * map_size)
        return '\n'.join(output)  # Join lines to form full map

    def test_full_map(self):
        """ Test the full map output with a flower placed at (2, 2) """
        map_size = 10  # Define map size
        iterations = 5  # Define number of iterations
        # Valid flower setup
        flower_input = f'{map_size} {iterations} f sort\nF 2 2 2\n1.0\n2.0\n'

        # Run the function and capture all terminal output
        printed_output = self.run_read_map_with_input(stdin_value=flower_input)

        # Define entities with their positions and icons
        entities = {(2, 2): 'F'}  # Flower placed at (2, 2)

        # Generate expected full map output
        expected_full_map = self.generate_expected_full_map(
            map_size=map_size, entities=entities)

        # Debugging: Print the expected output for comparison
        # print("Expected Map Output:\n", expected_full_map)
        # print("Captured output:\n", expected_full_map)

        if len(expected_full_map) != len(printed_output):
            printed_output = printed_output[:len(expected_full_map)]
            # print("Captured output (TRIMMED):\n", printed_output)

        # Assert that the full map is printed correctly
        self.assertEqual(printed_output.strip(), expected_full_map.strip(
        ), f"\nExpected Map:\n{expected_full_map}\n\nBut got:\n{printed_output}")


if __name__ == '__main__':
    unittest.main()
