import unittest
from unittest.mock import patch
from chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def test_respond(self):
        chatbot = []
        message = "Hello"
        data_type = "Preprocessed"
        temperature = 0

        with patch('chatbot.Chroma') as mock_chroma:
            mock_chroma.return_value.similarity_search.return_value = ["doc1", "doc2"]
            response = Chatbot.respond(chatbot, message, data_type, temperature)

        self.assertEqual(response[0], "")
        self.assertEqual(response[1], [(message, "response")])
        self.assertEqual(response[2], "markdown_documents")

    def test_clean_references(self):
        documents = ["page_content=content metadata={source: 'file.txt', page: 1}"]
        expected_result = "markdown_documents"

        result = Chatbot.clean_references(documents)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()