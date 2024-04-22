import unittest
from gradio.testing import Client
from hubermananswers_app import demo

class TestHubermanAnswersApp(unittest.TestCase):
    def setUp(self):
        self.client = Client(demo)

    def test_input_submission(self):
        input_text = "What is the meaning of life?"
        expected_output = "The meaning of life is 42."
        response = self.client.post("/input_txt", {"input_txt": input_text})
        self.assertEqual(response.text, expected_output)

    def test_button_click(self):
        input_text = "Tell me a joke."
        expected_output = "Why don't scientists trust atoms? Because they make up everything!"
        response = self.client.post("/text_submit_btn", {"text_submit_btn": "Submit"})
        self.assertEqual(response.text, expected_output)

if __name__ == '__main__':
    unittest.main()