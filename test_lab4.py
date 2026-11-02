import unittest
from unittest.mock import patch, mock_open
from lab4 import extract_bytes, process_log, read_lines_in_chunks


class TestNginxParser(unittest.TestCase):

    def test_extract_bytes_valid_both(self):
        line = '127.0.0.1 - - [12/Oct/2026] "POST / HTTP/1.1" 200 1024 512'
        self.assertEqual(extract_bytes(line), (1024, 512))

    def test_extract_bytes_missing_received(self):
        line = '127.0.0.1 - - [12/Oct/2026] "GET / HTTP/1.1" 200 2048'
        self.assertEqual(extract_bytes(line), (2048, 0))

    def test_extract_bytes_hyphens(self):
        line = '127.0.0.1 - - [12/Oct/2026] "GET / HTTP/1.1" 404 - -'
        self.assertEqual(extract_bytes(line), (0, 0))

    @patch("builtins.open", new_callable=mock_open,
           read_data='127.0.0.1 "GET" 200 100 50\n127.0.0.1 "GET" 200 200 150\n')
    def test_process_log(self, mock_file):
        sent, received = process_log("dummy.log")
        self.assertEqual(sent, 300)
        self.assertEqual(received, 200)

    @patch("builtins.open", new_callable=mock_open, read_data='line1\nline2\nline3')
    def test_read_lines_in_chunks(self, mock_file):
        lines = list(read_lines_in_chunks("dummy.log", chunk_size=5))
        self.assertEqual(lines, ['line1', 'line2', 'line3'])


if __name__ == '__main__':
    unittest.main()