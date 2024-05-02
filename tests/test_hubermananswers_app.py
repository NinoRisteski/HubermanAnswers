import pytest
from unittest.mock import patch
from utils.chatbot import Chatbot
import src.hubermananswers_app

# Create a fixture for the application
@pytest.fixture
def app():
    return hubermananswers_app.demo

# Test to ensure the app can be launched
def test_app_launch(app):
    with patch('gradio.Blocks.launch'):
        app.launch()
        assert True  

# Test the chatbot response mechanism
@patch.object(Chatbot, 'respond', return_value=["", "Hello, how can I help?", ""])
def test_chatbot_interaction(mock_respond, app):
    # Simulate input to the chatbot and button press
    with app.test_client() as client:
        response = client.post("/", json={
            "input_txt": "What is the meaning of life?",
            "chatbot": [],
            "temperature_bar": 0.5
        })
        # Validate that our mock was called
        mock_respond.assert_called_once()
        assert mock_respond.call_args[1]["inputs"][1] == "What is the meaning of life?"
        assert mock_respond.call_args[1]["inputs"][2] == 0.5

        # Check the response was as expected
        assert "Hello, how can I help?" in response.get_data(as_text=True)
