import unittest
from http.server import HTTPServer
from src.serve import SingleDirectoryHTTPRequestHandler

class TestSingleDirectoryHTTPRequestHandler(unittest.TestCase):
    def test_inheritance(self):
        handler = SingleDirectoryHTTPRequestHandler
        self.assertIsInstance(handler, http.server.SimpleHTTPRequestHandler)

if __name__ == '__main__':
    unittest.main()