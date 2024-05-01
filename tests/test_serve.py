import pytest
from http.server import SimpleHTTPRequestHandler
from src.serve import SingleDirectoryHTTPRequestHandler

def test_single_directory_http_request_handler():
    handler = SingleDirectoryHTTPRequestHandler
    assert issubclass(handler, SimpleHTTPRequestHandler)
    
def test_single_directory_http_request_handler_inherits_from_simple_http_request_handler():
    assert issubclass(SingleDirectoryHTTPRequestHandler, SimpleHTTPRequestHandler)
