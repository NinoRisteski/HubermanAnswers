import pytest
from unittest.mock import patch, MagicMock
from utils.chatbot import Chatbot 

# Mock the LoadConfig to provide test configuration
class MockConfig:
    persist_directory = "/fake/directory"
    embedding_model = MagicMock()
    llm_engine = "text-davinci-003"
    llm_system_role = "AI"
    k = 5
    number_of_q_a_pairs = 3

@pytest.fixture
def chatbot():
    return []

@pytest.fixture
def mock_config():
    return MockConfig()

# Test respond method when VectorDB does not exist
@patch("os.path.exists", return_value=False)
def test_respond_no_vectordb(mock_exists, chatbot, mock_config):
    message = "Hello, how are you?"
    response = Chatbot.respond(chatbot, message, mock_config)
    assert response == ("", chatbot, None)
    assert chatbot[-1][1] == "VectorDB doesn't exist. Please upload a document and execute the 'upload_data_manually.py' to create VectorDB."

# Test text cleaning function
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello&nbsp;World", "Hello World"),
    ("  Spaces  everywhere   ", "Spaces everywhere"),
    (b"Encoding\x89".decode("latin1", "ignore"), "Encoding")
])
def test_clean_text(input_text, expected_output):
    assert Chatbot.clean_text(input_text) == expected_output
